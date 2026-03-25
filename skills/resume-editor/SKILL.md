---
name: resume-editor
description: |
  Read, edit, and manage your Word (.docx) resume. Two modes: Apply (tailor resume + cover letter
  for a job posting) and Edit (manual tweaks). Preserves formatting and maintains backups.
license: MIT
compatibility: marvin
metadata:
  marvin-category: career
  user-invocable: true
  slash-command: /resume
  model: default
  proactive: false
---

# Resume Editor

Edit and manage your Word resume from within MARVIN. Two modes:

- **Apply mode** — Given a job posting, create a tailored resume variant + cover letter
- **Edit mode** — Manual tweaks to the base resume (add entry, add skill, etc.)

## Resume Location

**Active resume (base):** `~/Resume/MatthewDruhl.docx`

### Directory Structure

```
~/Resume/
├── MatthewDruhl.docx          ← Base resume (source of truth)
├── applications/              ← Job-specific tailored variants
│   └── {Company}/
│       └── {Title}-{JobNumber}/
│           ├── Resume-MATTHEW-DRUHL-{Company}.docx
│           └── CoverLetter-MATTHEW-DRUHL-{Company}.docx
├── CoverLetterExamples/       ← Tone templates (6 styles)
│   ├── confident.docx
│   ├── informative.docx
│   ├── inspirational.docx
│   ├── playful.docx
│   ├── professional.docx
│   └── standard.docx
├── variants/                  ← Alternate resume formats
│   ├── Druhl Matthew ATS resume.docx
│   ├── Druhl Matthew network resume.docx
│   └── Druhl Matthew resume.docx
├── profile/                   ← Personal branding
├── certs/                     ← Coursera certification PDFs
└── archive/                   ← Backups
```

## When to Use

- User types `/resume`
- User says "update my resume", "add to resume", "edit resume"
- User says "apply to", "tailor resume for", provides a job URL
- User says "add certification to resume" or "add experience to resume"
- User wants to view current resume sections
- After earning a new certification or changing jobs

## Tool Base Command

```bash
uv run --with python-docx python3 ~/marvin/skills/resume-editor/scripts/resume_tool.py <command>
```

For page-count (needs extra deps):
```bash
uv run --with python-docx --with docx2pdf --with PyPDF2 python3 ~/marvin/skills/resume-editor/scripts/resume_tool.py page-count
```

---

## Mode 1: Apply (Job Application Workflow)

**Trigger:** User provides a job URL, says "apply to", "tailor resume for", or similar.

### Step 1: Fetch & Analyze the Job Posting

Use WebFetch on the URL. Extract:
- Company name, job title, job number/ID
- Requirements and qualifications
- Tech stack and keywords
- Salary range, location (remote/hybrid/onsite)
- What makes the role unique

### Step 2: Read Base Resume

```bash
uv run --with python-docx python3 ~/marvin/skills/resume-editor/scripts/resume_tool.py read
```

Understand current content so you can identify what to reframe.

### Step 3: Ask User Targeted Questions

Use AskUserQuestion to clarify:
- Which experience areas to emphasize for this role?
- Skills to add or remove from the table?
- Should the title/summary be reframed? (suggest a reframe based on posting)
- Cover letter tone? (show 6 options: confident, informative, inspirational, playful, professional, standard)
- Anything specific to call out? (e.g., veteran status, specific project)

### Step 4: Create Application Directory

```bash
uv run --with python-docx python3 ~/marvin/skills/resume-editor/scripts/resume_tool.py create-variant \
  --company "Company Name" \
  --title "Job Title" \
  --jobnumber "12345"
```

This copies the base resume to `~/Resume/applications/{Company}/{Title}-{JobNumber}/`.

### Step 5: Tailor the Resume Variant

Edit the variant (NOT the base resume) using the resume tool commands with `--file` where supported:

- Rewrite the title and summary to match the role's language
- Add role-relevant skills: `add-skill --skill "Skill Name"`
- Remove irrelevant skills: `remove-skill --skill "Skill Name" --file <variant-path>`
- Add role-aligned keywords to experience entries
- Consolidate or emphasize entries as needed
- Remove unearned certifications (like PMP if not yet earned)

**Iterable lessons — do these every time:**
- Reframe the entire *narrative*, don't just swap keywords
- Remove unearned certs
- Consolidate related job entries when it helps the story
- Add role-aligned keywords (not generic resume buzzwords)
- Skills table: add role-relevant, remove irrelevant (not just append)
- Summary should speak the language of the target role

### Step 6: Generate Cover Letter

Write the cover letter body content to a temp .txt file, then:

```bash
uv run --with python-docx python3 ~/marvin/skills/resume-editor/scripts/resume_tool.py create-cover-letter \
  --target-dir "~/Resume/applications/{Company}/{Title}-{JobNumber}" \
  --company "Company Name" \
  --job-title "Job Title" \
  --date "March 25, 2026" \
  --body-file "/tmp/cover_letter_body.txt"
```

The body file should contain paragraphs separated by blank lines. The tool adds:
- Date + company header
- "Dear Hiring Manager," salutation
- Body paragraphs from the file
- Signature block (name, tagline, phone, email, LinkedIn)

### Step 7: Verify Page Count

```bash
uv run --with python-docx --with docx2pdf --with PyPDF2 python3 ~/marvin/skills/resume-editor/scripts/resume_tool.py page-count \
  --file ~/Resume/applications/{Company}/{Title}-{JobNumber}/Resume-MATTHEW-DRUHL-{Company}.docx
```

