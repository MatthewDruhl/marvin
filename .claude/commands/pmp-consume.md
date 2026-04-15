---
description: Consume PMP video transcripts and generate quiz questions
---

# /pmp-consume - PMP Transcript Consumer

Consume unprocessed PMP course video transcripts and generate exam-style questions for the pmp-quiz question bank.

## Instructions

### 1. Load Skill Definition

Read `skills/pmp-quiz/pmp-consume-SKILL.md` for the full process definition.

### 2. Execute the Process

Follow all steps in the SKILL.md:

1. **Discover** — find all unprocessed `*.md` files in `pmp/CourseContent/` (not in `processed/`)
2. **Read** — read each transcript, extract exam-relevant content
3. **Generate** — create 5-8 PMP-style questions per transcript (scenario-heavy, use instructor emphasis)
4. **Write** — append questions to `skills/pmp-quiz/question-bank.md`
5. **Move** — move consumed files to `pmp/CourseContent/processed/`
6. **Update** — report new video progress count
7. **Report** — show consumption summary

### 3. Key Rules

- Process ALL unprocessed files in one run (sorted by video number)
- Add questions directly to the question bank — no approval step needed
- Move processed files so they aren't re-read
- Follow the exact question format from the existing question bank
- Prioritize scenario-based questions (~50%)
- Tag each answer with `*(Video N)*` for traceability
- Writes/appends to `pmp/CourseContent/last-consumed.md` manifest for refresher quiz tracking
