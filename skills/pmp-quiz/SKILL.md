---
name: pmp-quiz
description: |
  PMP certification quiz skill with per-person progress tracking.
  Uses True/False and Multiple Choice questions only. Tracks individual
  confidence ratings and spaced repetition for each person.
  Invoke: /pmp-quiz <name> (Matt or Emily, case-insensitive)
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

Test your PMP certification knowledge with True/False and Multiple Choice questions.

## Multi-Person Tracking

This skill tracks progress independently for each person:
- **Matt** — `skills/pmp-quiz/progress/matt.md`
- **Emily** — `skills/pmp-quiz/progress/emily.md`

### Invocation
- `/pmp-quiz matt` or `/pmp-quiz Matt` — quiz Matt
- `/pmp-quiz emily` or `/pmp-quiz Emily` — quiz Emily
- `/pmp-quiz` (no name) — ask who is quizzing

Name matching is **case-insensitive**. Progress files use lowercase filenames.

### Shared vs Individual
- **Shared:** Question bank (`skills/pmp-quiz/question-bank.md`) — same questions for everyone
- **Individual:** Progress files (`skills/pmp-quiz/progress/<name>.md`) — separate confidence, review dates, quiz history

## When to Use

- User runs `/pmp-quiz <name>`
- User says "quiz me on PMP" or "PMP quiz" (ask which person)
- User says "review PMP" or "practice PMP"
- During briefing when PMP topics are overdue (suggest a quiz)
- User says "quick PMP quiz" (short 3-question session)

## Question Types

### True/False
- Present a statement about a PMP concept
- User answers True or False
- Provide brief explanation after answering

### Multiple Choice
- Present a question with 4 answer choices (A, B, C, D)
- ONE correct answer
- Distractors should be plausible (common misconceptions, related concepts)
- After answering, explain why the correct answer is right and why key distractors are wrong

## Confidence-Based Question Difficulty

| Confidence | Question Style |
|------------|---------------|
| 1/5 | Straightforward recall — definitions, basic facts, direct T/F |
| 2/5 | Applied recall — distinguish between similar concepts, slightly tricky T/F |
| 3/5 | Scenario-based — "A PM is in this situation, what should they do?" |
| 4/5 | Nuanced scenarios — edge cases, "BEST" answer among plausible options |
| 5/5 | Exam-style — complex scenarios requiring synthesis of multiple concepts |

## Process

### Step 0: Identify Person
1. Parse the name argument (case-insensitive)
2. Load their progress file: `skills/pmp-quiz/progress/<name>.md`
3. If no name provided, ask: "Who's quizzing? Matt or Emily?"
4. Greet them: "Hey [Name], let's do some PMP review."

### Step 1: Select Topics
1. Read the person's progress file — find their PMP topics and status
2. Read `skills/pmp-quiz/question-bank.md` for available questions
3. Determine scope:
   - **"PMP quiz"** → Pick from overdue and due-today PMP topics first, then upcoming
   - **"quiz me on [PMP topic]"** → Focus on that specific topic
   - **"quick PMP quiz"** → 3 questions from overdue/due PMP topics
   - **"full PMP review"** → Work through all due PMP topics

### Step 2: Ask Questions
1. Select questions from the question bank for the chosen topic(s)
2. Use ONLY True/False and Multiple Choice formats
3. Present ONE question at a time
4. Wait for the user's answer before moving on
5. Don't reveal the answer before the user attempts it
6. Mix T/F and MC within a session for variety

### Step 3: Evaluate Answer
For each answer:
1. Compare to expected answer
2. Rate: **Correct** or **Incorrect** (no partial for T/F and MC)
3. Provide brief, clear feedback:
   - If correct: Confirm and add a deeper insight or exam tip
   - If incorrect: Explain the correct answer concisely, clarify the misconception
4. Ask if they want to continue or stop

### Step 4: Score and Update
After the quiz session (user says done, or all questions asked):
1. Summarize results:
   ```
   ## PMP Quiz Results

   **Topics covered:** [list]
   **Score:** X/Y correct

   | Topic | Result | Suggested Confidence |
   |-------|--------|---------------------|
   | [topic] | 3/4 correct | 2/5 |
   ```
2. Suggest updated confidence ratings based on performance:
   - All correct → confidence +1 (max 5)
   - Mostly correct (>70%) → maintain or +1
   - Mixed (<70%) → maintain current
   - Mostly wrong (<40%) → confidence -1 (min 1)
3. Ask user to confirm confidence updates
4. Update the person's progress file at `skills/pmp-quiz/progress/<name>.md`:
   - Set "Last Reviewed" to today
   - Update confidence rating
   - Calculate next review date based on new confidence
   - Update status
   - Add entry to Quiz History table
5. Do NOT update `state/learning.md` — progress files are the source of truth for this skill

### Step 5: Add New Questions (Optional)
If during the quiz you identify gaps in the question bank:
- Note which topics need more questions
- Offer to add new questions based on what tripped the user up

## Proactive Integration

During daily briefing, if PMP topics are overdue:
- Mention: "You have X PMP topics overdue for review. Want a quick PMP quiz?"
- If 3+ PMP topics overdue for 3+ days, nudge harder

## Notes
- Keep quiz sessions focused — 5-10 questions is a good default
- Vary question difficulty based on current confidence level
- Questions should mirror PMP exam style (scenario-based at higher confidence)
- At confidence 4/5+, questions should use PMI language ("BEST", "MOST likely", "FIRST thing")
- Track quiz history in session logs for trend analysis
- Source material: TIA Udemy course, PMBOK 7, PMI Exam Content Outline

---

*Skill created: 2026-03-25*
