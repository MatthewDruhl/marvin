#!/usr/bin/env python3
"""
Compute a deterministic batch plan from findings.json.

Batching rules (in priority order):
  1. Blocking findings go in Batch 1 — always
  2. Non-blocking findings grouped by scope — same scope stays together
  3. Within a scope group, ordered by severity (Critical → High → Medium → Low)
  4. Scope groups ordered by highest-severity finding within the group

Usage:
    uv run python skills/harden/batch_plan.py findings.json
    uv run python skills/harden/batch_plan.py findings.json --assign   # writes batch numbers back
    uv run python skills/harden/batch_plan.py findings.json --json      # machine-readable output
"""
import argparse
import json
import sys
from pathlib import Path

SEVERITY_WEIGHT = {"critical": 4, "high": 3, "medium": 2, "low": 1}
EFFORT_BY_COUNT = {1: "Low", 2: "Low", 3: "Medium", 4: "Medium"}


def effort(count: int) -> str:
    return EFFORT_BY_COUNT.get(count, "High")


def severity_weight(finding: dict) -> int:
    return SEVERITY_WEIGHT.get(finding.get("severity", "").lower(), 0)


def group_into_batches(findings: list[dict]) -> list[list[dict]]:
    """Split findings into batches following the batching rules.

    Returns a list of batches, each batch being a list of findings.
    Batch 0 in the return value = Batch 1 for the user.
    """
    blocking = [f for f in findings if f.get("blocking")]
    non_blocking = [f for f in findings if not f.get("blocking")]

    batches: list[list[dict]] = []

    # Batch 1: all blocking findings, sorted by severity desc
    if blocking:
        batches.append(sorted(blocking, key=severity_weight, reverse=True))

    # Remaining batches: non-blocking grouped by scope
    scope_groups: dict[str, list[dict]] = {}
    for f in non_blocking:
        scope = f.get("scope", "Other")
        scope_groups.setdefault(scope, []).append(f)

    # Sort scope groups by highest severity in the group (desc)
    sorted_scopes = sorted(
        scope_groups.items(),
        key=lambda kv: max(severity_weight(f) for f in kv[1]),
        reverse=True,
    )

    # Pack scope groups into batches of up to 5 findings each
    current_batch: list[dict] = []
    for _scope, group in sorted_scopes:
        group_sorted = sorted(group, key=severity_weight, reverse=True)
        if current_batch and len(current_batch) + len(group_sorted) > 5:
            batches.append(current_batch)
            current_batch = []
        current_batch.extend(group_sorted)
    if current_batch:
        batches.append(current_batch)

    return batches


def batch_description(batch: list[dict], batch_num: int) -> str:
    """Generate a short description for a batch."""
    if any(f.get("blocking") for f in batch):
        return "blocking fixes"
    scopes = list(dict.fromkeys(f.get("scope", "Other") for f in batch))
    return " + ".join(scopes).lower()


def render_plan(batches: list[list[dict]]) -> str:
    """Render the batch plan in SKILL.md format."""
    lines = []
    for i, batch in enumerate(batches):
        batch_num = i + 1
        is_blocking = any(f.get("blocking") for f in batch)
        desc = batch_description(batch, batch_num)
        ids = ", ".join(f.get("id", "?") for f in batch)
        dep = "None — do this first" if batch_num == 1 else f"Batch {batch_num - 1}"

        lines.append(f"### Batch {batch_num} — {desc} ({len(batch)} issues)")
        lines.append(f"Resolves: {ids}")
        blocking_str = (  # noqa: E501
            "Yes — must fix before shipping" if is_blocking else "No — quality improvement"
        )
        lines.append(f"Blocking: {blocking_str}")
        lines.append(f"Dependency: {dep}")
        lines.append(f"Effort: {effort(len(batch))}")
        lines.append("")

    return "\n".join(lines).rstrip()


def assign_batches(findings_path: Path, batches: list[list[dict]]) -> None:
    """Write batch numbers back to findings.json."""
    id_to_batch: dict[str, int] = {}
    for i, batch in enumerate(batches):
        for f in batch:
            id_to_batch[f["id"]] = i + 1

    all_findings = json.loads(findings_path.read_text())
    for f in all_findings:
        if f.get("id") in id_to_batch:
            f["batch"] = id_to_batch[f["id"]]
    findings_path.write_text(json.dumps(all_findings, indent=2) + "\n")
    print(f"Batch numbers written to {findings_path}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Compute batch plan from findings.json")
    parser.add_argument("findings", help="Path to findings.json")
    parser.add_argument(
        "--assign", action="store_true", help="Write computed batch numbers back to findings.json"
    )
    parser.add_argument(
        "--json", dest="as_json", action="store_true", help="Output machine-readable JSON"
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

    if not isinstance(findings, list) or not findings:
        print("ERROR: findings.json must be a non-empty JSON array", file=sys.stderr)
        sys.exit(1)

    batches = group_into_batches(findings)

    if args.as_json:
        output = [
            {
                "batch": i + 1,
                "description": batch_description(b, i + 1),
                "blocking": any(f.get("blocking") for f in b),
                "count": len(b),
                "ids": [f.get("id") for f in b],
            }
            for i, b in enumerate(batches)
        ]
        print(json.dumps(output, indent=2))
    else:
        print(render_plan(batches))

    if args.assign:
        assign_batches(findings_path, batches)


if __name__ == "__main__":
    main()
