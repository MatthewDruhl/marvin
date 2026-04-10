"""
validate_findings.py — Validate findings JSON before passing to score_audit.py.

Checks each finding has required fields with valid values.
Exits 0 if valid (or no findings), 1 with errors listed if invalid.

Usage:
  uv run python skills/harden/validate_findings.py findings.json
  cat findings.json | uv run python skills/harden/validate_findings.py
"""

import json
import sys
from pathlib import Path

from schema import REQUIRED_FIELDS, VALID_SEVERITIES


def validate(findings: list[dict]) -> list[str]:
    errors: list[str] = []
    for i, f in enumerate(findings):
        label = f"Finding[{i}] (scope={f.get('scope', '?')})"
        for field in REQUIRED_FIELDS:
            if field not in f:
                errors.append(f"{label}: missing required field '{field}'")
        sev = f.get("severity", "")
        if sev and sev.lower() not in VALID_SEVERITIES:
            errors.append(
                f"{label}: invalid severity '{sev}' — must be one of: "
                + ", ".join(sorted(VALID_SEVERITIES))
            )
        blocking = f.get("blocking")
        if blocking is not None and not isinstance(blocking, bool):
            errors.append(
                f"{label}: 'blocking' must be a boolean, got {type(blocking).__name__}"
            )
    return errors


def main() -> None:
    if "--help" in sys.argv or "-h" in sys.argv:
        print(__doc__)
        sys.exit(0)

    if len(sys.argv) > 1:
        path = Path(sys.argv[1])
        if not path.exists():
            print(f"Error: file not found: {path}", file=sys.stderr)
            sys.exit(1)
        try:
            findings = json.loads(path.read_text())
        except json.JSONDecodeError as e:
            print(f"Error: invalid JSON in {path}: {e}", file=sys.stderr)
            sys.exit(1)
    else:
        data = sys.stdin.read().strip()
        if not data:
            print("No findings to validate.")
            sys.exit(0)
        try:
            findings = json.loads(data)
        except json.JSONDecodeError as e:
            print(f"Error: invalid JSON on stdin: {e}", file=sys.stderr)
            sys.exit(1)

    if not isinstance(findings, list):
        print("Error: findings must be a JSON array", file=sys.stderr)
        sys.exit(1)

    errors = validate(findings)
    if errors:
        print(f"Validation failed — {len(errors)} error(s):")
        for err in errors:
            print(f"  {err}")
        sys.exit(1)

    print(f"Valid — {len(findings)} finding(s) passed.")


if __name__ == "__main__":
    main()
