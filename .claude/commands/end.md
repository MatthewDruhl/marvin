---
description: End MARVIN session - save context and state
---

# /end - End MARVIN Session

## Step 1: Load Context (parallel batch)

Read ALL of these in one parallel batch:
- `state/current.md`
- `state/habits.md`
- `state/goals.md`
- `sessions/{TODAY}.md` (if exists)

Get today's date with `date +%Y-%m-%d` in the same batch.

## Step 2: Summarize + Preview + Habit Check (single output)

Review the conversation and prepare ONE combined message with all three sections:

**Session Summary:**
- Topics discussed, decisions made, open threads, action items

**State Changes Preview:**
- Show proposed changes to `state/current.md` (new priorities, changed statuses, completed items, new open threads)
- If goal progress was made, show proposed `state/goals.md` updates
- If content was shipped, note it for `content/log.md`

**Habit Check:**
- List any habits from `state/habits.md` not yet logged today
- Ask: "Did you do any of these today?"

Present all three sections in one message. Wait for user response once.

## Step 3: Write Everything (parallel batch)

After user confirms, write ALL updates in one parallel batch:
- Append to `sessions/{TODAY}.md` (create with `# Session Log: {TODAY}` header if new)
- Edit `state/current.md` (keep under 50 lines — move details to `content/`)
- Update `state/habits.md` with reported completions
- Edit `state/goals.md` only if progress was discussed
- Append to `content/log.md` only if content was shipped

## Step 4: Conditional Cleanup (skip if nothing to do)

Only run each if applicable:
- **TWC PDFs:** Only if a `work-search-week-*.csv` in `content/jobs/TWC/` was modified today
- **Archive:** Only if more than 14 files in `sessions/` (move >2 weeks old to `sessions/archive/YYYY-MM/`)
- **Git commit:** Only if user requests it

## Notes
- Multiple `/end` calls in one day append to the same session file
- Keep summaries concise but complete for future context
- Log non-obvious decisions to `state/decisions.md`
