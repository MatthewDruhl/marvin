#!/usr/bin/env python3
"""
File GitHub issues from a harden audit findings.json.

Usage:
    uv run python skills/harden/harden-issues.py findings.json --repo owner/repo

Prerequisites:
    - gh CLI installed and authenticated
    - findings.json produced by validate_findings.py + score_audit.py pipeline
    - GitHub labels exist: Critical, High, Medium, Low, harden, blocking
    - GitHub milestones match batch names in the findings (optional)

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
      },
      ...
    ]
"""
import argparse
import json
import subprocess
import sys
from pathlib import Path

from schema import REQUIRED_FIELDS
from schema import VALID_SEVERITIES as SEVERITY_LABELS


def build_body(f: dict) -> str:
    blocking_str = "Yes" if f.get("blocking") else "No"
    return f"""### {f['id']}: {f['title']}

**Scope:** {f['scope']}
**Severity:** {f['severity']}
**Blocking:** {blocking_str}
**Where:** `{f['where']}`

**What:**
{f.get('what', '')}

**Proof:**
{f.get('proof', '')}

**Impact:**
{f.get('impact', '')}

**Fix:**
{f.get('fix', '')}

---
*Filed by harden-issues.py from audit findings.json*
"""


def create_issue(finding: dict, repo: str, batch: int, dry_run: bool) -> None:
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
        return

    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"ERROR creating issue for {finding['id']}: {result.stderr.strip()}", file=sys.stderr)
    else:
        print(f"Created: {result.stdout.strip()}")


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
    args = parser.parse_args()

    findings_path = Path(args.findings)
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
        findings = [f for f in findings if f.get("batch") == args.batch]
        print(f"Filing {len(findings)} issue(s) for batch {args.batch}")
    else:
        print(f"Filing {len(findings)} issue(s) across all batches")

    errors = validate_findings(findings)
    if errors:
        print("Validation errors — fix before filing:", file=sys.stderr)
        for e in errors:
            print(f"  - {e}", file=sys.stderr)
        sys.exit(1)

    # File in batch order
    findings_sorted = sorted(findings, key=lambda f: (f.get("batch", 99), f.get("id", "")))
    for finding in findings_sorted:
        create_issue(finding, repo=args.repo, batch=finding.get("batch", 1), dry_run=args.dry_run)

    print("Done.")


if __name__ == "__main__":
    main()