Must be 2 pages or fewer.

### Step 8: Show Results

Display:
- Tailored resume content (run `read` equivalent on the variant)
- Cover letter content summary
- Page count
- Application directory path

### Step 9: Offer to Log

Ask: "Ready to apply? I'll log to applications.md + TWC when you confirm."

If confirmed, follow the job tracking workflow from CLAUDE.md to update:
- `content/jobs/applications.md`
- `content/jobs/TWC/job-application-tracker.csv`
- Current week's `content/jobs/TWC/work-search-week-*.csv`

---

## Mode 2: Edit (Manual Tweaks)

**Trigger:** User says "edit resume", "add certification", "add skill", or `/resume` without a job URL.

### Step 1: Understand the Request

Determine what the user wants:
- **View** → Display current resume structure and content
- **Add entry** → Add an entry to an existing section (cert, job, skill, etc.)
- **Add section** → Create a new section that doesn't exist yet
- **Edit entry** → Modify an existing entry
- **Remove entry** → Remove an entry from a section

### Step 2: Read Current Resume

```bash
uv run --with python-docx python3 ~/marvin/skills/resume-editor/scripts/resume_tool.py read
```

### Step 3: Backup

Before making ANY changes, create a timestamped backup:

```bash
uv run --with python-docx python3 ~/marvin/skills/resume-editor/scripts/resume_tool.py backup
```

### Step 4: Make Changes

**Add an entry to an existing section:**
```bash
uv run --with python-docx python3 ~/marvin/skills/resume-editor/scripts/resume_tool.py add-entry \
  --section "Certifications" \
  --bold-text "Cert Name" \
  --normal-text ", Issuing Org, Date"
```

**Add a new section:**
```bash
uv run --with python-docx python3 ~/marvin/skills/resume-editor/scripts/resume_tool.py add-section \
  --name "New Section Name" \
  --after "Technical Skills"
```

**Add a technical skill:**
```bash
uv run --with python-docx python3 ~/marvin/skills/resume-editor/scripts/resume_tool.py add-skill \
  --skill "Skill Name"
```

**Remove a technical skill:**
```bash
uv run --with python-docx python3 ~/marvin/skills/resume-editor/scripts/resume_tool.py remove-skill \
  --skill "Skill Name"
```

### Step 5: Verify

```bash
uv run --with python-docx python3 ~/marvin/skills/resume-editor/scripts/resume_tool.py read
```

### Step 6: Check Page Count

```bash
uv run --with python-docx --with docx2pdf --with PyPDF2 python3 ~/marvin/skills/resume-editor/scripts/resume_tool.py page-count
```

### Step 7: Confirm with User

Show what was changed and the current state. Ask if anything else needs updating.

---

## All Tool Commands

| Command | Description |
|---------|-------------|
| `read` | Display resume structure and content |
| `page-count [--file PATH]` | Check page count (converts to PDF via Word) |
| `backup` | Create a timestamped backup to `~/Resume/archive/` |
| `add-section --name NAME --after SECTION` | Add a new section header |
| `add-entry --section NAME --bold-text TEXT --normal-text TEXT` | Add entry to a section |
| `add-skill --skill NAME` | Add skill to Technical Skills table |
| `remove-skill --skill NAME [--file PATH]` | Remove skill from Technical Skills table |
| `create-variant --company NAME --title TITLE [--jobnumber ID]` | Create application-specific resume copy |
| `create-cover-letter --target-dir DIR --company NAME --job-title TITLE --body-file PATH [--date DATE]` | Generate formatted cover letter .docx |

## Rules

### Formatting Rules
- The resume is a `.docx` file — never try to edit it as text
- Section headers are: centered, bold, 14pt (matching existing style)
- Entry formatting: **Bold text** followed by normal text on the same line
- **Active resume max length: 2 pages.** Never allow changes that push it past 2 pages.
- Backups are saved to `~/Resume/archive/` with timestamps

### Technical Skills Table Rules
- **Active resume uses a 4-column table** (alphabetized)
- **ATS variant uses plain text list** (one skill per line, no table)
- **Network variant uses grouped pairs** (e.g., "Confluence / Jira")
- **Original variant uses a 2-column table**
- When adding skills, fill empty cells first, then add new rows only if needed

### Apply Mode Rules
- **Never edit the base resume** in Apply mode — always work on the variant
- Reframe the narrative for the target role, don't just swap keywords
- Remove unearned certifications
- Always verify page count after tailoring
- Skills table changes: add role-relevant, remove irrelevant

### Variant Sync Rules (Edit Mode)
- **Always sync variants after changing the active resume.** Skills, certifications, and experience must match across all files.
- **Preserve each variant's unique format:**
  - ATS: plain text, no pipes/columns, no tables for skills
  - Network: 1-page format, grouped skills, executive summary style
  - Original: 2-column skills table
- **Never add hard page breaks.** Let content flow naturally.

### Safety Rules
- Always backup before editing the base resume
- Read current resume state before making changes
- After changes, verify section order and content

## Current Resume Sections

1. Header (name, contact info)
2. Title & Summary
3. Skills Keywords
4. Technical Skills (4-column table)
5. Certifications (consolidated format: "Specialization Name, Org (Platform), Date")
6. Professional Experience
7. Additional Relevant Experience
8. Military Service
9. Education

---

*Skill created: 2026-02-17*
*Updated: 2026-03-25 — Added Apply mode for job-specific tailoring, create-variant, remove-skill, create-cover-letter commands*
