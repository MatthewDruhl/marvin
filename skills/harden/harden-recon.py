"""harden-recon.py — Fast static Pass 1 candidate scanner.

Scans a target directory for candidate issues using regex pattern matching.
No AI calls needed. Produces structured output for Pass 2 (full harden audit).

Usage:
    uv run python skills/harden/harden-recon.py <target_dir> [--output candidates.md] [--json]
"""

import argparse
import json
import re
import sys
import time
from dataclasses import dataclass, field
from pathlib import Path

# ---------------------------------------------------------------------------
# Patterns
# ---------------------------------------------------------------------------

SECRET_KEYWORDS = ["api_key", "secret", "password", "token", "private_key"]

# Matches: keyword = "literal" or keyword = 'literal'
# Does NOT match: keyword = os.environ.get(...) or keyword = config["..."]
SECRET_PATTERN = re.compile(
    r"""(?i)\w*(?:"""
    + "|".join(re.escape(k) for k in SECRET_KEYWORDS)
    + r""")\w*\s*=\s*['"][^'"]{1,}['"]""",
)

BARE_EXCEPT_PATTERN = re.compile(r"^\s*except\s*(?:Exception\s*)?:\s*$", re.MULTILINE)
HARDCODED_IP_PATTERN = re.compile(r"\b(\d{1,3})\.(\d{1,3})\.(\d{1,3})\.(\d{1,3})\b")
HARDCODED_PORT_PATTERN = re.compile(r"\bport\s*=\s*(\d{2,5})\b", re.IGNORECASE)

HANDLER_FUNC_PATTERN = re.compile(r"^\s*def\s+(handle_|process_|parse_)\w+\s*\(", re.MULTILINE)
VALIDATION_PATTERN = re.compile(r"\b(if not|raise|assert)\b")

# --- #211: Extended patterns ---

# Security: SQL injection (string formatting into queries)
SQL_INJECTION_PATTERN = re.compile(
    r"""(?:execute|cursor\.execute|\.query)\s*\(\s*(?:f['"]|['"].*%s|['"].*\.format)""",
    re.IGNORECASE,
)

# Security: unsafe deserialization
UNSAFE_DESERIALIZE_PATTERN = re.compile(
    r"\b(?:pickle\.loads?|yaml\.(?:load|unsafe_load))\s*\(",
)

# Security: shell injection via subprocess with shell=True
# Used for whole-file scanning (DOTALL) since shell=True often spans lines
SHELL_INJECTION_PATTERN = re.compile(
    r"\bsubprocess\.(?:call|run|Popen)\s*\([^)]*?shell\s*=\s*True",
    re.DOTALL,
)

# AI: unframed user input flowing into prompts
PROMPT_INJECTION_PATTERN = re.compile(
    r"""(?:prompt|message|content)\s*=\s*(?:f['"]|['"].*\.format|.*\+\s*(?:user_|input|request))""",
    re.IGNORECASE,
)

# Code Quality: unused imports (import X but X never used again in file)
# Detected post-scan by cross-referencing import names against file text.

# Decoupling: circular import guard (import inside function body = likely circular dep workaround)
LATE_IMPORT_PATTERN = re.compile(
    r"^(?:    |\t)+(import |from \S+ import )", re.MULTILINE
)

# --- End #211 patterns ---

EXCLUDED_DIRS = {"__pycache__", ".git", "node_modules", "venv", ".venv"}
EXCLUDED_SUFFIXES = {".lock", ".min.js"}

LARGE_FILE_THRESHOLD = 300

# --- #213: Risk scoring weights ---
SEVERITY_WEIGHTS: dict[str, int] = {
    "secrets": 5,
    "sql_injection": 5,
    "unsafe_deserialization": 5,
    "shell_injection": 5,
    "prompt_injection": 4,
    "bare_excepts": 2,
    "missing_input_validation": 3,
    "hardcoded_values": 2,
    "late_imports": 1,
    "test_gaps": 2,
    "large_files": 1,
}

# Higher-risk file path patterns (auth, config, routes)
HIGH_RISK_PATH_KEYWORDS = {
    "auth", "login", "config", "secret", "cred",
    "route", "api", "admin", "middleware",
}

# Valid IP octet range check
def _is_valid_ip(groups: tuple[str, ...]) -> bool:
    return all(0 <= int(g) <= 255 for g in groups)


