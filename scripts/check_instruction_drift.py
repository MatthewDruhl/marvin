#!/usr/bin/env python3
"""Check MARVIN runtime adapters for copied workflow procedures."""

from __future__ import annotations

import re
import sys
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
COMMAND_DIR = ROOT / ".claude" / "commands"
SKILLS_DIR = ROOT / "skills"

MAX_MAPPED_COMMAND_LINES = 35
MAX_ORDERED_LIST_ITEMS = 3
PROCEDURE_HEADING_RE = re.compile(
    r"^#{2,}\s+(process|mode detection|key rules|commit types|template|workflow|steps?)\b",
    re.IGNORECASE,
)
ORDERED_LIST_RE = re.compile(r"^\s*\d+\.\s+\S")


@dataclass(frozen=True)
class DriftResult:
    errors: list[str]
    warnings: list[str]


def meaningful_lines(text: str) -> list[str]:
    return [
        line
        for line in text.splitlines()
        if line.strip() and not line.strip().startswith("---") and not line.strip().startswith("description:")
    ]


def frontmatter_lines(text: str) -> list[str]:
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return []

    for index, line in enumerate(lines[1:], start=1):
        if line.strip() == "---":
            return lines[1:index]
    return []


def frontmatter_value(lines: list[str], key: str) -> str | None:
    prefix = f"{key}:"
    for line in lines:
        if line.strip().startswith(prefix):
            return line.split(":", 1)[1].strip().strip("\"'")
    return None


def normalize_command(value: str | None) -> str | None:
    if not value or value == "null":
        return None
    return value.removeprefix("/")


def discover_command_skills() -> tuple[dict[str, str], list[str]]:
    command_skills: dict[str, str] = {}
    errors: list[str] = []

    for skill_path in sorted(SKILLS_DIR.rglob("*SKILL*.md")):
        relative_skill = skill_path.relative_to(ROOT)
        if relative_skill.parts[1:] == ("_template", "SKILL.md"):
            continue

        metadata = frontmatter_lines(skill_path.read_text(encoding="utf-8"))
        command = normalize_command(frontmatter_value(metadata, "slash-command"))
        if command is None:
            continue

        existing = command_skills.get(command)
        if existing is not None:
            errors.append(f"{relative_skill}: duplicate slash-command /{command}; already owned by {existing}")
            continue

        command_skills[command] = relative_skill.as_posix()

    return command_skills, errors


def check_mapped_command(command_path: Path, skill_path: str) -> list[str]:
    errors: list[str] = []
    text = command_path.read_text(encoding="utf-8")
    relative_command = command_path.relative_to(ROOT)
    relative_skill = Path(skill_path)

    if not (ROOT / relative_skill).exists():
        errors.append(f"{relative_command}: mapped skill does not exist: {skill_path}")

    if skill_path not in text:
        errors.append(f"{relative_command}: must reference canonical skill {skill_path}")

    lines = meaningful_lines(text)
    if len(lines) > MAX_MAPPED_COMMAND_LINES:
        errors.append(
            f"{relative_command}: mapped command wrapper is {len(lines)} meaningful lines; "
            f"keep it <= {MAX_MAPPED_COMMAND_LINES}"
        )

    ordered_items = [line for line in lines if ORDERED_LIST_RE.match(line)]
    if len(ordered_items) > MAX_ORDERED_LIST_ITEMS:
        errors.append(
            f"{relative_command}: contains {len(ordered_items)} ordered-list items; "
            "move procedure steps to the canonical skill"
        )

    procedure_headings = [line.strip() for line in lines if PROCEDURE_HEADING_RE.match(line)]
    if procedure_headings:
        errors.append(
            f"{relative_command}: contains procedural heading(s): {', '.join(procedure_headings)}; "
            "move procedure content to the canonical skill"
        )

    return errors


def check_commands() -> DriftResult:
    errors: list[str] = []
    warnings: list[str] = []
    command_skills, discovery_errors = discover_command_skills()
    errors.extend(discovery_errors)

    command_paths = sorted(COMMAND_DIR.glob("*.md"))
    command_names = {path.stem for path in command_paths}

    for command_name, skill_path in sorted(command_skills.items()):
        command_path = COMMAND_DIR / f"{command_name}.md"
        if not command_path.exists():
            errors.append(f"{command_path.relative_to(ROOT)}: mapped command file is missing")
            continue
        errors.extend(check_mapped_command(command_path, skill_path))

    for command_path in command_paths:
        if command_path.stem in command_skills:
            continue
        lines = meaningful_lines(command_path.read_text(encoding="utf-8"))
        if len(lines) > MAX_MAPPED_COMMAND_LINES:
            warnings.append(
                f"{command_path.relative_to(ROOT)}: no canonical skill mapping and {len(lines)} meaningful lines; "
                "review manually or create a skill mapping"
            )

    for command_name in sorted(set(command_skills) - command_names):
        errors.append(f".claude/commands/{command_name}.md: mapped command file is missing")

    return DriftResult(errors=errors, warnings=warnings)


def main() -> int:
    result = check_commands()

    for warning in result.warnings:
        print(f"WARNING: {warning}", file=sys.stderr)

    if result.errors:
        for error in result.errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1

    print("OK: instruction adapter drift check passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
