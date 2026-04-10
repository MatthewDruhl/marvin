#!/usr/bin/env python3
"""Log per-run token usage for /harden audits."""
import argparse
import csv
import os
from datetime import date

LOG_FILE = os.path.join(os.path.dirname(__file__), "token_usage.csv")
FIELDNAMES = ["date", "project", "scope", "input_tokens", "output_tokens", "total_tokens"]


def main() -> None:
    parser = argparse.ArgumentParser(description="Log harden audit token usage")
    parser.add_argument("--project", required=True, help="Project name being audited")
    parser.add_argument("--scope", required=True, help="Scope name (e.g. Security, AI, Tests, All)")
    parser.add_argument("--input-tokens", type=int, required=True, dest="input_tokens")
    parser.add_argument("--output-tokens", type=int, required=True, dest="output_tokens")
    args = parser.parse_args()

    write_header = not os.path.exists(LOG_FILE)
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
