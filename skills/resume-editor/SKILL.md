---
name: resume-editor
description: |
  Build tailored resumes and cover letters from structured data + formatting template.
  Four modes: Apply (tailor for a job posting), Match (validate fit), Update (modify data), View (display data).
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

Build tailored resumes from structured data (`resume-data.json`) + a formatting template (`resume-template.docx`). No more copy-and-edit.

## Architecture

```
skills/resume-editor/
├── SKILL.md
├── data/
│   └── resume-data.json        # Master content record (single source of truth)
├── templates/
│   └── resume-template.docx    # Skeleton with formatting preserved
└── scripts/
    ├── resume_builder.py       # CLI tool (view, update, build, cover-letter, page-count)
    └── create_template.py      # One-time template generator
```

**Output location:** `~/Resume/applications/{Company}/{Title}-{JobNumber}/`

## Tool Commands

```bash
# Base command
uv run --with python-docx python3 ~/marvin/skills/resume-editor/scripts/resume_builder.py <command>

# For page-count (extra deps)
uv run --with python-docx --with docx2pdf --with PyPDF2 python3 ~/marvin/skills/resume-editor/scripts/resume_builder.py page-count --file FILE
```

| Command | Description |
|---------|-------------|
| `view` | Pretty-print resume-data.json contents |
| `update add-skill --name NAME --categories CATS` | Add a skill with comma-separated categories |
| `update add-cert --name NAME --org ORG --platform PLATFORM --date DATE` | Add a certification |
| `update add-bullet --role ROLE --text TEXT --tags TAGS` | Add a bullet to a role |
| `update edit` | Show data file path for manual editing |
| `build --tailoring-file FILE --output-dir DIR` | Build resume .docx from tailoring file |
| `cover-letter --company NAME --job-title TITLE --body-file FILE --output-dir DIR [--date DATE]` | Build cover letter .docx |
| `page-count --file FILE` | Check page count (converts to PDF via Word) |

---

## Commands

### `/resume apply <url>`

Fetch a job posting, tailor the resume, build the .docx + cover letter.

#### Checkpoint Flow

**Step 1: Fetch & Analyze**
- WebFetch the URL
- Extract: company, title, job ID, requirements, tech stack, salary, location
- Read `resume-data.json` via `view` command

**Step 2: Checkpoint 1 — Strategy**
Present to user:
- Which keywords to emphasize for this role
- Which bullets to include (by tag relevance)
- Which skills to feature vs drop
- Title/summary reframe recommendation
- Bullets to cut (least relevant by tag score) for 2-page fit
- Cover letter tone (confident or professional)

Wait for user approval before proceeding.

**Step 3: Checkpoint 2 — Content Review**
Present to user:
- Reworded summary paragraph
- Selected and reworded bullets per role
- Skills list
- Certifications to include

Wait for user approval before proceeding.

**Step 4: Build**
1. Write the tailoring JSON file to a temp location
2. Run `build --tailoring-file FILE --output-dir DIR`
3. Write cover letter body to temp .txt file
4. Run `cover-letter --company NAME --job-title TITLE --body-file FILE --output-dir DIR`
5. Run `page-count --file RESUME_PATH` (if on macOS with Word installed)

**Tailoring file structure:**
```json
{
  "title": "Generated title for this role",
  "summary": "Generated summary paragraph",
  "keywords": ["Selected", "Keywords"],
  "skills": ["Python", "SQL"],
  "certifications": ["cert1, Org (Platform), Date"],
  "experience": [
    {
      "company": "PEARSON",
      "location": "Iowa City, IA",
      "roles": [
        {
          "title": "Senior SRE",
          "type": "Remote",
          "dates": "2022 - 2025",
          "bullets": ["Reworded bullet 1", "Reworded bullet 2"]
        }
      ]
    }
  ],
  "additional_experience": [...],
  "military": {
    "branch": "ARMY NATIONAL GUARD",
    "location": "Iowa City, IA",
    "role": "Medical Specialist",
    "start": "Nov 1993",
    "end": "Nov 2004",
    "bullets": ["Bullet text"]
  },
  "education": [
    {
      "degree": "Associate of Science (AS)",
      "field": "Computer Science",
      "school": "Indian Hills Community College",
      "location": "Ottumwa, IA",
      "years": "1995 - 1997"
    }
  ]
}
```

**Step 5: Final Review**
- Show built resume content
- Show cover letter summary
- Show page count
- Show file paths

**Step 6: Log**
Ask: "Ready to apply? I'll log to applications.md + TWC when you confirm."

If confirmed, follow the job tracking workflow from CLAUDE.md.

---

### `/resume match <url>`

Strict validation against resume data. No hand-waving.

#### Analysis Rules

- **Required qualifications:** YES or NO against data file. No "close enough."
- **Years of experience:** Math against actual dates in resume-data.json.
- **Tech stack:** Exact match against skills list. Missing = gap.
- **Preferred vs Required:** Separate sections. Preferred gaps are OK. Required gaps are risks.
- **Recommendation:** One of:
  - **Apply** — meets all required, most preferred
  - **Stretch** — meets most required, clear gaps in preferred
  - **Don't Apply** — missing required qualifications

Present the analysis with clear YES/NO columns, then the recommendation with reasoning.

---

### `/resume update`

Add or modify entries in `resume-data.json`.

Subcommands:
- `add-skill` — Add a skill with categories
- `add-cert` — Add a certification
- `add-bullet` — Add a bullet to an existing role (with tags)
- `edit` — Open the data file for manual changes

After any update, run `view` to confirm.

---

### `/resume view`

Display the current contents of `resume-data.json` in a readable format.

Run: `view` command on the builder script.

---

## Rules

### Voice
- Direct, concise, impact-first
- No AI fluff ("I'm excited to...", "As a passionate...", "leveraging")
- Never fabricate experience or skills
- Reword existing bullets for the target role — never invent new ones

### 2-Page Max
- Hard cap on bullets per role (defined in resume-data.json `max_bullets`)
- Auto-trim: cut least relevant bullets by tag match score
- Show what was cut so user can override
- Builder removes "Page Two" headers and "(continued)" lines automatically

### Cover Letter
- Tone: confident or professional (user chooses)
- Structure: date+company header, salutation, 2-3 body paragraphs, signature block
- 1 page max
- Same voice rules as resume

### Skills Table
- 4-column table, alphabetized
- Add role-relevant skills, remove irrelevant ones
- Fill empty cells first, then add rows

### Formatting
- Template preserves all original formatting: margins, fonts, spacing, section headers
- Section headers: centered, bold, 14pt
- Role headers: bold title + tab + bold dates
- Bullets: ListParagraph style

---

*Skill rewritten: 2026-03-28 — Data + template architecture*
