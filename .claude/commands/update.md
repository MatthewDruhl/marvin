---
description: Quick checkpoint without ending session
---

# /update - Quick Context Checkpoint

Lightweight save without ending the session. Use frequently to preserve context.

## Instructions

### 1. Identify What Changed
Quickly scan the recent conversation for:
- Topics worked on
- Decisions made
- Files created/modified
- Any state changes needed

Keep it brief. No full summary needed.

### 2. Append to Session Log
Get today's date: `date +%Y-%m-%d`

Append to `sessions/{TODAY}.md`:
```markdown
## Update: {TIME}
- {what was worked on, 1-3 bullets}
```

If file doesn't exist, create with header: `# Session Log: {TODAY}`

### 3. Update State (if needed)
Only update `state/current.md` if something actually changed:
- New open thread
- Completed item
- Changed priority
- New task discovered

Keep `current.md` under 50 lines. Move project details to `content/` files, not current.md.

Skip if nothing material changed.

### 4. Generate TWC PDFs (if TWC files changed)
If any TWC CSV files were modified, see `skills/twc-pdf/SKILL.md` and run:
```bash
cd content/jobs/TWC
for file in work-search-week-*.csv; do
    python3 fill_twc_pdf.py "$file" 2>/dev/null
done
```

Only mention if PDFs were updated.

### 5. Confirm (minimal)
One line: "Checkpointed: {brief description}"

No summary. No "next actions" list. Just confirm the save.