# ---------------------------------------------------------------------------
# Data model
# ---------------------------------------------------------------------------

@dataclass
class Candidate:
    category: str
    file: str
    line: int | None
    detail: str
    risk_score: float = 0.0

    def to_dict(self) -> dict:
        d = {
            "category": self.category,
            "file": self.file,
            "line": self.line,
            "detail": self.detail,
        }
        if self.risk_score > 0:
            d["risk_score"] = self.risk_score
        return d


@dataclass
class FileRiskScore:
    """Aggregated risk score for a single file."""
    file: str
    score: float
    match_count: int
    categories: set[str] = field(default_factory=set)


@dataclass
class ReconResult:
    target: str
    files_scanned: int
    duration: float
    candidates: list[Candidate] = field(default_factory=list)
    file_risk_scores: dict[str, FileRiskScore] = field(default_factory=dict)

    def by_category(self) -> dict[str, list[Candidate]]:
        result: dict[str, list[Candidate]] = {}
        for c in self.candidates:
            result.setdefault(c.category, []).append(c)
        return result

    def files_by_risk(self) -> list[FileRiskScore]:
        """Return files sorted by risk score (highest first)."""
        return sorted(self.file_risk_scores.values(), key=lambda f: f.score, reverse=True)


# ---------------------------------------------------------------------------
# File collection
# ---------------------------------------------------------------------------

def _collect_python_files(target: Path) -> list[Path]:
    """Return all .py files, excluding blacklisted dirs and suffixes."""
    files: list[Path] = []
    for path in target.rglob("*.py"):
        # Check no excluded dir is in the path parts
        if any(part in EXCLUDED_DIRS for part in path.parts):
            continue
        if path.suffix in EXCLUDED_SUFFIXES:
            continue
        files.append(path)
    return files


def _collect_all_files(target: Path) -> list[Path]:
    """Return all non-excluded files (any extension)."""
    files: list[Path] = []
    for path in target.rglob("*"):
        if not path.is_file():
            continue
        if any(part in EXCLUDED_DIRS for part in path.parts):
            continue
        if path.suffix in EXCLUDED_SUFFIXES:
            continue
        files.append(path)
    return files


# ---------------------------------------------------------------------------
# Scanners
# ---------------------------------------------------------------------------

def _scan_secrets(path: Path, rel: str) -> list[Candidate]:
    candidates: list[Candidate] = []
    try:
        text = path.read_text(encoding="utf-8", errors="ignore")
    except OSError:
        return candidates
    for i, line in enumerate(text.splitlines(), start=1):
        if SECRET_PATTERN.search(line):
            # Extract which keyword triggered the match
            stripped = line.strip()
            keyword = next(
                (k for k in SECRET_KEYWORDS if k.lower() in stripped.lower()),
                "secret",
            )
            candidates.append(
                Candidate(
                    category="secrets",
                    file=rel,
                    line=i,
                    detail=f"hardcoded {keyword} assignment",
                )
            )
    return candidates


def _scan_bare_excepts(path: Path, rel: str) -> list[Candidate]:
    candidates: list[Candidate] = []
    try:
        text = path.read_text(encoding="utf-8", errors="ignore")
    except OSError:
        return candidates

    lines = text.splitlines()
    for i, line in enumerate(lines, start=1):
        if re.match(r"^\s*except\s*(?:Exception\s*)?:\s*$", line):
            # Check if there's a re-raise or logging in the next ~5 lines
            block = lines[i : i + 5]  # lines after except (i is 1-based, index is i)
            block_text = "\n".join(block)
            reraise_pat = re.compile(
                r"\braise\b|\blog(ging)?\b|logger\b|print\b|warn\b", re.IGNORECASE
            )
            has_reraise = bool(reraise_pat.search(block_text))
            if not has_reraise:
                candidates.append(
                    Candidate(
                        category="bare_excepts",
                        file=rel,
                        line=i,
                        detail="bare except with no logging/re-raise",
                    )
                )
    return candidates


