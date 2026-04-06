---
name: daily-briefing
description: |
  Generate daily briefing with priorities, progress, and alerts. Used as part of session-start or when user asks "what's on today". Internal skill supporting the marvin skill.
license: MIT
compatibility: marvin
metadata:
  marvin-category: session
  user-invocable: false
  slash-command: null
  model: default
  proactive: false
---

# Daily Briefing Skill

Generate comprehensive daily briefing with priorities, progress, and alerts.

## When to Use

- Part of `marvin` skill (session start)
- User asks "what's on today" or "daily briefing"
- Morning check-in requests

## Process

### Step 1: Calendar Overview
Check if Google Workspace MCP is available. If so:
1. Use Google Workspace MCP tools to query today's calendar events
2. Also check tomorrow's events for preview
3. Look ahead 7 days for important deadlines or meetings

If Google Workspace MCP is NOT available:
- Skip this step silently
- Note: User can set up Google Calendar access via `.marvin/integrations/google-workspace/setup.sh`

Display format:
```
**Today's Schedule:**
- {time}: {event}
- {time}: {event}

**Tomorrow:** {preview of events}
**This Week:** {any notable upcoming events}
```

If no events found, display: "No calendar events today."

### Step 2: Task Status
From `state/current.md`:
- Active priorities
- Overdue items
- Due today
- Open threads needing attention

### Step 3: Progress Check
For current month from `state/goals.md`:
- Progress against each goal
- Days remaining in month

If behind pace, flag it.

### Step 4: Open Threads
From `state/current.md`:
- Anything waiting on follow-up
- Stale threads (no update > 5 days)

### Step 5: Proactive Suggestions
Based on patterns:
- "You haven't made progress on {goal} this week"
- "Deadline for {item} is in 3 days"
- "Monthly review coming up — want to schedule?"

### Step 6: Learning Reviews Due
From `state/learning.md`:
- List overdue topics (past their Next Review date)
- List topics due today
- List topics coming up in next 3 days
- If overdue count > 3, flag as needing attention

### Step 7: Habit Streaks
From `state/habits.md`:
- Show current streak for each active habit
- Show this week's completion rate
- Celebrate streak milestones (7, 14, 30, 60, 90 days)
- Flag if any habit streak is about to break (not logged yesterday)

### Step 8: Application Follow-Up Reminders
From `~/Resume/jobs/applications.md`:
- Calculate days since each active application was submitted
- Surface applications pending 7+ days with no status change:
  ```
  **Follow-Up Reminders:**
  - [Company] - [Role]: Applied [N] days ago — consider following up
  - [Company] - [Role]: Applied [N] days ago — consider following up
  ```
- For applications 14+ days old, suggest drafting a follow-up email
- If Gmail MCP is available, offer to draft follow-up email (always confirm with user before sending)
- Skip applications already marked as "Follow-up sent" or "Rejected"

## Output Format

Keep concise. Structure as:
```
## {Day}, {Date}

**Today**: {summary}

**Alerts**:
- {any urgent items}

**Progress**: {goal status summary}

**Learning Reviews Due:**
- 🔴 Overdue: {topics past due date}
- 🟡 Due Today: {topics due today}
- 🟢 Upcoming: {next 3 days}

**Habits:**
- Exercise: {streak} day streak ({week}/7 this week)
- DSA Practice: {streak} day streak ({week}/7 this week)
- Coding: {streak} day streak ({week}/7 this week)

**Focus**: {top 1-2 priorities}
```

Offer to expand any section on request.

---

*Skill created: 2026-01-22*
