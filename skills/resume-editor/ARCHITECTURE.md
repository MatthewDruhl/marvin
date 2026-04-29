# Resume Skill Architecture

## File Structure

```
~/Resume/                              (data home — outside marvin repo)
├── data/
│   ├── resume-data.json               Single source of truth for all content
│   ├── role-deep-dive-*.json          Role mining interview transcripts (8 files)
│   └── voice-samples.md              Tone calibration quotes from interviews
├── MatthewDruhl.docx                  Base resume (preserves all formatting)
└── applications/
    └── {Company}/                     Output per company
        ├── {First}_{Last}_resume.docx
        ├── {First}_{Last}_cover_letter.docx
        ├── tailoring.json             Tailoring input for this application
        └── tailoring-trimmed.json     Post-trim version (if auto-trimmed)

~/marvin/skills/resume-editor/         (skill code — in marvin repo)
├── SKILL.md                           Skill instructions + voice rules
├── ARCHITECTURE.md                    This file
├── scripts/
│   └── resume_builder.py              CLI tool (view, update, build, cover-letter, score, auto-trim)
└── tests/
    ├── __init__.py
    ├── test_scoring.py                score_bullet, score_tailoring
    ├── test_estimation.py             estimate_lines, estimate_total_lines, estimate_pages
    ├── test_trim.py                   remove_lowest_bullet
    ├── test_data_helpers.py           load_data, load_tailoring, save_data
    ├── test_build_integration.py      cmd_build, cmd_auto_trim (requires base resume)
    └── test_cover_letter_integration.py  cmd_cover_letter
```

Note: `resume-template.docx` is referenced in SKILL.md but the builder actually uses
`MatthewDruhl.docx` as the base document. The template file is not used in the current flow.

---

## Command Map

```
/resume
  ├── apply <url>      Fetch posting → tailor → build docx + cover letter → log
  ├── match <url>      Fetch posting → strict YES/NO analysis → recommendation
  ├── update           Modify resume-data.json (add-skill, add-cert, add-bullet, edit)
  ├── view             Pretty-print resume-data.json
  ├── score            Score bullets against keywords (diagnostic)
  └── auto-trim        Score + trim + build (used by apply internally)
```

---

## /resume apply Flow

This is the main workflow. Steps 1-3 are Claude (AI), steps 4-5 are resume_builder.py (code).

```
 User: /resume apply <url>
          │
          ▼
 ┌─────────────────────┐
 │  Step 1: Fetch &    │   WebFetch URL
 │  Analyze Posting    │   Extract: company, title, job ID, requirements,
 │                     │   tech stack, salary, location
 │                     │   Read resume-data.json via `view` command
 └────────┬────────────┘
          │
          ▼
 ┌─────────────────────┐
 │  Step 2: Strategy   │   Claude proposes:
 │  Checkpoint         │   • Keywords to emphasize
 │                     │   • Bullets to include (by tag relevance)
 │  ⏸ USER APPROVAL    │   • Skills to feature vs drop
 │                     │   • Title/summary reframe
 │                     │   • Cover letter tone
 └────────┬────────────┘
          │
          ▼
 ┌─────────────────────┐
 │  Step 3: Content    │   Claude presents:
 │  Review Checkpoint  │   • Reworded summary
 │                     │   • Selected/reworded bullets per role
 │  ⏸ USER APPROVAL    │   • Skills list
 │                     │   • Certifications
 └────────┬────────────┘
          │
          ▼
 ┌─────────────────────┐
 │  Step 4: Build      │   Claude writes tailoring.json, then calls:
 │  (resume_builder)   │
 │                     │   auto-trim ──or── build
 │                     │       │                │
 │                     │   (if many bullets)  (if fits)
 │                     │       │                │
 │                     │       ▼                ▼
 │                     │   Score → Trim ──► Build DOCX
 │                     │
 │                     │   Also: write cover letter body → cover-letter command
 └────────┬────────────┘
          │
          ▼
 ┌─────────────────────┐
 │  Step 5: Review     │   Show built content + file paths
 │  & Log              │
 │                     │   "Ready to apply? I'll log to
 │  ⏸ USER APPROVAL    │    applications.md + TWC when you confirm."
 └─────────────────────┘
```

---

## Build Pipeline (resume_builder.py)

