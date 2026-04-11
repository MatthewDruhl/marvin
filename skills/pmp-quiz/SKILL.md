---
name: pmp-quiz
description: |
  PMP certification quiz skill with per-person progress tracking.
  Supports Exam Mode (strict simulation) and Revision Mode (learning with feedback).
  Uses Scenario, Multi-Select, Ordering, and Calculation question types.
  Tracks individual confidence ratings and spaced repetition for each person.
  Invoke: /pmp-quiz <name> [exam|revision] (Matt or Emily, case-insensitive)
license: MIT
compatibility: marvin
metadata:
  marvin-category: learning
  user-invocable: true
  slash-command: /pmp-quiz
  model: default
  proactive: true
---

# PMP Quiz

Test your PMP certification knowledge with scenario-based, multi-select, ordering, and calculation questions in either Exam Mode or Revision Mode.

---

## Multi-Person Tracking

This skill tracks progress independently for each person:
- **Matt** — `skills/pmp-quiz/progress/matt.md`
- **Emily** — `skills/pmp-quiz/progress/emily.md`

### Invocation
- `/pmp-quiz Matt exam` — quiz Matt in Exam Mode
- `/pmp-quiz Matt revision` — quiz Matt in Revision Mode
- `/pmp-quiz Emily exam` — quiz Emily in Exam Mode
- `/pmp-quiz Emily revision` — quiz Emily in Revision Mode
- `/pmp-quiz Matt` (no mode) — ask which mode before starting
- `/pmp-quiz` (no name) — ask who is quizzing, then which mode

Name and mode matching are **case-insensitive**.

### Shared vs Individual
- **Shared:** Question bank (`skills/pmp-quiz/question-bank.md`) — same questions for everyone
- **Individual:** Progress files (`skills/pmp-quiz/progress/<name>.md`) — separate confidence, review dates, quiz history

---

## Session Modes

### Exam Mode
Strict PMP exam simulation. No feedback during the session.

- After each answer: respond only with "Recorded." — no hints, no explanations, no encouragement, no "that's close"
- All feedback, explanations, and scoring are held until the end-of-section review
- Mirrors real PMP exam conditions

### Revision Mode
Learning mode with immediate feedback after each answer.

- After each answer: state correct/incorrect, provide an explanation, and identify which PMBOK 7 principle applies
- Encourages understanding, not just recall
- Suitable for studying and building confidence

**If mode is not specified, ask before starting:** "Which mode — Exam (no feedback until the end) or Revision (feedback after each answer)?"

---

## Context Window Warning

**IMPORTANT:** A full 180-question PMP session exceeds safe context window limits.

- Treat each 60-question section as a **separate session**
- Start a new `/pmp-quiz` session for each section
- If the user requests more than 60 questions in one session, display this reminder:
  > "180 questions exceed safe context window limits. Treat each 60Q section as a separate session. Start a new /pmp-quiz session for each section."

---

## Question Types

Each question must be labeled with its type. The label appears at the start of the question.

| Label | Type | Description |
|-------|------|-------------|
| `[SCENARIO]` | Situational judgment | A PM situation — choose the best response |
| `[MULTI-SELECT]` | Select all that apply | Multiple correct answers; user selects all that apply |
| `[ORDERING]` | Arrange steps | Put items or process steps in the correct order |
| `[CALCULATION]` | EV/EAC/SPI/CPI math | Compute a project metric given numbers |

### Target Mix per 60-Question Section
- ~70% Scenario (42 questions)
- ~15% Multi-Select (9 questions)
- ~10% Ordering (6 questions)
- ~5% Calculation (3 questions)

Track the type of every question asked and report the mix in the end-of-section domain audit.

---

## PMP Exam Domains (PMI ECO Distribution)

| Domain | Target % | Target Q per 60 |
|--------|----------|-----------------|
| People | ~42% | ~25 questions |
| Process | ~50% | ~30 questions |
| Business Environment | ~8% | ~5 questions |

After each 60-question section, report how many questions came from each domain and flag any domain that is more than 10 percentage points off target.

---

## Answer Distribution Rule (HARD RULE)

**Before writing any questions for a session, pre-plan the full answer key.**

- Verify the answer key is approximately 25% A, 25% B, 25% C, 25% D before presenting questions.
- AI models default to answer B — this bias must be explicitly counteracted.
- Do not begin presenting questions until the distribution check passes.
- For a 60-question set: target 15 A answers, 15 B answers, 15 C answers, 15 D answers (±3 tolerance).
- This rule applies to all multiple-choice question types (Scenario, Calculation). Multi-select and Ordering questions are exempt from the letter distribution check but must still be pre-planned.

---

## 60-Question Section Hard Limit

- Each section is capped at **60 questions**. This limit is absolute — do not continue past 60.
- Display a counter with every question: **"Question X of 60"**
- At question 60, complete that answer and immediately run the end-of-section domain audit and scoring.
- If the user asks for more questions after 60: "This section is complete. Start a new /pmp-quiz session to continue."

---

## Disputed Answers

If the user believes a question's answer is wrong:

1. User flags it with `[DISPUTED]`
2. Before confirming or changing the answer, cross-reference PMBOK 7 + Agile Practice Guide
3. State which source supports the final answer
4. Final authority: **PMBOK 7 + Agile Practice Guide**
5. Note the dispute and resolution in the end-of-section review

---

## Confidence-Based Question Difficulty

| Confidence | Question Style |
|------------|---------------|
| 1/5 | Straightforward recall — definitions, basic facts |
| 2/5 | Applied recall — distinguish between similar concepts |
| 3/5 | Scenario-based — "A PM is in this situation, what should they do?" |
| 4/5 | Nuanced scenarios — edge cases, "BEST" answer among plausible options |
| 5/5 | Exam-style — complex scenarios requiring synthesis of multiple concepts |

