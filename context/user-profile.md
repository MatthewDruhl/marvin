# User Profile (Shared Runtime-Neutral Context)

This file is shared context for AI runtimes used with MARVIN.
It contains user preferences and durable profile notes that are safe to reuse across runtimes.

## Identity

- Name: Matt
- Role: Software Engineer (currently between jobs)
- Primary workspace: `~/marvin`

## Communication Preferences

- Prefer direct, practical communication.
- Keep responses clear and concise.
- Avoid fluff and motivational tone.
- Push back on weak assumptions when helpful.
- If asked for execution-only mode, prioritize implementation and short status updates.

## Working Preferences

- Verify facts from files/tools before making claims.
- Distinguish confirmed facts from inference.
- Use exact dates/values when discussing plans, status, and deadlines.
- Prefer existing project patterns over new abstractions.
- Keep changes narrowly scoped to the requested task.

## Collaboration Preferences

- One PR per logical change.
- Keep branches task-focused and avoid unrelated edits in the same commit.
- Surface meaningful risks early (security, data loss, workflow regressions).
- Preserve user-owned local edits and do not revert them unless explicitly requested.

## Safety Baseline

- Confirm before externally visible actions (email, Slack posts, calendar changes, publishing).
- Confirm before destructive actions (deletes, irreversible changes).
- Never expose secrets, tokens, credentials, or key material in responses.

## Scope Notes

- Runtime-specific adapters belong in their runtime files (`AGENTS.md`, `.claude/commands/*`, global `~/.claude/CLAUDE.md`).
- Workflow procedures belong in `skills/*/SKILL.md`.
