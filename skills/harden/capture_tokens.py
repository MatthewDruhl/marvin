#!/usr/bin/env python3
"""Capture token usage for a background harden audit from Claude Code session logs.

NOTE: This module reads Claude Code session JSONL files which contain full conversation
history, potentially including PII or sensitive data. Token counts are the only values
used; no conversation content is retained.
"""
import argparse
import csv
import json
import time
from datetime import date
from pathlib import Path

FIELDNAMES = ["date", "project", "scope", "input_tokens", "output_tokens", "total_tokens"]


def log_file_path(output_dir: str | None = None) -> Path:
    """Return the token log path: harden_{date}_token_usage.csv in output_dir (default: cwd)."""
    directory = Path(output_dir) if output_dir else Path.cwd()
    return directory / f"harden_{date.today().isoformat()}_token_usage.csv"

# Lookback window for time-based JSONL search (seconds). Covers long audits.
RECENT_WINDOW_SECS = 7200  # 2 hours


def get_project_dir(override: str | None = None) -> Path:
    """Compute Claude Code project directory.

    If override is provided, use it directly (allows caller to specify the
    project dir when the agent's cwd differs from the audited project path).
    Otherwise fall back to computing from cwd.
    """
    if override:
        return Path(override)
    cwd = str(Path.cwd())
    project_hash = cwd.replace("/", "-").lstrip("-")
    return Path.home() / ".claude" / "projects" / project_hash


def find_agent_jsonl(
    project_dir: Path,
    marker_path: Path | None,
    verbose: bool = False,
) -> Path | None:
    """Find the background agent JSONL — newest file created within the lookback window.

    Strategy (in order):
    1. If a marker exists, use files modified after the marker mtime.
    2. Fall back to files modified within RECENT_WINDOW_SECS of now.
    3. Last resort: most recently modified file across all subagents.
    """
    subagent_files = list(project_dir.glob("*/subagents/*.jsonl"))

    if verbose:
        print(f"[verbose] project_dir: {project_dir}")
        print(f"[verbose] subagent files found: {len(subagent_files)}")
        for f in subagent_files:
            print(f"  {f}  mtime={f.stat().st_mtime:.0f}")
        if marker_path:
            if marker_path.exists():
                print(f"[verbose] marker mtime: {marker_path.stat().st_mtime:.0f}")
            else:
                print(f"[verbose] marker not found: {marker_path}")

    if not subagent_files:
        return None

    # Strategy 1: marker-relative filter
    if marker_path and marker_path.exists():
        marker_mtime = marker_path.stat().st_mtime
        recent = [f for f in subagent_files if f.stat().st_mtime >= marker_mtime]
        if verbose:
            print(f"[verbose] files after marker: {len(recent)}")
        if recent:
            return max(recent, key=lambda p: p.stat().st_mtime)

    # Strategy 2: time-based window (handles race condition where marker is gone)
    cutoff = time.time() - RECENT_WINDOW_SECS
    recent = [f for f in subagent_files if f.stat().st_mtime >= cutoff]
    if verbose:
        print(f"[verbose] files within {RECENT_WINDOW_SECS}s window: {len(recent)}")
    if recent:
        return max(recent, key=lambda p: p.stat().st_mtime)

    # Strategy 3: absolute fallback
    if verbose:
        print("[verbose] falling back to most recently modified file")
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
                # Only token fields are extracted; conversation content is discarded
                entry = json.loads(line)
                usage = entry.get("message", {}).get("usage", {})
                input_tokens += usage.get("input_tokens", 0)
                input_tokens += usage.get("cache_creation_input_tokens", 0)
                input_tokens += usage.get("cache_read_input_tokens", 0)
                output_tokens += usage.get("output_tokens", 0)
            except (json.JSONDecodeError, KeyError):
                continue
    return input_tokens, output_tokens


def write_log(
    project: str, scope: str, input_tokens: int, output_tokens: int, log_file: Path
) -> None:
    write_header = not log_file.exists()
    with open(log_file, "a", newline="") as f:
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
    parser.add_argument(
        "--project-dir",
        help="Explicit Claude project directory path (overrides cwd-based computation)",
    )
    parser.add_argument(
        "--output-dir",
        help="Directory to write token log (default: current working directory)",
    )
    parser.add_argument(
        "--verbose", action="store_true",
        help="Print debug info: project_dir, found JSONLs, mtime values",
    )
    args = parser.parse_args()

    project_dir = get_project_dir(args.project_dir)
    marker_path = Path(args.marker) if args.marker else None

    jsonl_path = find_agent_jsonl(project_dir, marker_path, verbose=args.verbose)
    if not jsonl_path:
        print(f"No agent JSONL found in {project_dir}")
        raise SystemExit(1)

    print(f"Reading tokens from: {jsonl_path}")
    input_tokens, output_tokens = sum_tokens(jsonl_path)

    log_file = log_file_path(args.output_dir)
    write_log(args.project, args.scope, input_tokens, output_tokens, log_file)
    print(f"Logged: {args.project} / {args.scope} — {input_tokens + output_tokens:,} tokens total")
    print(f"  Input: {input_tokens:,}  Output: {output_tokens:,}")
    print(f"  Written to: {log_file}")

    if marker_path and marker_path.exists() and str(marker_path).startswith("/tmp/"):
        marker_path.unlink()


if __name__ == "__main__":
    main()
