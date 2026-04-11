#!/usr/bin/env python3
"""
File GitHub issues from a harden audit findings.json.

Usage:
    # File issues for a batch and save issue URLs back to findings.json:
    uv run python skills/harden/harden-issues.py findings.json --repo owner/repo --batch 1

    # File issues AND create the PR in one shot:
    uv run python skills/harden/harden-issues.py findings.json \
        --repo owner/repo --batch 1 --create-pr

    # Create PR only (issues already filed, URLs in findings.json):
    uv run python skills/harden/harden-issues.py findings.json \
        --repo owner/repo --batch 1 --create-pr --skip-issues

Prerequisites:
    - gh CLI installed and authenticated
    - findings.json produced by validate_findings.py + score_audit.py pipeline
    - GitHub labels exist: Critical, High, Medium, Low, harden, blocking
    - For --create-pr: must be on the feature branch for that batch

findings.json format (array of finding objects):
    [
      {
        "id": "SEC-1",
        "title": "Hardcoded API key in config.py",
        "scope": "Security",
        "severity": "Critical",
        "blocking": true,
        "where": "config.py:42",
        "what": "...",
        "proof": "...",
        "impact": "...",
        "fix": "...",
        "batch": 1
        // issue_url is written here automatically after filing
      },
      ...
    ]
"""
import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

from harden_state import mark_batch_filed, update_batch_state
from schema import REQUIRED_FIELDS
from schema import VALID_SEVERITIES as SEVERITY_LABELS

MAX_BODY_LEN = 65535


def _strip_html(text: str) -> str:
    """Remove raw HTML tags from a string."""
    return re.sub(r'<[^>]+>', '', text)


def build_body(f: dict) -> str:
    blocking_str = "Yes" if f.get("blocking") else "No"
    what = _strip_html(f.get('what', ''))
    proof = _strip_html(f.get('proof', ''))
    impact = _strip_html(f.get('impact', ''))
    fix = _strip_html(f.get('fix', ''))
    body = f"""### {f['id']}: {f['title']}

**Scope:** {f['scope']}
**Severity:** {f['severity']}
**Blocking:** {blocking_str}
**Where:** `{f['where']}`

**What:**
{what}

**Proof:**
{proof}

**Impact:**
{impact}

**Fix:**
{fix}

---
*Filed by harden-issues.py from audit findings.json*
"""
    if len(body) > MAX_BODY_LEN:
        body = body[:MAX_BODY_LEN] + "\n\n*(truncated)*"
    return body


def create_issue(finding: dict, repo: str, batch: int, dry_run: bool) -> str | None:
    """Create a GitHub issue for a finding. Returns the issue URL on success, None on failure."""
    labels = ["harden", finding["severity"].lower()]
    if finding.get("blocking"):
        labels.append("blocking")

    title = f"[harden] {finding['id']}: {finding['title']}"
    body = build_body(finding)

    cmd = [
        "gh", "issue", "create",
        "--repo", repo,
        "--title", title,
        "--body", body,
        "--label", ",".join(labels),
    ]

    if dry_run:
        print(f"[dry-run] Would create: {title}")
        print(f"          Labels: {labels}")
        return None

    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"ERROR creating issue for {finding['id']}: {result.stderr.strip()}", file=sys.stderr)
        return None

    url = result.stdout.strip()
    print(f"Created: {url}")
    return url


def save_issue_url(findings_path: Path, finding_id: str, url: str) -> None:
    """Write issue_url back to the matching finding in findings.json."""
    all_findings = json.loads(findings_path.read_text())
    for f in all_findings:
        if f.get("id") == finding_id:
            f["issue_url"] = url
            break
    findings_path.write_text(json.dumps(all_findings, indent=2) + "\n")


