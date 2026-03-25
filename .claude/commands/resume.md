---
description: View, edit, or tailor your resume for a job application
---

# /resume - Resume Editor

Two modes: **Apply** (tailor for a job posting) and **Edit** (manual tweaks).

## Instructions

Read and follow the skill definition at `skills/resume-editor/SKILL.md`.

The resume tool script is at `skills/resume-editor/scripts/resume_tool.py`.
Run it with: `uv run --with python-docx python3 skills/resume-editor/scripts/resume_tool.py <command>`

### Mode Detection

- **Apply mode** — User provides a job URL, says "apply to", "tailor resume for", etc.
  - Fetches posting, analyzes requirements, creates a tailored variant + cover letter
  - Files saved to `~/Resume/applications/{Company}/{Title}-{JobNumber}/`
  - Offers to log to applications.md + TWC after completion

- **Edit mode** — User says "edit", "add", "view", or just `/resume` without a URL
  - Manual edits to the base resume at `~/Resume/MatthewDruhl.docx`
  - Always backup before editing, verify page count after

### Key Rules
- **Base resume:** `~/Resume/MatthewDruhl.docx` (4-column skills table, 2-page max)
- **Apply mode edits the variant, never the base resume**
- **Variants** in `~/Resume/variants/` must be synced after any base resume change (Edit mode only)
- Each variant has its own format — preserve it (see SKILL.md for details)
- Never introduce hard page breaks — let content flow naturally
- Always backup to `~/Resume/archive/` before editing the base resume

If the user provided specific instructions (e.g., `/resume add cert XYZ`), parse those and proceed.
If no specific instructions and no job URL, ask what they'd like to do: view, add, edit, or remove.
