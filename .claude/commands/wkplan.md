---
description: Weekly planning session - set priorities and plan the week ahead
---

# /wkplan - Weekly Planning Session

Forward-looking planning complement to `/report`. Review last week, set upcoming priorities.

## Instructions

### 1. Establish Date and Week
Run `date +%Y-%m-%d` and `date +%A` to get today's date and day.
Determine the current week (Sunday-Saturday for TWC, Monday-Sunday for general).

### 2. Review Last Week
Read the most recent report from `reports/` (if available).
If no report, scan the last 7 days of session logs from `sessions/`.

Summarize:
- What was accomplished
- What was planned but not done
- Any patterns (e.g., "spent 80% on job search, 10% on DSA, 10% on projects")

### 3. Review Goals and Current State
Read:
- `state/goals.md` — Are we on track?
- `state/current.md` — What's currently active?
- `state/habits.md` — How are habit streaks? (if file exists)
- `state/learning.md` — What topics need review? (if file exists)

### 4. Plan the Week

Present a draft plan:

```
## Week Plan: {date range}

### Top Priorities
1. {priority 1 — what and why}
2. {priority 2}
3. {priority 3}

### Goal Allocation
| Goal | Planned Sessions | Focus Areas |
|------|-----------------|-------------|
| Job Search | {N} | {specific actions} |
| DSA Study | {N} | {topics to cover/review} |
| Data Engineering | {N} | {what to learn/build} |
| D&D Project | {N} | {what to work on} |
| Recipe App | {N} | {what to work on} |
| Exercise | {N} | {schedule} |

### TWC Plan
- Activities needed this week: {N remaining}/4
- Planned activities:
  1. {activity}
  2. {activity}

### Learning Reviews Scheduled
- {topics due for review this week, from state/learning.md}

### Key Deadlines
- {any deadlines this week}
```

### 5. Get User Input
Ask the user:
- "Does this look right? Want to adjust any priorities?"
- "Any events or commitments I should know about?"

### 6. Save Plan
After user approval, save to `sessions/plans/{date}.md`.
Update `state/current.md` with new priorities.

### 7. Confirm
```
**Plan saved** for the week of {date range}.
Updated priorities in state/current.md.

Let's make it a good week!
```
