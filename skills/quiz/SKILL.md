---
name: quiz
description: |
  Quiz and review skill that tests knowledge on learning tracker topics.
  Pulls from the question bank, asks conceptual and code-based questions,
  evaluates answers, and updates confidence ratings in the spaced repetition
  system. Supports focused review of overdue/due topics.
license: MIT
compatibility: marvin
metadata:
  marvin-category: learning
  user-invocable: false
  slash-command: null
  model: default
  proactive: true
---

# Quiz / Review

Test your knowledge on topics you're learning with targeted questions.

## When to Use

- User says "quiz me" or "test me"
- User says "review [topic]" in a study context
- User says "practice [topic]"
- User says "what do I need to review?"
- During briefing when topics are overdue (suggest a quiz)
- User says "quick quiz" (short 3-question session)
- User says "teach me [topic]" or "teach back" (triggers teach-back mode directly)
- User says "quiz consume" or "consume study guides"

## Process

### Step 1: Select Topics
1. Read `state/learning.md` to find topics and their status
2. Read `skills/quiz/question-bank.md` for available questions
3. Determine scope:
   - **"quiz me"** → Pick from overdue and due-today topics first, then upcoming
   - **"quiz me on [topic]"** → Focus on that specific topic
   - **"quick quiz"** → 3 questions from overdue/due topics
   - **"full review"** → Work through all due topics

### Step 2: Ask Questions
1. Select questions from the question bank for the chosen topic(s)
2. Mix question types: conceptual, code output, code writing, compare/contrast
3. Present ONE question at a time
4. Wait for the user's answer before moving on
5. Don't reveal the answer before the user attempts it
6. **Every question MUST have a correct answer.** For "Spot the Bug" questions, always verify there is an actual bug in the code before presenting it. Never show working code and ask "what's wrong?" — that wastes time and erodes trust.

