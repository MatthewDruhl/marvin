---
description: View or edit your resume
---

# /resume - Resume Editor

Read, edit, and manage your Word resume.

## Instructions

Read and follow the skill definition at `skills/resume-editor/SKILL.md`.

The resume tool script is at `skills/resume-editor/scripts/resume_tool.py`.
Run it with: `uv run --with python-docx python3 skills/resume-editor/scripts/resume_tool.py <command>`

If the user provided specific instructions (e.g., `/resume add cert XYZ`), parse those and proceed.
If no specific instructions, ask what they'd like to do: view, add, edit, or remove.