---

## Process

### Step 0: Identify Person and Mode

1. Parse the name argument (case-insensitive). If absent, ask: "Who's quizzing? Matt or Emily?"
2. Parse the mode argument (exam or revision). If absent, ask: "Which mode — Exam (no feedback until the end) or Revision (feedback after each answer)?"
3. Load their progress file: `skills/pmp-quiz/progress/<name>.md`
4. Display the session header:
   ```
   Hey [Name], let's do some PMP review.
   Mode: [EXAM MODE — no feedback until section end] or [REVISION MODE — feedback after each answer]
   Section: 60 questions | Answer distribution pre-planned | Domain coverage tracked
   ```
5. Display the context window warning if the user has indicated they want more than 60 questions.

### Step 1: Pre-Plan the Question Set

Before presenting any questions:

1. Select topics based on THIS PERSON's progress file (not `state/learning.md`).
2. Plan the full 60-question set (or shorter set if fewer requested):
   - Assign domains: ~42% People, ~50% Process, ~8% Business Environment
   - Assign question types: ~70% Scenario, ~15% Multi-Select, ~10% Ordering, ~5% Calculation
   - Assign answer letters: ~25% each of A, B, C, D (for MC questions)
   - Verify all three distributions pass before continuing
3. Pull questions from `skills/pmp-quiz/question-bank.md` where available; generate new questions to fill the plan.

### Step 2: Ask Questions

1. Present ONE question at a time.
2. Format each question:
   ```
   Question X of 60 | [TYPE] | Domain: [People/Process/Business Environment]

   [Question text]

   A. [Option]
   B. [Option]
   C. [Option]
   D. [Option]
   ```
   For Multi-Select: note "Select all that apply."
   For Ordering: list items and ask user to arrange them.
   For Calculation: include the numeric inputs in the question.
3. Wait for the user's answer before moving on. Do not reveal the answer before the user attempts it.

### Step 3: Evaluate Answer

**Exam Mode:**
- Respond only with "Recorded." and present the next question.
- Do not provide any feedback, hints, or explanations.

**Revision Mode:**
- State correct or incorrect.
- Provide a concise explanation.
- Identify which PMBOK 7 principle or process group applies.
- For Multi-Select: list all correct answers and explain any the user missed or got wrong.

### Step 4: End-of-Section Review (both modes)

After question 60 (or the final question of a shorter session):

1. **Score summary:**
   ```
   ## PMP Quiz Results — Section Complete

   Mode: [Exam/Revision]
   Score: X/60 correct ([Y]%)

   | Topic | Q Asked | Correct | Score |
   |-------|---------|---------|-------|
   | [topic] | N | N | N% |
   ```

2. **Domain audit:**
   ```
   ## Domain Coverage

   | Domain | Questions | % of Total | Target | Status |
   |--------|-----------|------------|--------|--------|
   | People | N | N% | 42% | [OK / OVER / UNDER] |
   | Process | N | N% | 50% | [OK / OVER / UNDER] |
   | Business Environment | N | N% | 8% | [OK / OVER / UNDER] |
   ```

3. **Question type mix:**
   ```
   ## Question Type Mix

   | Type | Questions | % of Total | Target |
   |------|-----------|------------|--------|
   | Scenario | N | N% | 70% |
   | Multi-Select | N | N% | 15% |
   | Ordering | N | N% | 10% |
   | Calculation | N | N% | 5% |
   ```

4. **Exam Mode only — full answer review:** Go through each question, state the correct answer, and provide the explanation that was withheld during the session. Flag any `[DISPUTED]` items and their resolutions.

5. **Confidence update suggestions:**
   - All correct → confidence +1 (max 5)
   - Mostly correct (>70%) → maintain or +1
   - Mixed (40–70%) → maintain current
   - Mostly wrong (<40%) → confidence -1 (min 1)
   - Ask user to confirm before writing changes.

6. **Update progress file** at `skills/pmp-quiz/progress/<name>.md`:
   - Set "Last Reviewed" to today
   - Update confidence rating (after confirmation)
   - Calculate next review date based on new confidence
   - Update status
   - Add entry to Quiz History table

7. Do NOT update `state/learning.md` — progress files are the source of truth for this skill.

### Step 5: Add New Questions (Optional)

If gaps exist in the question bank for certain topics:
- Note which topics need more questions
- Offer to add new questions based on what tripped the user up

---

## Proactive Integration

During daily briefing, if PMP topics are overdue:
- Mention: "You have X PMP topics overdue for review. Want a quick PMP quiz?"
- If 3+ PMP topics overdue for 3+ days, nudge harder
- Suggest mode: "Exam Mode for realistic practice, Revision Mode for studying."

---

## Notes

- Keep quiz sessions to 60 questions per session maximum (context window safety)
- Vary question difficulty based on current confidence level
- Questions must mirror PMP exam style at higher confidence levels — use PMI language: "BEST", "MOST likely", "FIRST thing"
- Track quiz history in session logs for trend analysis
- Source material: TIA Udemy course, PMBOK 7, PMI Exam Content Outline, Agile Practice Guide
- For disputed answers: always cite the specific PMBOK 7 or Agile Practice Guide section

---

*Skill created: 2026-03-25*
*Updated: 2026-04-09 — Added Exam/Revision modes, answer distribution enforcement, 60Q hard limit, domain audit, question type mix, zero feedback in exam mode, disputed answer procedure, context window warning*
