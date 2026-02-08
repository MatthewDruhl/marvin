---
description: End MARVIN session - save context and state
---

# /end - End MARVIN Session

Wrap up the current session and save context for continuity.

## Instructions

### 1. Summarize This Session
Review the conversation and extract:
- **Topics discussed** - What did we work on?
- **Decisions made** - What was decided?
- **Open threads** - What's unfinished or needs follow-up?
- **Action items** - What needs to happen next?

### 2. Update Session Log
Get today's date with `date +%Y-%m-%d`.

Append to `sessions/{TODAY}.md` (create if doesn't exist):
```markdown
## Session: {TIME}

### Topics
- {topic 1}
- {topic 2}

### Decisions
- {decision 1}

### Open Threads
- {thread 1}

### Next Actions
- {action 1}
```

If creating new file, add header: `# Session Log: {TODAY}`

### 3. Update State
Update `state/current.md` with:
- Any new priorities
- Changed project statuses
- New open threads
- Removed/completed items

Keep `current.md` under 50 lines. Move project details to `content/` files, not current.md.

### 4. Update Goals (if applicable)
If any goal-related progress was made this session, update `state/goals.md` tracking table with current status and "Last updated" date.

### 5. Generate TWC PDFs
See `skills/twc-pdf/SKILL.md` for instructions. Run:
```bash
cd content/jobs/TWC
for file in work-search-week-*.csv; do
    python3 fill_twc_pdf.py "$file" 2>/dev/null
done
```

If PDFs were generated, note: "TWC PDFs updated"

### 6. Archive Old Sessions
If there are more than 14 session files in `sessions/`, move files older than 2 weeks to `sessions/archive/YYYY-MM/`.

### 7. Confirm
Show a brief summary:
- What was logged
- Key items for next session
- State updated confirmation
- TWC PDFs status (if applicable)

Keep it concise.
