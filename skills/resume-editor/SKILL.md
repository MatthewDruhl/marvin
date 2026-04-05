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

Build tailored resumes from structured data (`resume-data.json`) + a base resume (`MatthewDruhl.docx`). No more copy-and-edit.

## Architecture

```
~/Resume/
├── data/
│   ├── resume-data.json        # Master content record (single source of truth)
│   └── role-deep-dive-*.json   # Role mining interview transcripts
└── MatthewDruhl.docx           # Base resume (preserves all formatting)

skills/resume-editor/
├── SKILL.md
├── ARCHITECTURE.md             # Detailed flow diagrams and data model
└── scripts/
    └── resume_builder.py       # CLI tool (view, update, build, cover-letter, score, auto-trim)
```

**Output location:** `~/Resume/applications/{Company}/{Title}-{JobNumber}/`

## Tool Commands

```bash
uv run --with python-docx python3 ~/marvin/skills/resume-editor/scripts/resume_builder.py <command>
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
| `score --tailoring-file FILE --keywords KW1,KW2,...` | Score all bullets against job keywords (lowest relevance first) |
| `auto-trim --tailoring-file FILE --output-dir DIR --keywords KW1,KW2,... [--company NAME] [--max-pages N]` | Auto-trim lowest-scored bullets until resume fits page limit, then build |

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
2. Run `auto-trim --tailoring-file FILE --output-dir DIR --keywords KW1,KW2,... --company NAME` to build the resume with automatic 2-page enforcement. This scores all bullets against the job posting keywords and removes the lowest-relevance bullets until it fits. It shows what was cut so the user can override.
3. If auto-trim is not needed (already within page limit), use `build --tailoring-file FILE --output-dir DIR` directly.
4. Write cover letter body to temp .txt file
5. Run `cover-letter --company NAME --job-title TITLE --body-file FILE --output-dir DIR`

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

### `/resume score`

Score all bullets in a tailoring file against a set of job posting keywords. Outputs a ranked list from lowest to highest relevance, showing which bullets would be cut first by auto-trim.

Run: `score --tailoring-file FILE --keywords KW1,KW2,...`

Keywords should be comma-separated terms extracted from the job posting (e.g., `Linux,SQL,Bash,Kubernetes,Java,troubleshooting`).

---

### `/resume auto-trim`

Automatically trim a tailored resume to fit within a page limit (default: 2 pages).

Run: `auto-trim --tailoring-file FILE --output-dir DIR --keywords KW1,KW2,... [--company NAME] [--max-pages N]`

**How it works:**
1. **Phase 1 (fast):** Estimates total lines and pages. Iteratively removes the lowest-scored bullet (by keyword relevance) until the estimate fits within the page limit. Never removes the last bullet from any role.
2. **Phase 2:** Builds the final DOCX using the trimmed tailoring data.

**Output:** Resume DOCX, plus `tailoring-trimmed.json` with the final bullet set for reference.

**Transparency:** Shows every bullet removed, its relevance score, and the running page estimate.

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
- Reword existing bullets for the target role, never invent new ones
- AI enhances, never authors. Every line must be defensible in an interview
- Treat generated text as a potential edit, not a final product
- **Read role mining files** (`data/role-deep-dive-*.json`) before rewording bullets. Use Matt's actual language from those transcripts as the starting point, then trim for resume format. Do not over-process.
- Every bullet must answer **"So what?"** — if it doesn't state why someone should care, rewrite or cut it
- Frame as **architect, not coder** for senior roles — "designed systems" > "wrote code"
- Show **business impact**, not just technical details — companies want engineers who understand cost, revenue, and users

### AI-Tell Checklist
Before finalizing any bullet, check for these patterns and remove them:

**Banned words/phrases:**
- Em dashes (—). Use periods, commas, or restructure instead.
- "Leveraging", "utilizing", "spearheading", "orchestrating"
- "Seamless", "seamlessly", "streamlined"
- "Cross-functional" (say who: "the security team", "Finance", etc.)
- "Stakeholders" (use the actual group: "report developers", "the Finance team")
- "End-to-end", "holistic"
- "Drove", "fostered", "facilitated"
- "Ensuring" + noun phrase
- "Successfully", "effectively", "proactively" (filler adverbs)
- "Responsible for", "worked on" (descriptions, not achievements)
- "Team player", "fast learner" (unprovable soft skills)
- Passive voice ("Latency was reduced" → "Reduced latency")

**Structural tells to avoid:**
- Every bullet starting with a past-tense power verb (mix it up)
- Overly parallel structure across bullets
- Semicolons where a period works fine
- Rule of three in every sentence
- Every bullet being roughly the same length

**Instead, write like Matt talks:**
- Lead with what actually happened, not a polished summary of it
- Be specific: names of systems (PEDA, BRIDGE, FileTransfer), real numbers, real teams
- It's OK for a bullet to tell a short story: problem, what he did, outcome
- Vary sentence openers. Not every bullet needs to start with a verb.

### XYZ Bullet Formula
Google's standard: **"Accomplished [X] as measured by [Y], by doing [Z]"**
Not every bullet needs all three parts, but aim for at least X + Z. Use this as a gut check, not a rigid template.

**Quantification methods when exact numbers aren't available:**
- Estimate scope: "serving ~2M daily active users"
- Use ranges: "reduced deploy time from ~45 min to ~8 min"
- Show scale: "across 50+ microservices"
- Use before/after: "from 200ms to 130ms"
- Count the things: "4 repos → 1", "3 separate installations → one"

### Bullet Ordering
- **Lead with the strongest achievement per role** — recruiters scan top-down, don't save the best for last
- 3-5 bullets for recent roles, 1-2 for older roles — quality over quantity
- Include **scale indicators** (users, data volume, services, team size) — these signal seniority
- Quantify mentorship outcomes where possible ("2 promoted to senior within 18 months")

### Matt's Voice Samples
These are direct quotes from role mining interviews. Use them as tone calibration:

- "Nobody else in the company was really doing Serverless. So I was really breaking new ground for us."
- "I wasn't going to be part of something that continued to not improve things."
- "I stated look at the direction we are headed."
- "We just created a new service when asked. Tested and rolled out to general use as all were created dynamically."
- "I had the idea to use SyncSort but the company didn't want to spend the money on it. So we developed a solution using Unix."
- "The developer who followed me met me like 5 years later and told me how much he enjoyed installing my code years later."
- "I always had managers or team leads come and ask me for help with something here or there."
- "I took that and improved messaging out of the system."

### Role Mining Context
Role mining deep dives are at `~/Resume/data/role-deep-dive-*.json`. These contain:
- Actual accomplishments with specific details (scale, tech, teams, outcomes)
- Matt's natural language describing his work
- Skills uncovered that may not be in resume-data.json yet
- Potential new bullets with strength ratings
- Voice notes and resume notes per role
- Career patterns (platform builder, forward thinker, go-to person, technical integrity)

**When rewording or selecting bullets:**
1. Read the relevant deep dive file first
2. Pull Matt's actual phrasing where possible
3. Add specifics from the findings (numbers, system names, team sizes)
4. Run the AI-Tell Checklist before finalizing
5. Read the bullet aloud. If it sounds like LinkedIn, rewrite it.

### ATS Optimization
- **Mirror exact language** from job postings — use the posting's phrasing, not synonyms
- **Spell out acronyms first:** "Customer Relationship Management (CRM)" so ATS catches both forms
- Use standard section headers: "Education," "Experience," "Skills"
- No headers, footers, graphics, images, or symbols — they break ATS parsing
- No complex visual layouts — keep formatting simple and clean
- Provide context alongside skills — don't just list "project management," describe how it was applied
- ~98% of Fortune 500 use ATS (Greenhouse, Lever, Workday, ICIMS, Taleo, Jobvite, etc.)
- **Semantic keyword clustering** — don't just match one keyword; include related terms (e.g., "CI/CD" + "continuous integration" + "deployment pipeline")
- **Match exact terminology** from the posting — if it says "React.js," don't write "ReactJS"
- Aim for **70-80% keyword match rate** against the job posting
- **DOCX is the safest format** for ATS portals — Taleo and iCIMS legacy have documented PDF parsing issues. Greenhouse and Lever handle both well.

### 7-Second Scan Rule
Recruiters spend ~7 seconds on initial scan, in this order:
1. **Company names** (brand recognition)
2. **Job titles** (career progression)
3. **Years of experience** (tenure)
4. **Standout numbers** (metrics that pop)

Design page 1 accordingly: contact, summary, last 2-3 roles, and key skills must all be on page 1. Put the most impressive info where eyes land first (top of page, first bullet per role).

### Senior Engineer Framing
- Show **career progression** explicitly (Dev II → Dev III → Senior → Specialist → SRE)
- Include **system design decisions** — technology selection, architecture trade-offs, migration strategies
- Connect experiences into a **narrative of growing scope and impact**
- Cut or minimize experience older than 10 years unless directly relevant to the target role
- Don't list outdated tech as primary skills — lead with current stack

### 2-Page Max
- Hard cap on bullets per role (defined in resume-data.json `max_bullets`)
- **Use `auto-trim` command** to enforce page limits programmatically:
  - Scores each bullet against job posting keywords (0.0-1.0 relevance)
  - Iteratively removes lowest-scored bullets until page estimate fits
  - Never removes the last bullet from any role
  - Shows what was cut with scores so user can override
  - Saves `tailoring-trimmed.json` for reference
- For the `/resume apply` flow, prefer `auto-trim` over `build` when the initial tailoring has many bullets
- Builder removes "Page Two" headers and "(continued)" lines automatically

### Cover Letter
- Tone: confident or professional (user chooses)
- Structure: date+company header, salutation, 2-3 body paragraphs, signature block
- 1 page max
- Same voice rules as resume
- Include concrete examples — match job requirements to specific experiences
- Maintain authentic voice — the final letter must sound like the user, not AI
- Research the org's mission and recent news to personalize
- Address career gaps or transitions directly and persuasively
- Check application instructions — some orgs restrict AI use

### Skills Table
- 4-column table, alphabetized
- Add role-relevant skills, remove irrelevant ones
- Fill empty cells first, then add rows

### Formatting
- Template preserves all original formatting: margins, fonts, spacing, section headers
- Section headers: centered, bold, 14pt
- Role headers: bold title + tab + right-justified bold dates (tab stop at pos 10800)
- Bullets: ListParagraph style
- Single-column layout only — multi-column breaks ATS parsing
- **File naming:** `Resume-FIRSTNAME-LASTNAME-COMPANY.docx` (helps recruiters find the file)
- Submit as .docx (not PDF) for maximum ATS compatibility

### Company-Tier Tailoring
Different companies value different framing:
- **FAANG/Big Tech:** Scale, data-driven decisions, system design, algorithms
- **Enterprise/Government:** Certifications matter more, compliance language, stability, clearance
- **Startups:** Speed of execution, breadth of skills, ownership, shipping
- **Consulting/Agencies:** Client-facing skills, adaptability, breadth of tech exposure

---

## References

- [Harvard FAS — AI for Resumes and Cover Letters](https://careerservices.fas.harvard.edu/ai-resumes-and-cover-letters/)
- [UPenn — Optimizing Your Resume for AI Scanners](https://careerservices.upenn.edu/blog/2024/10/08/optimizing-your-resume-for-ai-scanners/)
- [Nick Singh — 36 Resume Rules for Software Engineers](https://www.nicksingh.com/posts/36-resume-rules-for-software-engineers)
- [Tech Interview Handbook — Resume Guide](https://www.techinterviewhandbook.org/resume/)
- [SWE Resume — XYZ Method](https://www.sweresume.app/articles/xyz-method-resume/)
- [Jobscan — Resume PDF vs Word](https://www.jobscan.co/blog/resume-pdf-vs-word/)

---

*Skill updated: 2026-04-02 — Added auto-trim (confidence scoring + iterative page enforcement) and score commands*
