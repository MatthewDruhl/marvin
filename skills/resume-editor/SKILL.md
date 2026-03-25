---
name: resume-editor
description: |
  Read, edit, and manage your Word (.docx) resume. Add certifications, experience,
  skills, and new sections while preserving formatting. Maintains backups before changes.
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

Edit and manage your Word resume from within MARVIN.

## Resume Location

**Active resume:** `~/Resume/MatthewDruhl.docx`

### Directory Structure

```
~/Resume/
├── MatthewDruhl.docx          ← Active resume (always edit this first)
├── variants/                  ← Alternate resume formats
│   ├── Druhl Matthew ATS resume.docx      (ATS-optimized, plain text, no tables)
│   ├── Druhl Matthew network resume.docx  (1-page networking version)
│   └── Druhl Matthew resume.docx          (2-column table format)
├── profile/                   ← Personal branding
│   └── Matthew Druhl Professional Profile.docx
├── certs/                     ← Coursera certification PDFs
└── archive/                   ← Old versions & backups
```

## When to Use

- User types `/resume`
- User says "update my resume", "add to resume", "edit resume"
- User says "add certification to resume" or "add experience to resume"
- User wants to view current resume sections
- After earning a new certification or changing jobs

## Process

### Step 1: Understand the Request

Determine what the user wants to do:
- **View** → Display current resume structure and content
- **Add entry** → Add an entry to an existing section (cert, job, skill, etc.)
- **Add section** → Create a new section that doesn't exist yet
- **Edit entry** → Modify an existing entry
- **Remove entry** → Remove an entry from a section

### Step 2: Read Current Resume

Always read the resume first to understand current state:

```bash
uv run --with python-docx python3 ~/marvin/skills/resume-editor/scripts/resume_tool.py read
```

This outputs the full resume structure with section headers and content.

### Step 3: Backup

Before making ANY changes, create a timestamped backup:

```bash
uv run --with python-docx python3 ~/marvin/skills/resume-editor/scripts/resume_tool.py backup
```

### Step 4: Make Changes

Use the resume tool for modifications:

**Add an entry to an existing section:**
```bash
uv run --with python-docx python3 ~/marvin/skills/resume-editor/scripts/resume_tool.py add-entry \
  --section "Certifications" \
  --bold-text "Cert Name" \
  --normal-text ", Issuing Org, Date"
```

**Add a new section** (inserts with centered, bold, 14pt header matching existing style):
```bash
uv run --with python-docx python3 ~/marvin/skills/resume-editor/scripts/resume_tool.py add-section \
  --name "New Section Name" \
  --after "Technical Skills"
```

**Add a technical skill to the skills table:**
```bash
uv run --with python-docx python3 ~/marvin/skills/resume-editor/scripts/resume_tool.py add-skill \
  --skill "Skill Name"
```

### Step 5: Verify

After making changes, read the resume again to confirm:

```bash
uv run --with python-docx python3 ~/marvin/skills/resume-editor/scripts/resume_tool.py read
```

### Step 6: Check Page Count

After any content changes, verify the resume stays within the 2-page limit:

```bash
uv run --with python-docx --with docx2pdf --with PyPDF2 python3 ~/marvin/skills/resume-editor/scripts/resume_tool.py page-count
```

For a specific file (e.g., a variant):
```bash
uv run --with python-docx --with docx2pdf --with PyPDF2 python3 ~/marvin/skills/resume-editor/scripts/resume_tool.py page-count --file ~/Resume/variants/SomeVariant.docx
```

This converts the .docx to PDF via Word and counts the actual rendered pages.

### Step 7: Confirm with User

Show what was changed and the current state. Ask if anything else needs updating.

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

### Variant Sync Rules
- **Always sync variants after changing the active resume.** Skills, certifications, and experience must match across all files.
- **Preserve each variant's unique format:**
  - ATS: plain text, no pipes/columns, no tables for skills, repeats "PEARSON, Iowa City, IA" per role
  - Network: 1-page format, grouped skills, executive summary style, no certifications section
  - Original: 2-column skills table, same structure as active but different table layout
- **Copy paragraph XML from active resume** when possible to preserve spacing (`before=60`, `before=120`, etc.)
- **Never add hard page breaks** (`w:br type="page"`). Let content flow naturally. The "Page Two" header is inline content, not tied to a page break.
- After syncing, verify the variant paragraph structure matches the active resume (same paragraph count, same spacing attributes)

### Safety Rules
- Always backup before editing (to `~/Resume/archive/`)
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
*Updated: 2026-03-11 — New file paths, variant sync rules, 2-page limit, 4-column table*
