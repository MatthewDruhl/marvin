# MARVIN for Codex

Codex adapter for this repository. Keep this file thin: route behavior to canonical skills and shared context files.

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
- `/pmp-intake` -> `skills/pmp-intake/SKILL.md`
- `/youtube-transcribe` -> `skills/youtube-transcribe/SKILL.md`
- `/commit` -> `skills/commit/SKILL.md`

If a command exists only in `.claude/commands/`, treat that file as reference and adapt it to Codex tools.

## Workflow Change Order

When MARVIN behavior changes:

1. Update canonical `skills/*/SKILL.md` first.
2. Update shared context files in `context/*` for runtime-neutral changes.
3. Update runtime adapters only if routing changed:
   - Claude adapter files: `.claude/commands/*`
   - Codex adapter file: `AGENTS.md`
4. Add a session log note when behavior changes materially.

## Adapter Constraints

- Preserve existing Claude behavior.
- Do not edit `.claude/` files unless explicitly required by a separate issue.
- Keep external-action safeguards: confirm before send/post/calendar-modify/delete/publish.
