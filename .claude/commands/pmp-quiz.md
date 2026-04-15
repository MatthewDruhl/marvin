---
description: PMP quiz - usage /pmp-quiz <name> [exam|revision|refresher] (Matt or Emily)
---

# /pmp-quiz - PMP Certification Quiz

Launch a PMP quiz session for a specific person.

## Usage

`/pmp-quiz <name> [mode] [count]` — where name is `Matt` or `Emily` (case-insensitive)

### Examples
- `/pmp-quiz Matt exam` — Exam Mode (60 questions, no feedback until end)
- `/pmp-quiz Matt revision` — Revision Mode (feedback after each answer)
- `/pmp-quiz Matt refresher` — Refresher Mode (recently consumed content, default 15 questions)
- `/pmp-quiz Matt refresher 10` — Refresher Mode capped at 10 questions
- `/pmp-quiz Emily refresher` — works for Emily too
- `/pmp-quiz Matt` — ask which mode before starting

## Instructions

### 1. Parse the Arguments

- Read the arguments passed after `/pmp-quiz` (available as `$ARGUMENTS`)
- Normalize to lowercase for matching
- **First argument:** Match against known users: `matt`, `emily`. If no argument or unrecognized name: display usage and ask who is quizzing
- **Second argument (optional):** Mode — `exam`, `revision`, or `refresher`. If absent, ask which mode.
- **Third argument (optional, refresher only):** Question count cap (integer). Default is 15 for refresher mode.

### 2. Load Person's Progress

- Read `skills/pmp-quiz/progress/<name>.md` (lowercase filename: `matt.md` or `emily.md`)
- If file doesn't exist, create it from the template (see below)
- This file tracks their individual PMP topic confidence, questions answered, and review dates

### 3. Run the Quiz

- Follow the full quiz process defined in `skills/pmp-quiz/SKILL.md`
- Pull questions from `skills/pmp-quiz/question-bank.md` (shared question bank)
- Select topics based on THIS PERSON's progress file (not `state/learning.md`)
- Greet them by name: "Hey [Name], let's do some PMP review."

### 4. Update Person's Progress

- After the quiz, update ONLY that person's progress file at `skills/pmp-quiz/progress/<name>.md`
- Do NOT update `state/learning.md` PMP section (that's Matt's MARVIN tracker, separate concern)
- Follow the same confidence/scoring rules from the SKILL.md

### Template for New Progress File

When creating a new progress file, copy ALL current PMP topics from `state/learning.md` (PMP Certification Topics section) with fresh starting values:

```markdown
# PMP Progress: [Name]

Last updated: [today's date]

---

## PMP Topics

| Topic | Confidence | Questions | Last Reviewed | Next Review | Interval | Status |
|-------|-----------|-----------|---------------|-------------|----------|--------|
| [copy each PMP topic from state/learning.md] | 1/5 | 0/10 | — | [today] | 1 day | New |

---

## Quiz History

| Date | Questions | Score | Topics Covered |
|------|-----------|-------|----------------|

---

*Managed by /pmp-quiz skill*
```
