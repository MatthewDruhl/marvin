---
name: end
description: End MARVIN session, save context, update state.
license: MIT
compatibility: marvin
metadata:
  marvin-category: session
  user-invocable: true
  slash-command: /end
  model: default
  proactive: false
---

# Session End Skill

End a MARVIN session by summarizing the work, previewing state changes, checking habits, and saving confirmed updates.

## When to Use

- User types `/end`
- User asks to end, wrap up, or close a MARVIN session
- User asks to save session context and stop

## Process

### Step 1: Load Context

Read these in parallel where possible:

1. `state/current.md`
2. `state/habits.md`
3. `state/goals.md`
4. `state/commitments.json`
5. `sessions/{TODAY}.md` if it exists

Get today's date with:

```bash
date +%Y-%m-%d
```

Use that value for `TODAY` and session log paths. If today's session log does not exist, prepare to create `sessions/{TODAY}.md`.

### Step 2: Summarize, Preview, and Check Habits

Review the conversation and prepare one combined message with these sections:

**Session Summary**
- Topics discussed
- Decisions made
- Open threads
- Action items

**State Changes Preview**
- Proposed changes to `state/current.md`, including new priorities, changed statuses, completed items, and new open threads
- Proposed `state/goals.md` updates only if goal progress was made
- Proposed `state/commitments.json` updates for new, resolved, blocked, waiting, stale, or changed commitments
- Proposed `content/log.md` entry only if content was shipped

**Habit Check**
- List habits from `state/habits.md` that are not yet logged for `TODAY`
- Ask: "Did you do any of these today?"

Present all three sections in one message and wait for the user's response once before writing.

### Step 3: Write Confirmed Updates

After the user confirms, write all applicable updates:

1. Append the session summary to `sessions/{TODAY}.md`.
   - If the file does not exist, create it with `# Session Log: {TODAY}`.
2. Edit `state/current.md` for material state changes.
   - Keep it under 50 lines.
   - Move details to `content/` when needed.
3. Update `state/habits.md` with any reported habit completions.
4. Edit `state/commitments.json` for confirmed commitment changes.
   - Use stable IDs (`commit-YYYY-MM-DD-NNN`).
   - Use ISO dates.
   - Do not add new active commitments to `state/todos.md`; that file is legacy/reference.
5. Edit `state/goals.md` only if goal progress was discussed.
6. Append to `content/log.md` only if content was shipped.

### Step 4: Conditional Cleanup

Only run each cleanup when applicable:

- **TWC PDFs:** If a `work-search-week-*.csv` file in `content/jobs/TWC/` was modified today, regenerate or update the relevant PDF artifacts according to the TWC workflow.
- **Archive:** If there are more than 14 files in `sessions/`, move session logs older than 2 weeks to `sessions/archive/YYYY-MM/`.
- **Git commit:** Only commit if the user asks for a commit.

## Output Rules

- Keep summaries concise but complete enough for future context.
- Multiple `/end` calls in one day append to the same session file.
- Log non-obvious decisions to `state/decisions.md`.
- Do not write state changes before the user confirms the preview.