def _scan_missing_validation(path: Path, rel: str) -> list[Candidate]:
    """Flag handle_*/process_*/parse_* functions with no early validation."""
    candidates: list[Candidate] = []
    try:
        text = path.read_text(encoding="utf-8", errors="ignore")
    except OSError:
        return candidates

    lines = text.splitlines()
    for i, line in enumerate(lines, start=1):
        m = re.match(r"^\s*def\s+(handle_\w+|process_\w+|parse_\w+)\s*\(", line)
        if not m:
            continue
        func_name = m.group(1)
        # Check first 5 lines of function body for validation
        body_lines = lines[i : i + 5]  # i is 1-based so lines[i] is line after def
        body_text = "\n".join(body_lines)
        if not VALIDATION_PATTERN.search(body_text):
            candidates.append(
                Candidate(
                    category="missing_input_validation",
                    file=rel,
                    line=i,
                    detail=f"{func_name}(): no early validation",
                )
            )
    return candidates


def _scan_hardcoded_values(path: Path, rel: str) -> list[Candidate]:
    candidates: list[Candidate] = []
    # Skip test files for port scanning (but still scan IPs)
    is_test = "test_" in path.name or path.name.startswith("test")
    try:
        text = path.read_text(encoding="utf-8", errors="ignore")
    except OSError:
        return candidates

    for i, line in enumerate(text.splitlines(), start=1):
        # Hardcoded IPs
        for m in HARDCODED_IP_PATTERN.finditer(line):
            if _is_valid_ip(m.groups()):
                ip = m.group(0)
                candidates.append(
                    Candidate(
                        category="hardcoded_values",
                        file=rel,
                        line=i,
                        detail=f"hardcoded IP: {ip}",
                    )
                )

        # Hardcoded ports (non-test files only)
        if not is_test:
            for m in HARDCODED_PORT_PATTERN.finditer(line):
                port = int(m.group(1))
                if 1 <= port <= 65535:
                    candidates.append(
                        Candidate(
                            category="hardcoded_values",
                            file=rel,
                            line=i,
                            detail=f"hardcoded port: {port}",
                        )
                    )
    return candidates


def _build_test_file_set(all_py_files: list[Path]) -> set[str]:
    """Return set of base names that test files cover (e.g. 'module' from 'test_module.py')."""
    covered: set[str] = set()
    for f in all_py_files:
        if f.name.startswith("test_"):
            covered.add(f.name[5:])  # strip "test_" prefix
        elif f.name.endswith("_test.py"):
            covered.add(f.name[: -len("_test.py")] + ".py")
    return covered


def _scan_test_gaps(target: Path, py_files: list[Path]) -> list[Candidate]:
    """Flag source files that have no corresponding test file anywhere in the tree."""
    candidates: list[Candidate] = []
    test_covered = _build_test_file_set(py_files)

    for path in py_files:
        # Only flag src/ files or root-level .py files (not test files themselves)
        rel_parts = path.relative_to(target).parts
        in_src = len(rel_parts) >= 1 and rel_parts[0] == "src"
        is_root_level = len(rel_parts) == 1
        is_test_file = path.name.startswith("test_") or path.name.endswith("_test.py")

        if is_test_file:
            continue

        if in_src or is_root_level:
            if path.name not in test_covered:
                candidates.append(
                    Candidate(
                        category="test_gaps",
                        file=str(path.relative_to(target)),
                        line=None,
                        detail="no test file found",
                    )
                )
    return candidates


def _scan_large_files(target: Path, py_files: list[Path]) -> list[Candidate]:
    """Flag files > 300 lines with no corresponding test file."""
    candidates: list[Candidate] = []
    test_covered = _build_test_file_set(py_files)

    for path in py_files:
        is_test_file = path.name.startswith("test_") or path.name.endswith("_test.py")
        if is_test_file:
            continue
        try:
            line_count = path.read_text(encoding="utf-8", errors="ignore").count("\n")
        except OSError:
            continue
        if line_count > LARGE_FILE_THRESHOLD and path.name not in test_covered:
            candidates.append(
                Candidate(
                    category="large_files",
                    file=str(path.relative_to(target)),
                    line=None,
                    detail=f"{line_count} lines, no test file",
                )
            )
    return candidates


# --- #211: New scanners ---


def _scan_sql_injection(path: Path, rel: str) -> list[Candidate]:
    candidates: list[Candidate] = []
    try:
        text = path.read_text(encoding="utf-8", errors="ignore")
    except OSError:
        return candidates
    for i, line in enumerate(text.splitlines(), start=1):
        if SQL_INJECTION_PATTERN.search(line):
            candidates.append(
                Candidate(
                    category="sql_injection",
                    file=rel,
                    line=i,
                    detail="possible SQL injection via string formatting",
                )
            )
    return candidates


