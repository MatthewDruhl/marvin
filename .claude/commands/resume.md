---
description: View, match, update, or tailor your resume for a job application
---

# /resume - Resume Builder

Modes: **Apply** (build tailored resume + cover letter), **Match** (strict gap analysis), **Update** (modify data), **View** (display data), **Stories** (STAR+R interview prep), **Form Answers** (application question drafts), **Outreach** (LinkedIn messages).

## Instructions

Read and follow the skill definition at `skills/resume-editor/SKILL.md`.

The builder script is at `skills/resume-editor/scripts/resume_builder.py`.
Run it with: `uv run --with python-docx --with lxml python3 skills/resume-editor/scripts/resume_builder.py <command>`

Available commands: `view`, `update`, `build`, `cover-letter`, `score`, `auto-trim`

If the user provided specific instructions (e.g., `/resume add skill SQL`), parse and proceed.
If no specific instructions and no job URL, ask what they'd like to do.
