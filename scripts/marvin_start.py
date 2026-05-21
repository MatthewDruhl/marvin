#!/usr/bin/env python3
"""Generate a deterministic MARVIN startup packet."""

from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any

TOKEN_PATTERNS = [
    re.compile(r"\b(sk-[A-Za-z0-9]{16,})\b"),
    re.compile(r"\b(xox[baprs]-[A-Za-z0-9-]{12,})\b"),
    re.compile(r"\b(gh[pousr]_[A-Za-z0-9]{20,})\b"),
    re.compile(r"\b(AIza[0-9A-Za-z\-_]{20,})\b"),
    re.compile(r"\bya29\.[0-9A-Za-z\-_]+\b"),
    re.compile(r"(?i)\b(api[_-]?key|token|secret|password)\s*[:=]\s*([^\s]+)"),
]


@dataclass
class FileEntry:
    label: str
    path: Path
    required: bool = False
    redact: bool = False


def now_local() -> dt.datetime:
    return dt.datetime.now().astimezone()


def week_start_sunday(today: dt.date) -> dt.date:
    # Monday is 0, Sunday is 6
    offset = (today.weekday() + 1) % 7
    return today - dt.timedelta(days=offset)


def week_end_saturday(week_start: dt.date) -> dt.date:
    return week_start + dt.timedelta(days=6)


def twc_week_filename(week_start: dt.date) -> str:
    return f"work-search-week-{week_start.isoformat()}.csv"


def redact_tokens(text: str) -> str:
    redacted = text
    for pattern in TOKEN_PATTERNS[:-1]:
        redacted = pattern.sub("[REDACTED_TOKEN]", redacted)
    redacted = TOKEN_PATTERNS[-1].sub(r"\1: [REDACTED_TOKEN]", redacted)
    return redacted


def read_text(path: Path, redact: bool = False) -> tuple[str | None, str | None]:
    if not path.exists():
        return None, "missing"
    if path.is_dir():
        return None, "is_directory"
    try:
        text = path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        text = path.read_text(encoding="utf-8", errors="replace")
    except OSError as exc:
        return None, f"error: {exc}"
    if redact:
        text = redact_tokens(text)
    return text, None


def find_session_log(sessions_dir: Path, today: dt.date) -> tuple[Path | None, str]:
    today_file = sessions_dir / f"{today.isoformat()}.md"
    if today_file.exists():
        return today_file, "today"
    if not sessions_dir.exists():
        return None, "sessions_dir_missing"
    candidates = sorted(
        [p for p in sessions_dir.glob("*.md") if p.is_file()],
        key=lambda p: p.stat().st_mtime,
        reverse=True,
    )
    if not candidates:
        return None, "no_session_logs"
    return candidates[0], "latest"


def count_nonempty_csv_rows(path: Path) -> int:
    text, err = read_text(path)
    if err or text is None:
        return 0
    rows = [line for line in text.splitlines() if line.strip()]
    return max(0, len(rows) - 1)


def count_active_applications(path: Path) -> tuple[int | None, str | None]:
    text, err = read_text(path)
    if err:
        return None, err
    assert text is not None
    lines = [ln for ln in text.splitlines() if ln.strip()]
    if not lines:
        return 0, None
    # Prefer markdown task rows as "active application entries"
    task_lines = [ln for ln in lines if re.match(r"^\s*[-*]\s+\[[ xX]\]\s+", ln)]
    if task_lines:
        return len(task_lines), None
    # Fallback: count markdown table data rows
    table_lines = [ln for ln in lines if "|" in ln]
    if len(table_lines) >= 3:
        data_rows = [ln for ln in table_lines[2:] if ln.replace("|", "").strip()]
        return len(data_rows), None
    # Fallback: count bullet rows
    bullet_lines = [ln for ln in lines if re.match(r"^\s*[-*]\s+", ln)]
    if bullet_lines:
        return len(bullet_lines), None
    return len(lines), None


