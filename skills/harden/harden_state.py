"""
harden_state.py — manages harden-state.json (co-located with findings.json)

harden-state.json records audit results and batch filing progress so that
the notification handler and /harden resume can pick up where the audit left off.
"""
import json
import os
import tempfile
from datetime import date
from pathlib import Path


def write_state(state_path: Path, state: dict) -> None:
    """Write state atomically (tmp file + rename)."""
    dir_ = state_path.parent
    fd, tmp = tempfile.mkstemp(dir=dir_, prefix=".harden-state-tmp-")
    try:
        with os.fdopen(fd, "w") as fh:
            json.dump(state, fh, indent=2)
            fh.write("\n")
        os.replace(tmp, state_path)
    except Exception:
        try:
            os.unlink(tmp)
        except OSError:
            pass
        raise


def read_state(state_path: Path) -> dict | None:
    """Read state file. Returns None if file doesn't exist."""
    if not state_path.exists():
        return None
    return json.loads(state_path.read_text())


def build_initial_state(
    project: str,
    target: str,
    repo: str,
    grade: str,
    token_usage: int,
    findings_file: str,
    batches: dict[str, dict],
) -> dict:
    """Build the initial state dict from audit results.

    Returns:
        {
          "project": project,
          "target": target,
          "repo": repo,
          "date": today's date as YYYY-MM-DD,
          "grade": grade,
          "token_usage": token_usage,
          "findings_file": findings_file,
          "batches": {
            "1": {"status": "pending", "description": "...", "count": N, "issues": []},
            ...
          }
        }
    Note: batch keys are strings in JSON.
    """
    return {
        "project": project,
        "target": target,
        "repo": repo,
        "date": date.today().isoformat(),
        "grade": grade,
        "token_usage": token_usage,
        "findings_file": findings_file,
        "batches": batches,
    }


def update_batch_state(state_path: Path, batch_num: int, finding_id: str, url: str) -> None:
    """Append a filed issue to the batch in harden-state.json. No-op if state file missing."""
    state = read_state(state_path)
    if state is None:
        return
    batch = state["batches"].get(str(batch_num))
    if batch is None:
        return
    batch["issues"].append({"id": finding_id, "url": url})
    write_state(state_path, state)


def mark_batch_filed(state_path: Path, batch_num: int) -> None:
    """Set batch status to 'filed' in harden-state.json. No-op if state file missing."""
    state = read_state(state_path)
    if state is None:
        return
    batch = state["batches"].get(str(batch_num))
    if batch is None:
        return
    batch["status"] = "filed"
    write_state(state_path, state)


def batches_from_findings(findings: list[dict]) -> dict[str, dict]:
    """Build the batches dict from a findings list.

    Groups findings by batch number, counts them, uses first finding's scope
    as description. Returns dict keyed by string batch number.
    """
    grouped: dict[int, list[dict]] = {}
    for f in findings:
        batch_num = f.get("batch", 1)
        grouped.setdefault(batch_num, []).append(f)

    result: dict[str, dict] = {}
    for batch_num in sorted(grouped):
        batch_findings = grouped[batch_num]
        description = batch_findings[0].get("scope", f"Batch {batch_num}")
        result[str(batch_num)] = {
            "status": "pending",
            "description": description,
            "count": len(batch_findings),
            "issues": [],
        }
    return result
