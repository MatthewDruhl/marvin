---
name: update-resume
description: |
  Scan cert PDFs and update resume with new certifications.
  Restructures Technical Skills table to 4 columns, alphabetized.
  Backs up before making changes. Capped at 2 pages.
license: MIT
compatibility: marvin
metadata:
  marvin-category: career
  user-invocable: true
  slash-command: /update-resume
  model: default
  proactive: false
---

# Update Resume

Scan cert PDFs from `~/Resume/certs/` and update the resume with new certifications.

## Paths

- **Resume:** `~/Resume/MatthewDruhl.docx`
- **Template:** `~/Resume/original/MatthewDruhl.docx` (formatting reference)
- **Certs:** `~/Resume/certs/*.pdf`
- **Backups:** `~/Resume/backup/`

## When to Use

- User types `/update-resume`
- User says "update resume with certs" or "add certs to resume"
- After earning a new certification (drop PDF in certs folder first)

## Process

### Step 1: Scan Cert PDFs

Extract text from all PDFs in the certs folder:

```bash
uv run --with python-docx,PyPDF2 python3 ~/marvin/skills/update-resume/scripts/update_resume.py scan-certs
```

Read the output and identify for each cert:
- **Name:** The certification/specialization name
- **Issuer:** Organization and platform (e.g., "University of Michigan (Coursera)")
- **Date:** Completion date (e.g., "Feb 2026")

For specialization certs that cover multiple courses, use the specialization name only (not individual courses).

### Step 2: Check Existing Certs

Show what's already on the resume:

```bash
uv run --with python-docx,PyPDF2 python3 ~/marvin/skills/update-resume/scripts/update_resume.py show-certs
```

Compare and identify which certs are new (skip duplicates).

### Step 3: Confirm with User

Present the list of new certs to add and ask for confirmation before modifying the resume.

### Step 4: Backup

```bash
uv run --with python-docx,PyPDF2 python3 ~/marvin/skills/update-resume/scripts/update_resume.py backup
```

### Step 5: Apply Updates

Pass the new certs as JSON via stdin:

```bash
echo '{"certs": [{"name": "Cert Name", "issuer": "Org (Platform)", "date": "Mon YYYY"}]}' | \
  uv run --with python-docx,PyPDF2 python3 ~/marvin/skills/update-resume/scripts/update_resume.py add-certs
```

This command:
1. Adds a **Certifications** section (if it doesn't exist) between Technical Skills and Professional Experience
2. Re-sorts **all** certs (existing + new) in reverse chronological order (newest first)
3. Restructures **Technical Skills** table to 4 columns, items alphabetized
4. Saves the resume

### Step 6: Verify

After updating, remind the user to open the document and verify:
- Certifications appear correctly (bold name, normal issuer and date)
- Technical Skills table has 4 columns
- Resume stays within 2 pages
- Fonts and formatting match the rest of the document

If the resume exceeds 2 pages, **stop and ask** before removing or compressing content.

## Cert Format on Resume

```
**Cert Name**, Issuer (Platform), Mon YYYY
```

- Certs listed in reverse chronological order (newest first)
- Skip certs already on the resume

## Important Notes

- Always backup before editing
- Resume is capped at 2 pages — if changes push past 2 pages, ask before compressing
- **Spacing rules to stay within 2 pages:**
  - No blank paragraph between "Certifications" header and first cert entry
  - No blank paragraph between last cert entry and next section header
  - When creating the Certifications section, insert only a blank before the header (not after)
- Match existing fonts and headings — do not change formatting
- Headers stay at the beginning of each page
- Template at `~/Resume/original/MatthewDruhl.docx` is the formatting standard

---

*Skill created: 2026-02-23*