```
 ┌──────────────┐     ┌──────────────┐
 │ MatthewDruhl │     │  tailoring   │
 │   .docx      │     │    .json     │
 │ (base resume)│     │ (selections) │
 └──────┬───────┘     └──────┬───────┘
        │                    │
        ▼                    ▼
 ┌─────────────────────────────────┐
 │         cmd_build()             │
 │                                 │
 │  1. Open base .docx             │
 │  2. Replace title, tagline,     │
 │     summary, keywords           │
 │  3. Rebuild skills table        │
 │  4. Rebuild certifications      │
 │  5. Rebuild experience sections │
 │     ├── Company headers         │
 │     ├── Role headers (keepNext) │
 │     ├── Bullets                 │
 │     └── Page break estimation   │
 │  6. Rebuild military section    │
 │  7. Rebuild education           │
 │  8. Apply compact mode (if set) │
 │  9. Save .docx                  │
 └────────────────┬────────────────┘
                  │
                  ▼
     Matthew_Druhl_resume.docx
```

---

## Auto-Trim Pipeline

```
 tailoring.json + keywords
        │
        ▼
 ┌─────────────────────────────────┐
 │  Phase 1: Estimate & Trim       │
 │                                 │
 │  Loop:                          │
 │    score_tailoring()            │
 │      └─► score_bullet() ×N     │  substring match: kw.lower() in text
 │          (sorted ascending)     │
 │    estimate_pages()             │
 │      └─► estimate_total_lines() │  HEADER_LINES + sections + bullets
 │          └─► estimate_lines()   │  chars / CHARS_PER_LINE (95)
 │    if pages > max:              │
 │      remove_lowest_bullet()     │  never removes last bullet per role
 │    else: break                  │
 └────────────────┬────────────────┘
                  │
                  ▼
 ┌─────────────────────────────────┐
 │  Phase 2: Build                 │
 │                                 │
 │  Write trimmed tailoring → temp │
 │  Call cmd_build()               │
 │  Save tailoring-trimmed.json    │
 └────────────────┬────────────────┘
                  │
                  ▼
     Resume .docx + tailoring-trimmed.json
```

---

## Data Flow

```
                    ┌─────────────────────┐
                    │  resume-data.json   │
                    │  (master record)    │
                    │                     │
                    │  • header (contact) │
                    │  • title, tagline   │
                    │  • summary          │
                    │  • keywords         │
                    │  • skills[]         │
                    │  • certifications[] │
                    │  • experience[]     │
                    │    └─ roles[]       │
                    │      └─ bullets[]   │
                    │        └─ tags[]    │
                    │  • military         │
                    │  • education[]      │
                    └────────┬────────────┘
                             │
              ┌──────────────┼──────────────┐
              │              │              │
              ▼              ▼              ▼
         /resume view   /resume apply   /resume update
         (read-only)    (read → tailor) (read → modify → save)
                             │
                             ▼
                    ┌─────────────────────┐
                    │   tailoring.json    │
                    │   (per-application) │
                    │                     │
                    │  Subset of master   │
                    │  data, reworded for │
                    │  specific job:      │
                    │  • selected bullets │
                    │  • reworded text    │
                    │  • filtered skills  │
                    │  • targeted summary │
                    └────────┬────────────┘
                             │
                    ┌────────┴────────┐
                    │                 │
                    ▼                 ▼
              build command     auto-trim command
                    │                 │
                    ▼                 ▼
              Resume .docx      Resume .docx
                              + trimmed.json
```

---

## Test Coverage Map

```
resume_builder.py
│
├── Data Helpers ─────────── test_data_helpers.py (8 tests)
│   ├── load_data()             missing file, valid JSON, malformed JSON
│   ├── load_tailoring()        missing file, valid load
│   └── save_data()             round-trip, unicode, trailing newline
│
├── Scoring ──────────────── test_scoring.py (15 tests)
│   ├── score_bullet()          exact match, no match, partial, case,
│   │                           empty, substring bugs (SQL/MySQL, Java/JS)
│   └── score_tailoring()       sorting, completeness, structure, truncation
│
├── Estimation ───────────── test_estimation.py (13 tests)
│   ├── estimate_lines()        empty, short, exact, wrapping, long
│   ├── estimate_total_lines()  minimal, headers, bullets, compact, military
│   └── estimate_pages()        1-page, 2+-page, empty
│
├── Trimming ─────────────── test_trim.py (8 tests)
│   └── remove_lowest_bullet()  removes lowest, protects last bullet,
│                               all-at-minimum, military, iterative
│
├── Build (integration) ──── test_build_integration.py (7 tests)
│   ├── cmd_build()             produces docx, filename, not empty
│   └── cmd_auto_trim()         output, valid JSON, rename, min-bullets
│
└── Cover Letter (integration) ─ test_cover_letter_integration.py (5 tests)
    └── cmd_cover_letter()      creates docx, filename, missing file, default date

                                                         Total: 56 tests
```

---

## Known Issues

Tracked as GitHub issues: [MatthewDruhl/marvin issues (resume-skill)](https://github.com/MatthewDruhl/marvin/labels/resume-skill)

---

*Generated: 2026-04-05*
