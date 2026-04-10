"""
score_audit.py — Scorecard grade calculator for /harden audit findings.

Grading formula:
  Points per finding: Critical=4, High=3, Medium=2, Low=1
  Any critical finding in a scope = D minimum (cannot grade above D until resolved)
  Grade thresholds (per scope): A=0pts, B=1-4pts, C=5-9pts, D=10-14pts, F=15+pts
  Overall grade = average of scope grades (A=4, B=3, C=2, D=1, F=0), rounded.

Input JSON format:
  [{"scope": "Security", "severity": "High", "blocking": true}, ...]
"""

import json
import math
import sys
from pathlib import Path

SEVERITY_POINTS: dict[str, int] = {
    "critical": 4,
    "high": 3,
    "medium": 2,
    "low": 1,
}

GRADE_THRESHOLDS: list[tuple[float, float, str]] = [
    (0, 0, "A"),
    (1, 4, "B"),
    (5, 9, "C"),
    (10, 14, "D"),
    (15, math.inf, "F"),
]

GRADE_TO_GPA: dict[str, int] = {"A": 4, "B": 3, "C": 2, "D": 1, "F": 0}
GPA_TO_GRADE: dict[int, str] = {v: k for k, v in GRADE_TO_GPA.items()}


def points_to_grade(points: int, has_critical: bool) -> str:
    for lo, hi, grade in GRADE_THRESHOLDS:
        if lo <= points <= hi:
            if has_critical and grade in ("A", "B", "C"):
                return "D"
            return grade
    return "F"


def format_severity_counts(findings: list[dict]) -> str:
    counts: dict[str, int] = {}
    for f in findings:
        sev = f.get("severity", "").lower()
        counts[sev] = counts.get(sev, 0) + 1
    if not counts:
        return "—"
    order = ["critical", "high", "medium", "low"]
    parts = [f"{counts[s]} {s}" for s in order if s in counts]
    return ", ".join(parts)


def compute_scorecard(findings: list[dict]) -> None:
    if not findings:
        print("No findings — Grade: A")
        return

    scopes: dict[str, list[dict]] = {}
    for f in findings:
        scope = f.get("scope", "Unknown")
        scopes.setdefault(scope, []).append(f)

    rows: list[tuple[str, str, str, str]] = []
    gpa_values: list[int] = []

    for scope, scope_findings in sorted(scopes.items()):
        blocking = [f for f in scope_findings if f.get("blocking", False)]
        non_blocking = [f for f in scope_findings if not f.get("blocking", False)]

        total_points = sum(
            SEVERITY_POINTS.get(f.get("severity", "").lower(), 0) for f in scope_findings
        )
        has_critical = any(f.get("severity", "").lower() == "critical" for f in scope_findings)
        grade = points_to_grade(total_points, has_critical)
        gpa_values.append(GRADE_TO_GPA[grade])

        rows.append((
            scope, grade, format_severity_counts(blocking), format_severity_counts(non_blocking)
        ))

    overall_gpa = int(sum(gpa_values) / len(gpa_values) + 0.5)
    overall_grade = GPA_TO_GRADE[overall_gpa]

    print("| Scope | Grade | Blocking | Non-blocking |")
    print("|-------|-------|----------|--------------|")
    for scope, grade, blocking_str, non_blocking_str in rows:
        print(f"| {scope} | {grade} | {blocking_str} | {non_blocking_str} |")
    print()
    print(f"Overall: {overall_grade}")


def main() -> None:
    if "--help" in sys.argv or "-h" in sys.argv:
        print(__doc__)
        print(f"Usage: uv run python {sys.argv[0]} [findings.json]")
        print(f"       cat findings.json | uv run python {sys.argv[0]}")
        sys.exit(0)

    if len(sys.argv) > 1:
        path = Path(sys.argv[1])
        if not path.exists() or path.stat().st_size == 0:
            print("No findings — Grade: A")
            sys.exit(0)
        try:
            findings = json.loads(path.read_text())
        except json.JSONDecodeError as e:
            print(f"Error: invalid JSON in {path}: {e}", file=sys.stderr)
            sys.exit(1)
    else:
        data = sys.stdin.read().strip()
        if not data:
            print("No findings — Grade: A")
            sys.exit(0)
        try:
            findings = json.loads(data)
        except json.JSONDecodeError as e:
            print(f"Error: invalid JSON on stdin: {e}", file=sys.stderr)
            sys.exit(1)

    compute_scorecard(findings)


if __name__ == "__main__":
    main()
