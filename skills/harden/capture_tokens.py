#!/usr/bin/env python3
"""Capture token usage for a background harden audit from Claude Code session logs."""
import argparse
import csv
import json
from datetime import date
from pathlib import Path

LOG_FILE = Path(__file__).parent / "token_usage.csv"
FIELDNAMES = ["date", "project", "scope", "input_tokens", "output_tokens", "total_tokens"]


def get_project_dir() -> Path:
    """Compute Claude Code project directory from current working directory."""
    cwd = str(Path.cwd())
    project_hash = cwd.replace("/", "-").lstrip("-")
    return Path.home() / ".claude" / "projects" / project_hash


def find_agent_jsonl(project_dir: Path, marker_path: Path | None) -> Path | None:
    """Find the background agent JSONL — most recently modified after the start marker."""
    subagent_files = list(project_dir.glob("*/subagents/*.jsonl"))
    if not subagent_files:
        return None

    if marker_path and marker_path.exists():
        marker_mtime = marker_path.stat().st_mtime
        recent = [f for f in subagent_files if f.stat().st_mtime >= marker_mtime]
        if recent:
            return max(recent, key=lambda p: p.stat().st_mtime)

    # Fallback: most recently modified
    return max(subagent_files, key=lambda p: p.stat().st_mtime)


def sum_tokens(jsonl_path: Path) -> tuple[int, int]:
    """Sum input and output tokens across all entries in a JSONL file."""
    input_tokens = 0
    output_tokens = 0
    with open(jsonl_path) as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                entry = json.loads(line)
                usage = entry.get("message", {}).get("usage", {})
                input_tokens += usage.get("input_tokens", 0)
                input_tokens += usage.get("cache_creation_input_tokens", 0)
                input_tokens += usage.get("cache_read_input_tokens", 0)
                output_tokens += usage.get("output_tokens", 0)
            except (json.JSONDecodeError, KeyError):
                continue
    return input_tokens, output_tokens


def write_log(project: str, scope: str, input_tokens: int, output_tokens: int) -> None:
    write_header = not LOG_FILE.exists()
    with open(LOG_FILE, "a", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
        if write_header:
            writer.writeheader()
        writer.writerow({
            "date": date.today().isoformat(),
            "project": project,
            "scope": scope,
            "input_tokens": input_tokens,
            "output_tokens": output_tokens,
            "total_tokens": input_tokens + output_tokens,
        })


def main() -> None:
    parser = argparse.ArgumentParser(description="Capture token usage from background harden agent")
    parser.add_argument("--project", required=True, help="Project name being audited")
    parser.add_argument("--scope", default="All", help="Scope audited (e.g. All, Security, AI)")
    parser.add_argument("--marker", help="Path to start marker file (created before agent launch)")
    args = parser.parse_args()

    project_dir = get_project_dir()
    marker_path = Path(args.marker) if args.marker else None

    jsonl_path = find_agent_jsonl(project_dir, marker_path)
    if not jsonl_path:
        print(f"No agent JSONL found in {project_dir}")
        raise SystemExit(1)

    print(f"Reading tokens from: {jsonl_path}")
    input_tokens, output_tokens = sum_tokens(jsonl_path)

    write_log(args.project, args.scope, input_tokens, output_tokens)
    print(f"Logged: {args.project} / {args.scope} — {input_tokens + output_tokens:,} tokens total")
    print(f"  Input: {input_tokens:,}  Output: {output_tokens:,}")

    if marker_path and marker_path.exists():
        marker_path.unlink()


if __name__ == "__main__":
    main()
