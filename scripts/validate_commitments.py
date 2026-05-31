#!/usr/bin/env python3
"""Validate MARVIN's structured commitments tracker."""

from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import date
from pathlib import Path
from typing import Any

ALLOWED_STATUSES = {"active", "waiting", "blocked", "done", "dropped"}
REQUIRED_FIELDS = {
    "id",
    "title",
    "status",
    "owner",
    "project",
    "source",
    "created",
    "due",
    "review_after",
    "last_touched",
    "next_action",
    "notes",
}
DATE_FIELDS = ("created", "due", "review_after", "last_touched")
ID_RE = re.compile(r"^commit-\d{4}-\d{2}-\d{2}-\d{3}$")


def parse_iso_date(value: Any, field: str, commitment_id: str, errors: list[str]) -> None:
    if value is None:
        if field == "due":
            return
        errors.append(f"{commitment_id}: {field} is required and cannot be null")
        return
    if not isinstance(value, str):
        errors.append(f"{commitment_id}: {field} must be an ISO date string or null")
        return
    try:
        date.fromisoformat(value)
    except ValueError:
        errors.append(f"{commitment_id}: {field} must use YYYY-MM-DD")


def validate_commitment(item: Any, index: int, seen_ids: set[str], errors: list[str]) -> None:
    label = f"commitments[{index}]"
    if not isinstance(item, dict):
        errors.append(f"{label}: must be an object")
        return

    missing = sorted(REQUIRED_FIELDS - set(item))
    if missing:
        errors.append(f"{label}: missing required fields: {', '.join(missing)}")

    commitment_id = item.get("id", label)
    if not isinstance(commitment_id, str) or not ID_RE.match(commitment_id):
        errors.append(f"{label}: id must match commit-YYYY-MM-DD-NNN")
    elif commitment_id in seen_ids:
        errors.append(f"{commitment_id}: duplicate id")
    else:
        seen_ids.add(commitment_id)

    status = item.get("status")
    if status not in ALLOWED_STATUSES:
        errors.append(f"{commitment_id}: status must be one of {', '.join(sorted(ALLOWED_STATUSES))}")

    for field in ("title", "owner", "project", "next_action", "notes"):
        value = item.get(field)
        if not isinstance(value, str) or not value.strip():
            errors.append(f"{commitment_id}: {field} must be a non-empty string")

    source = item.get("source")
    if not isinstance(source, dict):
        errors.append(f"{commitment_id}: source must be an object")
    else:
        for field in ("type", "path"):
            value = source.get(field)
            if not isinstance(value, str) or not value.strip():
                errors.append(f"{commitment_id}: source.{field} must be a non-empty string")

    for field in DATE_FIELDS:
        parse_iso_date(item.get(field), field, commitment_id, errors)


def validate(path: Path) -> list[str]:
    errors: list[str] = []
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        return [f"{path}: file not found"]
    except json.JSONDecodeError as exc:
        return [f"{path}: invalid JSON: {exc}"]

    if not isinstance(data, dict):
        return ["root must be an object"]

    if data.get("version") != 1:
        errors.append("version must be 1")

    parse_iso_date(data.get("last_updated"), "last_updated", "root", errors)

    commitments = data.get("commitments")
    if not isinstance(commitments, list):
        errors.append("commitments must be a list")
        return errors

    seen_ids: set[str] = set()
    for index, item in enumerate(commitments):
        validate_commitment(item, index, seen_ids, errors)
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate state/commitments.json")
    parser.add_argument(
        "path",
        nargs="?",
        default="state/commitments.json",
        help="Path to commitments JSON file",
    )
    args = parser.parse_args()

    errors = validate(Path(args.path))
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1

    print(f"OK: {args.path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
