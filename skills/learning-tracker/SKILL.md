---
name: learning-tracker
description: |
  Track learning progress with spaced repetition. Manages DSA and Data Engineering
  topics with confidence ratings and review schedules. Surfaces due reviews in
  daily briefings.
license: MIT
compatibility: marvin
metadata:
  marvin-category: learning
  user-invocable: false
  slash-command: null
  model: default
  proactive: true
---

# Learning Progress Tracker

Track topics with spaced repetition for effective long-term retention.

## When to Use

- User says "I reviewed [topic]" or "practiced [topic]"
- User says "add [topic] to learning tracker"
- User asks "what should I review?" or "what's due for review?"
- During daily briefing (surfaces overdue/due topics)
- User says "update confidence for [topic]"

## Process

### Step 1: Identify Action
Parse what the user wants:
- **Review completed** → Update last reviewed date, advance interval based on confidence
- **Add topic** → Add new row with 1/5 confidence, 1-day interval, next review = tomorrow
- **Check due** → Read state/learning.md, find overdue and due-today items
- **Update confidence** → Change confidence rating, adjust interval accordingly

### Step 2: Read Current State
Read `state/learning.md` to get current topic data.

### Step 3: Update Topic
For review completed:
1. Ask for confidence rating (1-5) or infer from context
2. Update "Last Reviewed" to today
3. Calculate next interval:
   - Confidence 1-2: Reset to 1-day interval
   - Confidence 3-4: Advance to next interval (1→3→7→14→30)
   - Confidence 5: Set to 30-day interval
4. Update "Next Review" date
5. Update "Status" column

### Step 4: Update File
Write changes to `state/learning.md` with updated timestamp.

### Step 5: Confirm
Show what was updated:
```
Updated: [Topic]
Confidence: [old] → [new]
Next review: [date] ([interval])
```

## Briefing Integration

When called from daily briefing, return:
```
**Learning Reviews Due:**
- 🔴 Overdue: [topics past due date]
- 🟡 Due Today: [topics due today]
- 🟢 Upcoming: [next 3 days]
```

## Notes
- Spaced repetition intervals: 1, 3, 7, 14, 30 days
- Topics are grouped by category (DSA, Data Engineering, etc.)
- Confidence scale: 1 (can't recall) to 5 (mastered)
- Syncs to Obsidian Learning/ folder when obsidian-sync runs

---

*Skill created: 2026-02-08*
