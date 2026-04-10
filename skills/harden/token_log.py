#!/usr/bin/env python3
"""Log per-run token usage for /harden audits."""
import argparse
import csv
from datetime import date
from pathlib import Path

LOG_FILE = Path.home() / ".claude" / "harden" / "token_usage.csv"
FIELDNAMES = ["date", "project", "scope", "input_tokens", "output_tokens", "total_tokens"]


def main() -> None:
    parser = argparse.ArgumentParser(description="Log harden audit token usage")
    parser.add_argument("--project", required=True, help="Project name being audited")
    parser.add_argument("--scope", required=True, help="Scope name (e.g. Security, AI, Tests, All)")
    parser.add_argument("--input-tokens", type=int, required=True, dest="input_tokens")
    parser.add_argument("--output-tokens", type=int, required=True, dest="output_tokens")
    args = parser.parse_args()

    LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
    write_header = not LOG_FILE.exists()
    with open(LOG_FILE, "a", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
        if write_header:
            writer.writeheader()
        total = args.input_tokens + args.output_tokens
        writer.writerow({
            "date": date.today().isoformat(),
            "project": args.project,
            "scope": args.scope,
            "input_tokens": args.input_tokens,
            "output_tokens": args.output_tokens,
            "total_tokens": total,
        })
    print(f"Logged: {args.project} / {args.scope} — {args.input_tokens + args.output_tokens:,} tokens total")


if __name__ == "__main__":
    main()
