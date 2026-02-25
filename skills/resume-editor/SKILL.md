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

`~/Jobs/Resume/Druhl Matthew resume.docx`

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

### Step 6: Confirm with User

Show what was changed and the current state. Ask if anything else needs updating.

## Important Notes

- Always backup before editing
- The resume is a `.docx` file — never try to edit it as text
- Section headers are: centered, bold, 14pt (matching existing style)
- Entry formatting: **Bold text** followed by normal text on the same line
- The Technical Skills section uses a 2-column table
- Backups are saved to `~/Jobs/Resume/backups/` with timestamps

## Current Resume Sections

1. Header (name, contact info)
2. Title & Summary
3. Skills Keywords
4. Technical Skills (table format)
5. Certifications
6. Professional Experience
7. Additional Relevant Experience
8. Military Service
9. Education

---

*Skill created: 2026-02-17*
