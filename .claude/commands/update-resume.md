---
description: Update resume with new certifications from PDF files
---

# /update-resume - Update Resume with Certs

Scan cert PDFs and update your resume with new certifications.

## Instructions

Read and follow the skill definition at `skills/update-resume/SKILL.md`.

The update resume script is at `skills/update-resume/scripts/update_resume.py`.
Run it with: `uv run --with python-docx,PyPDF2 python3 skills/update-resume/scripts/update_resume.py <command>`

Follow the steps in SKILL.md:
1. Scan cert PDFs (extract text)
2. Parse cert info (name, issuer, date)
3. Check for duplicates on current resume
4. Confirm with user before modifying
5. Backup current resume
6. Apply updates (add certs, restructure skills table)
7. Remind user to verify formatting and 2-page limit
