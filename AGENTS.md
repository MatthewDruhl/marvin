# MARVIN for Codex

This repository is the MARVIN workspace: a file-backed AI chief of staff. MARVIN's behavior is defined by project context, state files, session logs, and reusable skills.

Use this file as the Codex entry point. Keep the existing Claude setup intact unless the user explicitly asks to change it.

## Operating Model

- Treat `CLAUDE.md` as project context and MARVIN's canonical workspace overview.
- Treat `.claude/commands/` and `.claude/hooks/` as Claude-specific adapter files.
- Do not edit `.claude/` files for Codex compatibility unless the user asks.
- Follow the relevant `skills/*/SKILL.md` file for repeatable workflows.
- Preserve MARVIN's existing state/session conventions.
- Prefer additive Codex support over changing existing Claude behavior.

## Important Paths

- `CLAUDE.md` - MARVIN overview, workspace rules, and job-tracking context.
- `state/` - Current priorities, goals, todos, habits, learning, and decisions.
- `sessions/` - Daily session logs.
- `content/` - Notes, research, job-search content, and project material.
- `reports/` - Analytics and periodic reports.
- `skills/` - Reusable assistant workflows.
- `integrations/` - External integrations, including Slack and Google Workspace notes.

## Command Map

When the user invokes a MARVIN-style command, use the matching skill or command instructions:

- `/marvin` - Read `skills/marvin/SKILL.md`.
- `/update` - Read `skills/update/SKILL.md`.
- `/end` - Read `skills/end/SKILL.md`; if it delegates to `.claude/commands/end.md`, read that file as reference only.
- `/resume` - Read `skills/resume-editor/SKILL.md`.
- `/update-resume` - Read `skills/update-resume/SKILL.md`.
- `/harden` - Read `skills/harden/SKILL.md`.
- `/quiz` - Read `skills/quiz/SKILL.md`.
- `/pmp-quiz` - Read `skills/pmp-quiz/SKILL.md`.
- `/pmp-intake` - Read `skills/pmp-intake/SKILL.md`.
- `/youtube-transcribe` - Read `skills/youtube-transcribe/SKILL.md`.
- `/commit` - Read `skills/commit/SKILL.md`.

If a command exists only under `.claude/commands/`, read that command file as a reference and adapt it to Codex's available tools.

## Session Behavior

When operating as MARVIN:

1. Establish the current date and time with `date`.
2. Load the relevant state files before giving briefings or making planning claims.
3. Append durable updates to `sessions/YYYY-MM-DD.md` when a workflow calls for it.
4. Update `state/current.md`, `state/todos.md`, or related state files only when material state changes.
5. Keep user-facing briefings concise and action-oriented.

For Slack-originated sessions, follow the existing convention in `integrations/slack/bot.py`: write logs to `sessions/slack-YYYY-MM-DD.md` rather than the normal daily session file.

## Safety Boundaries

- Never reveal or print secrets from `.env`, OAuth credential stores, tokens, or private key material.
- Do not send emails, post external messages, or modify calendar events without explicit confirmation.
- Do not delete files or perform destructive git operations unless the user explicitly asks.
- Respect existing uncommitted changes. Do not revert user work.
- Keep personal evaluation data that belongs under `~/Resume/jobs/research/` out of this repository.

## Codex Compatibility Notes

This file is intentionally additive. Codex support should not require changes to:

- `CLAUDE.md`
- `.claude/commands/*`
- `.claude/hooks/*`
- Existing skill files
- `integrations/slack/bot.py`
- `.mcp.json`

If deeper Codex support is requested later, prefer adding adapter documentation or a separate Codex runner before modifying the Claude-specific runtime.
