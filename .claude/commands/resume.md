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
  - Modifies `~/Resume/data/resume-data.json`
  - Run `view` after to confirm changes

- **View mode** — User says "view" or just `/resume` without other context
  - Displays current resume data file contents

- **Stories mode** — User says "stories", "interview prep", "STAR stories"
  - Generates STAR+R stories from role deep dives
  - Saves to `~/Resume/jobs/interview-prep/story-bank.md`

- **Form Answers mode** — User says "form answers", "application questions"
  - Drafts answers to common application form questions
  - Saves to application output directory as `form-answers.md`

- **Outreach mode** — User says "outreach", "LinkedIn message"
  - Generates a 3-sentence LinkedIn connection message
  - Saves to application output directory as `outreach.md`

### Key Rules
- **Data file:** `~/Resume/data/resume-data.json` (single source of truth)
- **Base resume:** `~/Resume/MatthewDruhl.docx` (formatting preserved)
- **Voice:** Direct, concise, impact-first. No AI fluff.
- **Never fabricate** — reword existing data only
- **2-page max** — hard caps per role + auto-trim with transparency
- **Cover letter:** Confident/professional tone, 2-3 paragraphs, 1 page max

If the user provided specific instructions (e.g., `/resume add skill SQL`), parse and proceed.
If no specific instructions and no job URL, ask what they'd like to do.
