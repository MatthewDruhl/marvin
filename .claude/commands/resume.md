---
description: View or edit your resume
---

# /resume - Resume Editor

Read, edit, and manage your Word resume.

## Instructions

Read and follow the skill definition at `skills/resume-editor/SKILL.md`.

The resume tool script is at `skills/resume-editor/scripts/resume_tool.py`.
Run it with: `uv run --with python-docx python3 skills/resume-editor/scripts/resume_tool.py <command>`

### Key Rules
- **Active resume:** `~/Resume/MatthewDruhl.docx` (4-column skills table, 2-page max)
- **Variants** in `~/Resume/variants/` must be synced after any active resume change
- Each variant has its own format — preserve it (see SKILL.md for details)
- Never introduce hard page breaks — let content flow naturally
- Always backup to `~/Resume/archive/` before editing

If the user provided specific instructions (e.g., `/resume add cert XYZ`), parse those and proceed.
If no specific instructions, ask what they'd like to do: view, add, edit, or remove.
