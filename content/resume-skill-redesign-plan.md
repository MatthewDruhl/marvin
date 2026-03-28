# Resume Skill Redesign Plan

**Created:** 2026-03-28
**Status:** Ready to build

---

## Overview

Complete rewrite of the `/resume` skill. Replace the "copy and edit" approach with a "build from scratch" architecture using structured data + a formatting template.

## Architecture

### Data Layer
- **`resume-data.json`** — master record of all experience, skills, certs, education, military, header info
- Each bullet tagged with themes for smart selection (e.g., `["cloud", "leadership", "data"]`)
- Max bullet caps per role as overflow guardrails
- Single source of truth — if it's not in the data file, it's a gap

### Template Layer
- **`resume-template.docx`** — skeleton with placeholders (`{{TITLE}}`, `{{SUMMARY}}`, `{{SKILL_TABLE}}`, etc.)
- Owns all formatting: margins, fonts, spacing, table structure, section headers
- Builder opens template, replaces placeholders with generated content
- Cover letter built programmatically (confident/professional tone, 2-3 paragraphs, 1 page max)

### File Organization
```
~/marvin/skills/resume-editor/
├── SKILL.md                    # Updated skill definition
├── templates/
│   └── resume-template.docx    # Skeleton with placeholders
├── scripts/
│   └── resume_builder.py       # New builder script
└── data/
    └── resume-data.json        # Master content record

~/Resume/applications/          # Output stays here
└── {Company}/{Title}-{JobNumber}/
    ├── Resume-MATTHEW-DRUHL-{Company}.docx
    └── CoverLetter-MATTHEW-DRUHL-{Company}.docx
```

## Commands

| Command | Flow |
|---------|------|
| `/resume apply <url>` | Fetch posting → Checkpoint 1: what to emphasize/drop → Checkpoint 2: reworded content → Build .docx + cover letter → Final review → Log to applications.md + TWC |
| `/resume match <url>` | Fetch posting → strict validation against data file → required vs preferred gaps → apply/don't apply/stretch recommendation |
| `/resume update` | Add/modify entries in resume-data.json |
| `/resume view` | Display current data file contents |

## Apply Mode Checkpoints

1. **Checkpoint 1:** "Here's what I'd emphasize, here's what I'd drop" → user approves
2. **Checkpoint 2:** "Here's the reworded summary and bullets" → user approves
3. **Build:** Generate .docx from template + cover letter
4. **Final review:** Show results, page count, offer to log

## Match Analysis (`/resume match`)

Strict validation — no hand-waving:
- **Required qualifications:** YES/NO against data file, no "close enough"
- **Years of experience:** Math against actual dates
- **Tech stack:** Exact match against skills list
- **Preferred vs Required:** Separate sections to show real risk
- **Recommendation:** Apply / Don't Apply / Stretch with reasoning

## Build Rules

- **Voice:** Direct, concise, impact-first. No AI fluff.
- **Title/summary:** Generated fresh each time to match posting language
- **Bullets:** Reworded from existing data — never fabricated
- **2-page max:** Enforced via hard caps per role + auto-trim (cuts least relevant bullets by tag match score, shows what was cut)
- **Template:** Guarantees formatting fidelity

## Cover Letter

- Tone: Confident or professional
- Structure: Opening (why this role/company) → Middle (2-3 strongest matches) → Close (call to action)
- Voice: Same as resume — direct, concise, no AI fluff
- Length: 1 page max, 2-3 paragraphs

## Build Steps

1. Extract current resume into `resume-data.json` (from MatthewDruhl.docx)
2. Create skeleton `resume-template.docx` with placeholders
3. Write `resume_builder.py` (match, apply, update, view commands)
4. Update `SKILL.md` and `/resume` slash command
5. Remove old `resume_tool.py`
6. Test against a real job posting

## What Gets Deleted

- `resume_tool.py` — replaced entirely by `resume_builder.py`
- Old Apply/Edit mode logic in SKILL.md

---

*Plan finalized via /grill-me session on 2026-03-28*
