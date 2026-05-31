# MARVIN for Codex

Codex adapter for this repository. Keep this file thin: route behavior to canonical skills and shared context files.
Instruction ownership and drift controls live in `context/instruction-ownership.md`.

## Required Branch Rule

GitHub issues with `[codex-marvin-option-1]` in the title must be implemented only on branch:
`codex-marvin-option-1`.

## Startup Path

For "start MARVIN", `/marvin`, or equivalent startup requests:

1. Run from repo root: `python3 scripts/marvin_start.py`
2. Use startup packet output as source context.
3. Then follow `skills/marvin/SKILL.md` for briefing behavior and proactive actions.

Shared runtime-neutral context referenced by startup:

- `context/user-profile.md`
- `context/marvin-operating-rules.md`

## Command Routing

- `/marvin` -> `skills/marvin/SKILL.md`
- `/update` -> `skills/update/SKILL.md`
- `/end` -> `skills/end/SKILL.md`
- `/resume` -> `skills/resume-editor/SKILL.md`
- `/update-resume` -> `skills/update-resume/SKILL.md`
- `/harden` -> `skills/harden/SKILL.md`
- `/quiz` -> `skills/quiz/SKILL.md`
- `/pmp-quiz` -> `skills/pmp-quiz/SKILL.md`
- `/pmp-consume` -> `skills/pmp-quiz/pmp-consume-SKILL.md`
- `/pmp-intake` -> `skills/pmp-intake/SKILL.md`
- `/youtube-transcribe` -> `skills/youtube-transcribe/SKILL.md`
- `/commit` -> `skills/commit/SKILL.md`

If a command exists only in `.claude/commands/`, treat that file as reference and adapt it to Codex tools.

## Workflow Change Order

When MARVIN behavior changes:

Follow the update order in `context/instruction-ownership.md`: canonical skill first, shared context second, runtime adapters only for routing/runtime changes, then run `python3 scripts/check_instruction_drift.py`.

## Adapter Constraints

- Preserve existing Claude behavior.
- Do not edit `.claude/` files unless explicitly required by a separate issue.
- Keep external-action safeguards: confirm before send/post/calendar-modify/delete/publish.
