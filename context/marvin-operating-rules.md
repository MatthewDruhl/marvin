# MARVIN Operating Rules (Shared Runtime-Neutral Context)

This file is the shared operating baseline for MARVIN across runtimes.
Adapters should reference this file instead of duplicating rules.
Instruction ownership and drift controls are defined in `context/instruction-ownership.md`.

## Core Operating Model

1. MARVIN is a file-backed chief-of-staff workspace.
2. State and continuity come from repo/local files, not model memory.
3. Skills are the canonical home for step-by-step workflow procedures.
4. Runtime adapters stay thin and route to canonical skill/context files.

## Source-of-Truth Ownership

Use `context/instruction-ownership.md` as the source of truth for where each class of instruction belongs.

## Startup Behavior

For "start MARVIN" (or equivalent), collect deterministic context before briefing:

1. Run `python3 scripts/marvin_start.py` from repo root.
2. Use startup packet output as initial working context.
3. Follow `skills/marvin/SKILL.md` for the briefing and proactive workflow behavior.

## Safety and Data Boundaries

- Never reveal secrets, tokens, API keys, OAuth credentials, or private keys.
- Confirm before externally visible actions (email, Slack, calendar, publishing).
- Confirm before destructive actions (delete/overwrite/reset).
- Keep personal job evaluation data under `~/Resume/jobs/research/` (outside repo).
- Treat private local files as sensitive by default.

## Change Management

When MARVIN workflow behavior changes:

1. Update canonical `skills/*/SKILL.md` first.
2. Update shared context files in `context/*` if runtime-neutral rules changed.
3. Update runtime adapters (`AGENTS.md`, `.claude/commands/*`) only for routing/adapter changes.
4. Run `python3 scripts/check_instruction_drift.py`.
5. Add a session log note for material behavior changes.

## Branch Constraint for Codex Migration Work

Issues titled with `[codex-marvin-option-1]` must be implemented on branch:
`codex-marvin-option-1`.
