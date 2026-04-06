---
name: interview-prep
description: |
  Generate practice questions from job descriptions, track mock interview sessions,
  and maintain a question bank. Helps prepare for upcoming interviews with
  behavioral (STAR format) and technical questions.
license: MIT
compatibility: marvin
metadata:
  marvin-category: career
  user-invocable: false
  slash-command: null
  model: default
  proactive: true
---

# Interview Prep Pipeline

Prepare for interviews with targeted practice and research.

## When to Use

- User says "prep for [company] interview" or "interview prep"
- User says "let's do a mock interview"
- User asks for practice questions
- Interview invite detected in Gmail (proactive trigger)
- User says "add question to bank"

## Process

### Step 1: Identify Prep Type
- **Company prep** → Generate questions from job description + company research
- **Mock interview** → Run practice session with questions and feedback
- **Question bank** → Add/search questions
- **Auto-prep** → When interview invite detected, generate prep guide

### Step 2: Company Prep
When preparing for a specific company:
1. Read the application from `~/Resume/jobs/applications.md`
2. Research the company (tech stack, culture, recent news)
3. Generate targeted questions:
   - 3-5 behavioral questions relevant to the role
   - 3-5 technical questions matching the tech stack
   - 2-3 system design questions at the right level
4. Create prep guide in `~/Resume/jobs/interview-prep/company-research/{company}.md`

### Step 3: Mock Interview
When running a mock session:
1. Select questions (random or company-specific)
2. Present one question at a time
3. Let user answer
4. Provide constructive feedback using STAR framework
5. Rate each answer: Strong / Okay / Needs Work
6. Log session to `~/Resume/jobs/interview-prep/mock-sessions.md`

### Step 4: Auto-Prep (Gmail Integration)
When an interview invite is detected:
1. Extract company name, role, date/time
2. Generate company prep guide automatically
3. Add to briefing: "Interview prep ready for [Company] on [date]"
4. Suggest scheduling a mock session

### Step 5: Confirm
Show what was created/updated and suggest next steps.

## Output Format

### Company Prep Guide
```
## Interview Prep: [Company] - [Role]

**Interview Date:** [date if known]
**Tech Stack:** [from job description]

### Key Questions to Prepare
**Behavioral:**
1. [question]
2. [question]

**Technical:**
1. [question]
2. [question]

**Your STAR Stories to Prepare:**
1. [suggestion based on resume/experience]

### Company Research
- [key facts]
```

## Notes
- STAR format: Situation, Task, Action, Result
- Keep mock sessions focused (15-20 min max)
- Track improvement over time in mock sessions
- Questions should match the seniority level of the role

---

*Skill created: 2026-02-08*