def _scan_unsafe_deserialization(path: Path, rel: str) -> list[Candidate]:
    candidates: list[Candidate] = []
    try:
        text = path.read_text(encoding="utf-8", errors="ignore")
    except OSError:
        return candidates
    for i, line in enumerate(text.splitlines(), start=1):
        if UNSAFE_DESERIALIZE_PATTERN.search(line):
            candidates.append(
                Candidate(
                    category="unsafe_deserialization",
                    file=rel,
                    line=i,
                    detail="unsafe deserialization (pickle/yaml.load)",
                )
            )
    return candidates


def _scan_shell_injection(path: Path, rel: str) -> list[Candidate]:
    """Scan whole file for subprocess calls with shell=True (often spans multiple lines)."""
    candidates: list[Candidate] = []
    try:
        text = path.read_text(encoding="utf-8", errors="ignore")
    except OSError:
        return candidates
    for m in SHELL_INJECTION_PATTERN.finditer(text):
        # Find line number from match position
        line_num = text[:m.start()].count("\n") + 1
        candidates.append(
            Candidate(
                category="shell_injection",
                file=rel,
                line=line_num,
                detail="subprocess with shell=True",
            )
        )
    return candidates


def _scan_prompt_injection(path: Path, rel: str) -> list[Candidate]:
    candidates: list[Candidate] = []
    try:
        text = path.read_text(encoding="utf-8", errors="ignore")
    except OSError:
        return candidates
    for i, line in enumerate(text.splitlines(), start=1):
        if PROMPT_INJECTION_PATTERN.search(line):
            candidates.append(
                Candidate(
                    category="prompt_injection",
                    file=rel,
                    line=i,
                    detail="user input may flow into prompt unsanitized",
                )
            )
    return candidates


def _scan_late_imports(path: Path, rel: str) -> list[Candidate]:
    """Flag imports inside function bodies (often a circular-dependency workaround)."""
    candidates: list[Candidate] = []
    try:
        text = path.read_text(encoding="utf-8", errors="ignore")
    except OSError:
        return candidates
    in_function = False
    for i, line in enumerate(text.splitlines(), start=1):
        if re.match(r"^\s*def\s+", line) or re.match(r"^\s*async\s+def\s+", line):
            in_function = True
        elif line and not line[0].isspace():
            in_function = False
        if in_function and re.match(r"^(?:    |\t)+(?:import |from \S+ import )", line):
            candidates.append(
                Candidate(
                    category="late_imports",
                    file=rel,
                    line=i,
                    detail="import inside function body (possible circular dep workaround)",
                )
            )
    return candidates


# ---------------------------------------------------------------------------
# Main scan entry point
# ---------------------------------------------------------------------------

def _compute_risk_scores(
    candidates: list[Candidate], target: Path
) -> dict[str, FileRiskScore]:
    """Compute per-file risk scores from candidates (#213)."""
    scores: dict[str, FileRiskScore] = {}
    for c in candidates:
        if c.file not in scores:
            scores[c.file] = FileRiskScore(file=c.file, score=0.0, match_count=0)
        fs = scores[c.file]
        fs.match_count += 1
        fs.categories.add(c.category)
        fs.score += SEVERITY_WEIGHTS.get(c.category, 1)

    # Bonus for high-risk path keywords (auth, config, etc.)
    for rel, fs in scores.items():
        rel_lower = rel.lower()
        if any(kw in rel_lower for kw in HIGH_RISK_PATH_KEYWORDS):
            fs.score *= 1.5

    # Apply score back to individual candidates
    for c in candidates:
        if c.file in scores:
            c.risk_score = scores[c.file].score

    return scores


