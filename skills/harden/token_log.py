#!/usr/bin/env python3
"""Log per-run token usage for /harden audits."""
import argparse
import csv
from datetime import date
from pathlib import Path

FIELDNAMES = ["date", "project", "scope", "input_tokens", "output_tokens", "total_tokens"]


def main() -> None:
    parser = argparse.ArgumentParser(description="Log harden audit token usage")
    parser.add_argument("--project", required=True, help="Project name being audited")
    parser.add_argument("--scope", required=True, help="Scope name (e.g. Security, AI, Tests, All)")
    parser.add_argument("--input-tokens", type=int, required=True, dest="input_tokens")
    parser.add_argument("--output-tokens", type=int, required=True, dest="output_tokens")
    parser.add_argument(
        "--output-dir",
        help="Directory to write token log (default: current working directory)",
    )
    args = parser.parse_args()

    directory = Path(args.output_dir) if args.output_dir else Path.cwd()
    log_file = directory / f"harden_{date.today().isoformat()}_token_usage.csv"

    write_header = not log_file.exists()
    with open(log_file, "a", newline="") as f:
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
    print(f"Logged: {args.project} / {args.scope} — {total:,} tokens total")
    print(f"  Written to: {log_file}")


if __name__ == "__main__":
    main()