def create_pr(
    findings: list[dict], batch_num: int, repo: str, dry_run: bool
) -> None:
    """Create a GitHub PR for a batch using issue_url fields already in findings."""
    branch = subprocess.run(
        ["git", "branch", "--show-current"], capture_output=True, text=True
    ).stdout.strip()
    if not branch:
        print("ERROR: could not determine current branch", file=sys.stderr)
        sys.exit(1)

    ids = ", ".join(f.get("id", "?") for f in findings)
    title = f"fix(harden): batch {batch_num} — {ids}"

    missing_urls = [f["id"] for f in findings if not f.get("issue_url")]
    if missing_urls:
        print(
            f"WARNING: no issue_url for {missing_urls} — run without --skip-issues first",
            file=sys.stderr,
        )

    summary_lines = "\n".join(
        f"- **{f['id']}**: {f['title']}" for f in findings
    )
    closes_lines = "\n".join(
        f"Closes {f['issue_url']}" for f in findings if f.get("issue_url")
    )
    body = f"""## Summary
{summary_lines}

## Test plan
- [ ] Verify each fix matches its finding description
- [ ] Run existing tests: `uv run pytest skills/harden/tests/`

{closes_lines}

🤖 Generated with [Claude Code](https://claude.com/claude-code)
"""

    cmd = [
        "gh", "pr", "create",
        "--repo", repo,
        "--base", "main",
        "--head", branch,
        "--title", title,
        "--body", body,
    ]

    if dry_run:
        print(f"[dry-run] Would create PR: {title}")
        print(f"          Branch: {branch}")
        print(f"          Closes: {closes_lines or '(none)'}")
        return

    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"ERROR creating PR: {result.stderr.strip()}", file=sys.stderr)
    else:
        print(f"PR created: {result.stdout.strip()}")


def validate_findings(findings: list[dict]) -> list[str]:
    """Return a list of validation error strings; empty list means valid."""
    errors: list[str] = []
    for i, f in enumerate(findings):
        missing = REQUIRED_FIELDS - set(f.keys())
        if missing:
            errors.append(f"Finding {i}: missing fields {missing}")
        if f.get("severity", "").lower() not in SEVERITY_LABELS:
            errors.append(
                f"Finding {i} ({f.get('id', '?')}): invalid severity '{f.get('severity')}'"
            )
    return errors


def main() -> None:
    parser = argparse.ArgumentParser(description="File GitHub issues from harden audit findings")
    parser.add_argument("findings", help="Path to findings.json")
    parser.add_argument("--repo", required=True, help="GitHub repo in owner/repo format")
    parser.add_argument(
        "--dry-run", action="store_true", help="Print what would be created without filing"
    )
    parser.add_argument(
        "--batch", type=int, default=None, help="Only file issues for this batch number"
    )
    parser.add_argument(
        "--create-pr",
        action="store_true",
        help="Create a PR after filing issues (requires --batch)",
    )
    parser.add_argument(
        "--skip-issues",
        action="store_true",
        help="Skip filing issues; only create the PR (requires --create-pr)",
    )
    args = parser.parse_args()

    if args.create_pr and args.batch is None:
        print("ERROR: --create-pr requires --batch", file=sys.stderr)
        sys.exit(1)
    if args.skip_issues and not args.create_pr:
        print("ERROR: --skip-issues requires --create-pr", file=sys.stderr)
        sys.exit(1)

    findings_path = Path(args.findings)
    state_path = findings_path.parent / "harden-state.json"
    if not findings_path.exists():
        print(f"ERROR: {findings_path} not found", file=sys.stderr)
        sys.exit(1)

    try:
        findings = json.loads(findings_path.read_text())
    except json.JSONDecodeError as e:
        print(f"ERROR: Invalid JSON in {findings_path}: {e}", file=sys.stderr)
        sys.exit(1)

    if not isinstance(findings, list):
        print("ERROR: findings.json must be a JSON array", file=sys.stderr)
        sys.exit(1)

    # Filter by batch if specified
    if args.batch is not None:
        batch_findings = [f for f in findings if f.get("batch") == args.batch]
    else:
        batch_findings = findings

    if not args.skip_issues:
        label = f"batch {args.batch}" if args.batch is not None else "all batches"
        print(f"Filing {len(batch_findings)} issue(s) for {label}")

        errors = validate_findings(batch_findings)
        if errors:
            print("Validation errors — fix before filing:", file=sys.stderr)
            for e in errors:
                print(f"  - {e}", file=sys.stderr)
            sys.exit(1)

        findings_sorted = sorted(
            batch_findings, key=lambda f: (f.get("batch", 99), f.get("id", ""))
        )
        for finding in findings_sorted:
            url = create_issue(
                finding, repo=args.repo, batch=finding.get("batch", 1), dry_run=args.dry_run
            )
            if url and not args.dry_run:
                save_issue_url(findings_path, finding["id"], url)
                update_batch_state(state_path, finding.get("batch", 1), finding["id"], url)
                # Reload so create_pr sees fresh issue_url values
                batch_findings = [
                    f for f in json.loads(findings_path.read_text())
                    if f.get("batch") == args.batch
                ]

    if args.batch is not None and not args.dry_run and not args.skip_issues:
        mark_batch_filed(state_path, args.batch)

    if args.create_pr:
        print("\nCreating PR...")
        create_pr(batch_findings, args.batch, repo=args.repo, dry_run=args.dry_run)

    print("\nDone.")


if __name__ == "__main__":
    main()