def run_recon(target_dir: str | Path) -> ReconResult:
    target = Path(target_dir).resolve()
    start = time.monotonic()

    py_files = _collect_python_files(target)
    all_files_count = len(_collect_all_files(target))

    candidates: list[Candidate] = []

    for path in py_files:
        rel = str(path.relative_to(target))
        # Original scanners
        candidates.extend(_scan_secrets(path, rel))
        candidates.extend(_scan_bare_excepts(path, rel))
        candidates.extend(_scan_missing_validation(path, rel))
        candidates.extend(_scan_hardcoded_values(path, rel))
        # #211: New scanners
        candidates.extend(_scan_sql_injection(path, rel))
        candidates.extend(_scan_unsafe_deserialization(path, rel))
        candidates.extend(_scan_shell_injection(path, rel))
        candidates.extend(_scan_prompt_injection(path, rel))
        candidates.extend(_scan_late_imports(path, rel))

    # File-level checks (no per-line context needed)
    candidates.extend(_scan_test_gaps(target, py_files))
    candidates.extend(_scan_large_files(target, py_files))

    # #213: Compute per-file risk scores and sort candidates
    file_risk_scores = _compute_risk_scores(candidates, target)

    duration = time.monotonic() - start
    return ReconResult(
        target=str(target),
        files_scanned=all_files_count,
        duration=duration,
        candidates=candidates,
        file_risk_scores=file_risk_scores,
    )


# ---------------------------------------------------------------------------
# Output formatters
# ---------------------------------------------------------------------------

CATEGORY_LABELS: dict[str, str] = {
    "secrets": "Secrets",
    "sql_injection": "SQL Injection",
    "unsafe_deserialization": "Unsafe Deserialization",
    "shell_injection": "Shell Injection",
    "prompt_injection": "Prompt Injection",
    "bare_excepts": "Bare Excepts",
    "missing_input_validation": "Missing Input Validation",
    "hardcoded_values": "Hardcoded Values",
    "late_imports": "Late Imports (Circular Dep Indicator)",
    "test_gaps": "Test Gaps",
    "large_files": "Large Files",
}

CATEGORY_ORDER = list(CATEGORY_LABELS.keys())


def format_markdown(result: ReconResult) -> str:
    lines: list[str] = [
        "# Harden Recon — Candidates",
        "",
        f"Scanned: {result.target}",
        f"Files scanned: {result.files_scanned}",
        f"Candidates found: {len(result.candidates)}",
        f"Duration: {result.duration:.1f}s",
        "",
    ]

    # #213: Risk-ranked file summary
    ranked_files = result.files_by_risk()
    if ranked_files:
        lines.append("## File Risk Ranking")
        lines.append("")
        lines.append("| Rank | File | Score | Matches | Categories |")
        lines.append("|------|------|-------|---------|------------|")
        for rank, fs in enumerate(ranked_files, start=1):
            cats = ", ".join(sorted(fs.categories))
            lines.append(f"| {rank} | `{fs.file}` | {fs.score:.1f} | {fs.match_count} | {cats} |")
        lines.append("")
        lines.append("*Agent should read files in this order (highest risk first).*")
        lines.append("")

    by_cat = result.by_category()

    for cat in CATEGORY_ORDER:
        label = CATEGORY_LABELS[cat]
        items = by_cat.get(cat, [])
        lines.append(f"## {label} ({len(items)})")
        if items:
            for c in items:
                loc = f"{c.file}:{c.line}" if c.line is not None else c.file
                lines.append(f"- `{loc}` — {c.detail}")
        lines.append("")

    return "\n".join(lines)


def format_json(result: ReconResult) -> str:
    output: dict = {
        "candidates": [c.to_dict() for c in result.candidates],
        "file_risk_ranking": [
            {"file": fs.file, "score": fs.score, "match_count": fs.match_count,
             "categories": sorted(fs.categories)}
            for fs in result.files_by_risk()
        ],
    }
    return json.dumps(output, indent=2)


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Fast static Pass 1 candidate scanner for harden audits.",
    )
    parser.add_argument("target_dir", help="Directory to scan")
    parser.add_argument(
        "--output",
        metavar="FILE",
        help="Write output to file (default: stdout)",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        dest="as_json",
        help="Output as JSON array instead of markdown",
    )
    args = parser.parse_args(argv)

    target = Path(args.target_dir)
    if not target.exists():
        print(f"Error: target directory does not exist: {target}", file=sys.stderr)
        return 1
    if not target.is_dir():
        print(f"Error: target is not a directory: {target}", file=sys.stderr)
        return 1

    result = run_recon(target)
    output = format_json(result) if args.as_json else format_markdown(result)

    if args.output:
        Path(args.output).write_text(output, encoding="utf-8")
        print(f"Output written to {args.output}")
    else:
        print(output)

    return 0


if __name__ == "__main__":
    sys.exit(main())
