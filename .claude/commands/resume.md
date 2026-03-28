---
description: View, match, update, or tailor your resume for a job application
---

# /resume - Resume Builder

Four modes: **Apply** (build tailored resume + cover letter), **Match** (strict gap analysis), **Update** (modify data), **View** (display data).

## Instructions

Read and follow the skill definition at `skills/resume-editor/SKILL.md`.

The builder script is at `skills/resume-editor/scripts/resume_builder.py`.
Run it with: `uv run --with python-docx python3 skills/resume-editor/scripts/resume_builder.py <command>`

### Mode Detection

- **Apply mode** — User provides a job URL, says "apply to", "tailor resume for", etc.
  - Fetches posting, runs checkpoints, builds resume .docx + cover letter
  - Files saved to `~/Resume/applications/{Company}/{Title}-{JobNumber}/`
  - Offers to log to applications.md + TWC after completion

- **Match mode** — User says "match", "gap analysis", "how well do I fit", etc. with a URL
  - Strict validation against `resume-data.json` only
  - Required vs preferred gaps, exact skill matching, years math
  - Outputs: Apply / Stretch / Don't Apply recommendation

- **Update mode** — User says "update", "add skill", "add cert", "add bullet"
  - Modifies `skills/resume-editor/data/resume-data.json`
  - Run `view` after to confirm changes

- **View mode** — User says "view" or just `/resume` without other context
  - Displays current resume data file contents

### Key Rules
- **Data file:** `skills/resume-editor/data/resume-data.json` (single source of truth)
- **Template:** `skills/resume-editor/templates/resume-template.docx` (formatting only)
- **Voice:** Direct, concise, impact-first. No AI fluff.
- **Never fabricate** — reword existing data only
- **2-page max** — hard caps per role + auto-trim with transparency
- **Cover letter:** Confident/professional tone, 2-3 paragraphs, 1 page max

If the user provided specific instructions (e.g., `/resume add skill SQL`), parse and proceed.
If no specific instructions and no job URL, ask what they'd like to do.
