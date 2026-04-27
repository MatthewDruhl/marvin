---
name: pmp-consume
description: |
  Consume PMP course video transcripts from pmp/CourseContent/ and generate
  PMP-style questions added to the pmp-quiz question bank. Tracks processed
  files to avoid duplicate work. Updates video progress count.
  Invoke: /pmp-consume
license: MIT
compatibility: marvin
metadata:
  marvin-category: learning
  user-invocable: true
  slash-command: /pmp-consume
  model: default
  proactive: false
---

# PMP Consume — Transcript to Question Bank

Ingest PMP course video transcripts and generate exam-style questions for the pmp-quiz skill.

---

## Source Files

- **Input:** `pmp/CourseContent/*.md` — transcript files named by video number (e.g., `99.md`, `100.md`)
- **Output:** `skills/pmp-quiz/question-bank.md` — shared question bank
- **Processed:** `pmp/CourseContent/processed/` — consumed files moved here
- **Progress:** `skills/pmp-quiz/progress/matt.md` — video count updated

### File Format

Each transcript file contains ONLY the raw transcript from a TIA Education PMP course video. No AI overview, no frontmatter — just the instructor's words.

Files are named by video number: `99.md`, `100.md`, `101.md`, etc.

---

## Process

### Step 1: Discover Unprocessed Files

1. List all `*.md` files in `pmp/CourseContent/` (exclude `processed/` subdirectory)
2. If no files found, report "No new transcripts to consume." and stop
3. Sort files by video number (numeric sort on filename)
4. Report: "Found N unprocessed transcript(s): [list filenames]"

### Step 2: Read and Analyze Each Transcript

For each file, in video number order:

1. Read the full transcript
2. Identify the **topic(s)** covered (the instructor usually states it at the start)
3. Extract **exam-relevant content** — focus on:
   - Definitions and distinctions the instructor emphasizes
   - Anything the instructor says "remember for your exam" or "I want you to know"
   - Tricky details, traps, and common misconceptions
   - Concrete examples and analogies
   - Process relationships (what feeds into what)
   - Comparisons and tradeoffs (e.g., crashing vs fast tracking)

### Step 3: Generate Questions

For each transcript, generate **5-8 questions** following the pmp-quiz question types:

| Label | Type | Target % |
|-------|------|----------|
| `[SCENARIO]` | Situational judgment — a PM situation, choose best response | ~50% |
| `[MC]` | Multiple choice — one correct answer from 4 options | ~25% |
| `[MULTI-SELECT]` | Select all that apply | ~15% |
| `[ORDERING]` | Arrange steps in correct order | ~10% |

**Question quality rules:**

1. **Scenario questions are king.** The PMP exam is scenario-based. Don't just test definitions — test application. "A PM discovers the schedule is 20 days over. What should they try FIRST?" is better than "What is crashing?"
2. **Use the instructor's emphasis.** If they said "remember this for your exam," build a question around it.
3. **Include trap answers.** The PMP exam loves plausible-but-wrong options. Use common misconceptions as distractors.
4. **Test distinctions.** If the transcript compares two things (crashing vs fast tracking, schedule baseline vs project schedule), test that comparison.
5. **Match existing format.** Follow the exact format in `skills/pmp-quiz/question-bank.md`:
   ```
   **Q[N] - [TYPE]:** [Question]
   A) ...
   B) ...
   C) ...
   D) ...
   **A:** [Letter]) [Explanation with exam-relevant context]
   ```
6. **Answer distribution.** Across all generated questions per batch, roughly balance A/B/C/D answers.
7. **Tag the source video.** Add `*(Video [N])*` at the end of each answer explanation so questions are traceable.

### Step 4: Write to Question Bank

1. Read current `skills/pmp-quiz/question-bank.md`
2. Determine section placement:
   - Match the transcript topic to an existing `### [Topic]` section if one exists — append questions with incremented Q numbers
   - If no matching section exists, create a new `### [Topic]` subsection under the appropriate `## Section` header
   - If unsure which section header, create under `## Section 8: Schedule Management` (or whatever section the video belongs to based on the TIA course structure)
3. Update the "Last updated" date at top of question-bank.md
4. Write the changes

### Step 5: Move to Processed

1. Create `pmp/CourseContent/processed/` if it doesn't exist
2. Move each consumed file to `pmp/CourseContent/processed/`
3. This prevents re-reading on future runs

### Step 5.5: Write Refresher Manifest

After processing, write or update `pmp/CourseContent/last-consumed.md` to track which questions are available for refresher quizzes.

**If `last-consumed.md` does not exist**, create it:

```markdown
# Last Consumed

date: [today's date]
videos: [list of video numbers just processed]
topics:
  - [Topic 1]
  - [Topic 2]

## Unquizzed Questions

| Video | Topic | Question ID | Quizzed? |
|-------|-------|-------------|----------|
| 99 | Develop Schedule | Q1 | no |
| 99 | Develop Schedule | Q2 | no |
```

**If `last-consumed.md` already exists**, APPEND the new data:
- Add today's date and new video numbers to the header fields
- Add new topics to the topics list (skip duplicates)
- Append new question rows to the Unquizzed Questions table
- Do NOT overwrite existing rows — unquizzed questions from previous runs accumulate

**Question ID** matches the Q number under the topic's `### [Topic]` section in the question bank (e.g., Q1 under `### Develop Schedule`).

**Quizzed?** starts as `no` for all new questions. The `/pmp-quiz refresher` mode flips these to `yes` as questions are answered.

### Step 6: Update Video Progress and Sync State

After processing, gather these counts:
1. **Total videos processed:** count all files in `pmp/CourseContent/processed/`
2. **Highest video number:** from processed filenames
3. **Total questions in bank:** count all `**Q` lines in `skills/pmp-quiz/question-bank.md`
4. **Unquizzed refresher count:** count rows with `| no |` in `pmp/CourseContent/last-consumed.md`

Then **auto-update state files** so they stay in sync:

**`state/current.md`:**
- Update the PMP line in **Active Priorities** — replace the items count, remaining count, questions count, and refresher backlog count
  - Items formula: total videos processed + any exam/non-video items already counted (preserve the non-video portion, only replace the video count)
  - Remaining: 366 minus items count
- Update the **Projects table** PMP row with current video count and question count

**`state/goals.md`:**
- Update the **PMP Certification** row in the Tracking table with current items count and question count

### Step 7: Report

Output a consumption report:

```
## PMP Consume Report

**Processed:** [N] transcript(s)
**Videos:** [list video numbers]
**Questions generated:** [total count]

| Video | Topic | Questions Added | Section |
|-------|-------|----------------|---------|
| 99 | Develop Schedule | 7 | Section 8: Schedule Management |
| 100 | [topic] | 5 | [section] |

**Latest video:** [highest number]
**Total processed to date:** [count in processed/]
**New topics added to question bank:** [list any new ### sections created]
**Refresher manifest:** Updated `pmp/CourseContent/last-consumed.md` — [N] new questions queued for refresher
```

---

## Notes

- The transcript is the primary source. The instructor's emphasis, examples, and "exam tips" are the most valuable material for question generation.
- Questions should test understanding, not memorization. Scenario-based is always preferred.
- If a transcript covers a topic already in the question bank, ADD questions (don't replace). Different angles on the same topic strengthen the bank.
- Keep question explanations concise but include the "why" — this feeds into Revision Mode feedback.

---

*Skill created: 2026-04-14*
