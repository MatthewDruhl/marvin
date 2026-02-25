---
name: habit-tracker
description: |
  Track daily habits with streak counting and completion rates. Supports exercise,
  DSA practice, coding, and custom habits. Displays in briefings and prompts at
  session end.
license: MIT
compatibility: marvin
metadata:
  marvin-category: personal
  user-invocable: false
  slash-command: null
  model: default
  proactive: true
---

# Habit Streak Tracker

Track daily habits, maintain streaks, and celebrate consistency.

## When to Use

- User says "did [habit] today" or "completed [habit]"
- User asks about streaks or habit status
- During daily briefing (display current streaks)
- During session end (prompt for habit completion)
- User wants to add or remove a habit

## Process

### Step 1: Identify Action
- **Log completion** → Mark habit done for today
- **Check status** → Show all streaks and rates
- **Add habit** → Add new habit section
- **End-of-session prompt** → Ask about unchecked habits

### Step 2: Read Current State
Read `state/habits.md` for current streak data.

### Step 3: Update Habit
For logging completion:
1. Set "Last Completed" to today's date
2. Update streak:
   - If yesterday was completed → increment Current Streak
   - If yesterday was missed → reset Current Streak to 1
3. Update Longest Streak if Current > Longest
4. Update This Week and This Month counts
5. Add row to Completion Log table

### Step 4: Update File
Write changes to `state/habits.md`.

### Step 5: Confirm
```
✓ [Habit] logged for today!
Current streak: [N] days | Longest: [N] days
This week: [N]/7
```

## Briefing Integration

When called from daily briefing:
```
**Habits:**
- Exercise: [streak] day streak ([week]/7 this week)
- DSA Practice: [streak] day streak ([week]/7 this week)
- Coding: [streak] day streak ([week]/7 this week)
```

## End-of-Session Integration

At session end, check which habits haven't been logged today:
```
**Before you go — did you do these today?**
- [ ] Exercise
- [ ] DSA Practice
- [x] Coding (logged earlier)
```

Wait for user response and log accordingly.

## Notes
- Streaks reset after 1 missed day
- Week runs Monday-Sunday for habit tracking
- Month counts reset on the 1st
- Celebrate milestones: 7 days, 14 days, 30 days, 60 days, 90 days

---

*Skill created: 2026-02-08*