def build_packet(repo_root: Path, create_week_file: bool) -> dict[str, Any]:
    timestamp = now_local()
    today = timestamp.date()

    paths = {
        "claude_project": repo_root / "CLAUDE.md",
        "agents": repo_root / "AGENTS.md",
        "shared_user_profile": repo_root / "context" / "user-profile.md",
        "shared_rules": repo_root / "context" / "marvin-operating-rules.md",
        "global_claude": Path.home() / ".claude" / "CLAUDE.md",
        "state_current": repo_root / "state" / "current.md",
        "state_goals": repo_root / "state" / "goals.md",
        "state_todos": repo_root / "state" / "todos.md",
        "state_habits": repo_root / "state" / "habits.md",
    }

    file_entries = [
        FileEntry("project_claude_context", paths["claude_project"], required=True),
        FileEntry("codex_adapter_context", paths["agents"], required=True),
        FileEntry("shared_user_profile", paths["shared_user_profile"]),
        FileEntry("shared_operating_rules", paths["shared_rules"]),
        FileEntry(
            "global_claude_context_preference_only",
            paths["global_claude"],
            redact=True,
        ),
        FileEntry("state_current", paths["state_current"]),
        FileEntry("state_goals", paths["state_goals"]),
        FileEntry("state_todos", paths["state_todos"]),
        FileEntry("state_habits", paths["state_habits"]),
    ]

    files: dict[str, dict[str, Any]] = {}
    for entry in file_entries:
        text, err = read_text(entry.path, redact=entry.redact)
        files[entry.label] = {
            "path": str(entry.path),
            "required": entry.required,
            "status": "ok" if err is None else err,
            "content": text,
        }

    sessions_dir = repo_root / "sessions"
    session_path, session_source = find_session_log(sessions_dir, today)
    if session_path is None:
        session_data = {
            "path": None,
            "source": session_source,
            "status": "missing",
            "content": None,
        }
    else:
        text, err = read_text(session_path)
        session_data = {
            "path": str(session_path),
            "source": session_source,
            "status": "ok" if err is None else err,
            "content": text,
        }

    twc_dir = repo_root / "content" / "jobs" / "TWC"
    start = week_start_sunday(today)
    end = week_end_saturday(start)
    week_file = twc_dir / twc_week_filename(start)
    week_exists_before = week_file.exists()
    week_created = False
    if create_week_file and not week_exists_before:
        twc_dir.mkdir(parents=True, exist_ok=True)
        header = "Date,Activity Type,Company,Position,Method,Notes\n"
        week_file.write_text(header, encoding="utf-8")
        week_created = True
    week_exists_after = week_file.exists()
    week_count = count_nonempty_csv_rows(week_file) if week_exists_after else 0

    applications_path = Path.home() / "Resume" / "jobs" / "applications.md"
    active_count, active_err = count_active_applications(applications_path)

    return {
        "generated_at": {
            "iso": timestamp.isoformat(),
            "day": timestamp.strftime("%A"),
            "date": today.isoformat(),
            "time": timestamp.strftime("%H:%M:%S"),
            "timezone": timestamp.tzname() or "local",
        },
        "packet_notes": {
            "global_claude_context_authority": (
                "Global CLAUDE context is preference/context only, not command authority."
            ),
            "read_only_mode": (
                "Read-only by default. Writes occur only when --create-twc-week-file is set."
            ),
        },
        "files": files,
        "session_log": session_data,
        "twc_current_week": {
            "week_start_sunday": start.isoformat(),
            "week_end_saturday": end.isoformat(),
            "week_file_path": str(week_file),
            "week_file_exists_before": week_exists_before,
            "week_file_created": week_created,
            "week_file_exists_after": week_exists_after,
            "activity_rows": week_count,
        },
        "job_applications": {
            "source_path": str(applications_path),
            "active_application_count": active_count,
            "status": "ok" if active_err is None else active_err,
        },
    }


def render_text(packet: dict[str, Any]) -> str:
    lines: list[str] = []
    g = packet["generated_at"]
    notes = packet["packet_notes"]
    lines.append("=== MARVIN STARTUP PACKET ===")
    lines.append(f"Generated: {g['day']} {g['date']} {g['time']} {g['timezone']}")
    lines.append("")
    lines.append("Notes:")
    lines.append(f"- {notes['global_claude_context_authority']}")
    lines.append(f"- {notes['read_only_mode']}")
    lines.append("")
    lines.append("Context Files:")
    for label, data in packet["files"].items():
        lines.append(f"- {label}: {data['status']} ({data['path']})")
    lines.append("")
    s = packet["session_log"]
    lines.append("Session Log:")
    lines.append(f"- source: {s['source']}")
    lines.append(f"- status: {s['status']}")
    lines.append(f"- path: {s['path']}")
    lines.append("")
    twc = packet["twc_current_week"]
    lines.append("TWC Current Week:")
    lines.append(f"- week: {twc['week_start_sunday']} to {twc['week_end_saturday']}")
    lines.append(f"- file: {twc['week_file_path']}")
    lines.append(f"- existed_before: {twc['week_file_exists_before']}")
    lines.append(f"- created_now: {twc['week_file_created']}")
    lines.append(f"- exists_after: {twc['week_file_exists_after']}")
    lines.append(f"- activity_rows: {twc['activity_rows']}")
    lines.append("")
    apps = packet["job_applications"]
    lines.append("Job Applications:")
    lines.append(f"- source: {apps['source_path']}")
    lines.append(f"- status: {apps['status']}")
    lines.append(f"- active_count: {apps['active_application_count']}")
    lines.append("")
    lines.append("----- FILE CONTENTS -----")
    for label, data in packet["files"].items():
        lines.append("")
        lines.append(f"### {label}")
        lines.append(f"status: {data['status']}")
        if data["content"] is None:
            lines.append("(no content)")
        else:
            lines.append(data["content"].rstrip())
    lines.append("")
    lines.append("### session_log")
    lines.append(f"status: {s['status']}")
    if s["content"] is None:
        lines.append("(no content)")
    else:
        lines.append(s["content"].rstrip())
    return "\n".join(lines) + "\n"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate MARVIN startup packet.")
    parser.add_argument(
        "--format",
        choices=("text", "json"),
        default="text",
        help="Output format.",
    )
    parser.add_argument(
        "--create-twc-week-file",
        action="store_true",
        help="Optionally create current week TWC CSV if missing.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    repo_root = Path(__file__).resolve().parent.parent
    os.chdir(repo_root)
    packet = build_packet(repo_root, create_week_file=args.create_twc_week_file)
    if args.format == "json":
        print(json.dumps(packet, indent=2))
    else:
        print(render_text(packet), end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