**Answer verification (Issue #36):**
- For Python "Predict the Output" and "Spot the Bug" questions: mentally execute the code step by step before presenting. Verify your expected answer is correct.
- For generated questions (not from the question bank): double-check the answer by reasoning through the code again before presenting the question. If uncertain, prefer a question bank question instead.
- If the user says "bad question" or "that answer is wrong": immediately re-verify. If the question was indeed wrong, acknowledge the error, discard the question (do not count it), and apologize. Log the bad question in the session notes so it can be removed from the bank.

### Step 3: Evaluate Answer
For each answer:
1. Compare to expected answer/key concepts
2. Rate: **Correct**, **Partial**, or **Incorrect**
3. Provide brief, clear feedback:
   - If correct: Confirm and optionally add a deeper insight
   - If partial: Acknowledge what's right, clarify what's missing
   - If incorrect: Explain the correct answer concisely
4. Ask if they want to continue or stop

### Step 4: Score and Update
After the quiz session (user says done, or all questions asked):
1. Summarize results:
   ```
   ## Quiz Results

   **Topics covered:** [list]
   **Score:** X/Y correct (Z partial)

   | Topic | Result | Suggested Confidence |
   |-------|--------|---------------------|
   | [topic] | 3/4 correct | 4/5 |
   ```
2. Suggest updated confidence ratings based on performance:
   - All correct → confidence +1 (max 5)
   - Mostly correct (>70%) → maintain or +1
   - Mixed (<70%) → maintain current
   - Mostly wrong (<40%) → confidence -1 (min 1)
3. Ask user to confirm confidence updates
4. Update `state/learning.md` via learning-tracker skill logic:
   - Set "Last Reviewed" to today
   - Update confidence rating
   - Calculate next review date based on new confidence
   - Update status

### Step 5: Add New Questions (Optional)
If during the quiz you identify gaps in the question bank:
- Note which topics need more questions
- Offer to add new questions based on what tripped the user up
- User can also say "add question: [topic] - [question]" anytime

## Consume Study Guides

Ingest study guides from Learning projects into the question bank.

### Step 1: Discover
- List all `*_study_guide.md` files in `~/marvin/skills/quiz/learning/`
- If directory or files don't exist, report "No study guides to consume" and create directories if missing

### Step 2: Parse Each Study Guide
- Extract project name from filename (e.g., `decoratordojo` from `decoratordojo_study_guide.md`)
- Parse markdown sections — each heading group has: "What It Is", "Syntax", "Mini Example", "Common Mistake"

### Step 3: Generate Questions (scaled by content depth)
- **Minimum:** 3 questions per section (simple/short topics)
- **Standard:** 4-5 questions per section (typical with all 4 sub-parts)
- **Maximum:** 6-7 questions per section (meaty topics with multiple examples)

**Mapping from study guide parts to question types:**

| Study Guide Part | → Question Type |
|---|---|
| What It Is | Conceptual |
| Syntax | Fill in the Blank |
| Mini Example | Predict the Output / Code Output |
| Common Mistake (WRONG) | Spot the Bug |
| Common Mistake (RIGHT) | Refactor |
| What It Is + Syntax | Code Writing |
| Cross-section | Compare/Contrast |

**Rules:**
- Follow existing format: `**Q[N] - [Type]:** [Question]` / `**A:** [Answer]`
- Do NOT copy study guide examples verbatim — rephrase/modify values so the student has to think
- Number questions sequentially within each sub-section

### Step 4: Insert into question-bank.md
- Create new `### [Topic Name]` sub-sections under the appropriate top-level `##` section
- **Section mapping heuristic:**
  - Algorithms, data structures, sorting, searching → `## DSA Topics`
  - Python patterns (decorators, classes, error handling, OOP) → `## Python Coding Skills`
  - Idiomatic Python (comprehensions, PEP 8, built-ins) → `## Pythonic Code`
  - Docker, containers → `## Docker`
  - No match → create new `## [Category]` section before the "Adding Questions" section at the bottom
- If a sub-section with the same name already exists, append with incremented Q numbers
- Update "Last updated" date at top of question-bank.md

### Step 5: Archive and Report
- Move processed file to `~/marvin/skills/quiz/learning/consumed/`
- Create `consumed/` directory if it doesn't exist
- Output a consumption report:
  ```
  ## Study Guide Consumption Report
  **Processed:** [filename]
  **Questions generated:** [N]
  **Sections added/updated:**
  - [Topic] → [Parent Section] (X questions)
  **Moved to:** learning/consumed/[filename]
  ```

## Question Types

### Conceptual
- "What is [concept]?"
- "Explain how [algorithm] works"
- "What is the time complexity of [operation]?"
- "When would you use [X] over [Y]?"

### Code Output
- "What does this code print?" + code snippet
- "What's wrong with this code?" + buggy snippet
- "What's the return value of...?"

### Code Writing
- "Write a function that..."
- "Implement [algorithm] for..."
- "Fix this code so that..."

### Compare/Contrast
- "What's the difference between [X] and [Y]?"
- "Compare the time complexity of [X] vs [Y]"
- "When would you choose [X] over [Y]?"

## Teach-Back Mode

### When It Triggers

- Auto-activates when a topic is at confidence **4/5 or 5/5** during a quiz
- **Flow:** Ask 1-2 normal quiz questions first. If user passes, transition to teach-back. If user fails the quiz questions, stay at current confidence (no teach-back).
- Can also be triggered directly with "teach me [topic]" or "teach back"

### Three Styles (rotate all 3 per session)

**1. ELI5** — "Explain [topic] as if I've never coded before."
- Tests: Can you strip away jargon and convey the core idea?
- Follow-up probes: "Why does that matter?" / "What problem does it solve?"

**2. Applied Reasoning** — "When would you use [topic] in a real project? Give a concrete scenario."
- Tests: Can you connect theory to practice?
- Follow-up probes: "What would go wrong if you used [alternative] instead?" / "How would you decide between X and Y?"

**3. Code Walkthrough** — "Here's a snippet using [topic]. Walk me through it line by line."
- Tests: Can you read and explain existing code, not just write it?
- Follow-up probes: "What if we changed [line]?" / "Where could this break?"

### Conversation Rules

- **Probe, don't accept surface answers.** If the explanation is vague, ask a targeted follow-up.
- **2-3 follow-ups max** per style, then score and move on to next style.
- **"I'm stuck"** → Give a hint (not the answer). E.g., "Think about what happens when [specific scenario]..."
- Evaluate against the key concepts checklist for the topic (from `skills/quiz/teach-back-checklists.md`)

### Scoring

After all 3 styles, summarize:

```
## Teach-Back Results: [Topic]

| Style | Rating | Notes |
|-------|--------|-------|
| ELI5 | Strong/Adequate/Weak | [what was good/missing] |
| Applied Reasoning | Strong/Adequate/Weak | [what was good/missing] |
| Code Walkthrough | Strong/Adequate/Weak | [what was good/missing] |

**Key concepts covered:** X/Y from checklist
**Strengths:** [specific things done well]
**Areas for improvement:** [specific gaps]
```

**Rating thresholds:**
- **Strong** (all 3 styles adequate+, >80% checklist covered): Confidence +1 (or maintain at 5/5)
- **Adequate** (mixed, 50-80% checklist): Maintain current confidence
- **Weak** (any style weak, <50% checklist): Confidence -1, provide:
  - Inline explanation of missed concepts
  - Links to official docs (python.org, PEP pages, relevant documentation)

Every teach-back ends with a **Strengths + Areas for Improvement** summary.

---

## Proactive Integration

During daily briefing, if topics are overdue:
- Mention: "You have X topics overdue for review. Want a quick quiz?"
- If 3+ topics overdue for 3+ days, nudge harder

## Notes
- Keep quiz sessions focused — 5-10 questions is a good default
- Vary question difficulty based on current confidence level
- Low confidence (1-2): Start with fundamentals
- Medium confidence (3): Mix of conceptual and applied
- High confidence (4-5): Edge cases, tricky scenarios, code challenges
- **Teach-back is the assessment method for confidence 4/5 and 5/5** — auto-triggers after passing quiz questions at those levels
- Track quiz history in session logs for trend analysis
- Questions should be Python-focused where applicable (user's primary language)

---

*Skill created: 2026-02-10*
