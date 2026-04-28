---
name: marvin
description: |
  Start MARVIN session with briefing. Use when user types /marvin or starts a new session. Loads context, reviews state, checks Gmail, gives daily briefing.
license: MIT
compatibility: marvin
metadata:
  marvin-category: session
  user-invocable: true
  slash-command: /marvin
  model: default
  proactive: false
---

# Session Start Skill

Start MARVIN session with full context loading, Gmail check, cross-referencing, and daily briefing.

## When to Use

- When user types `/marvin`
- At the start of any Claude Code session in the MARVIN directory
- When resuming work after a break

## Process

### Step 1: Establish Current Date and Time
```bash
date '+%A %Y-%m-%d %H:%M %Z'
```
Store full output. Extract:
- `DAY` — day of week (e.g., Tuesday)
- `TODAY` — YYYY-MM-DD for file naming
- `TIME` — HH:MM for event-aware reasoning
- `TZ` — timezone for clarity

Use throughout the briefing. If events are scheduled today, compare against TIME to determine upcoming vs. already passed. Never guess the day of week from the date.

### Step 2: Load Context

Read these files (parallelize where possible):
1. `state/current.md` — Current priorities, open threads, scheduled events
2. `state/goals.md` — Goals and progress tracking
3. `state/todos.md` — Active todos and follow-ups
4. `state/habits.md` — Habit streaks
5. `sessions/{TODAY}.md` — If exists, we're resuming today's session
6. If no today file, read the most recent file in `sessions/` for continuity

### Step 3: Check Gmail

**Purpose:** Surface job responses and new contacts proactively.

1. Read `~/Resume/jobs/applications.md` for active company names
2. Search Gmail for emails from those companies (last 7 days)
3. Search Gmail for job keywords: "application", "interview", "thank you for applying" (last 7 days)
4. **Act, don't ask:** If results include unrecognized senders or new job-related emails, pull the full content immediately. Do NOT ask permission to read — just read and include findings in the briefing.
5. For email threads (introductions, recruiter outreach), pull the full thread to understand context

### Step 4: Cross-Reference and Resolve

Before presenting the briefing, check for contradictions and resolutions across loaded state:

1. **Follow-ups vs. reality:** Compare `state/todos.md` follow-ups against Gmail findings and `state/current.md`. If a follow-up is clearly resolved by current state (e.g., "wait for VA contact" but an orientation is already scheduled), mark it resolved in `todos.md` and note in the briefing.
2. **Today's events:** Check `state/current.md` for anything scheduled today. Use TIME from Step 1 to mark each as upcoming (include time remaining) or already passed.
3. **TWC week status:** Determine current TWC week (Sun-Sat). Check if a CSV exists for this week. Count activities logged. Calculate days remaining.
4. **Stale open threads:** Flag any open thread in `state/current.md` that hasn't been updated in 7+ days.
5. **New contacts from Gmail:** If Gmail surfaced a new job contact not in `content/jobs/contacts.md`, prepare to add them.

### Step 5: Sync Learning Tracker

1. Read `~/Code/Learning/topics-learned.md`
2. Compare against `state/learning.md` using dedup rules from CLAUDE.md
3. Add new topics:
   - `Issues Needing More Guidance` → confidence 1/5
   - `Topics Covered` and `Key Concepts Practiced` → confidence 2/5
4. If new topics were added, include a summary in the briefing
5. If nothing new, skip silently

### Step 6: Take Proactive Actions

Act on findings from Steps 3-5 before presenting the briefing:

1. **TWC CSV:** If a new week started and no CSV exists, create it
2. **Contacts:** If Gmail found a new job contact, add to `content/jobs/contacts.md`
3. **TWC logging:** If Gmail found a networking event or job search activity, log to current week's TWC CSV
4. **Follow-up resolution:** If Step 4 resolved any follow-ups, write the updates to `todos.md`

Note what actions were taken — include in the briefing.

### Step 7: Present Briefing

Compile everything into a concise briefing:

```
{Greeting based on time of day}. It's {Day}, {Date}, {Time} {TZ}.

**Today's Schedule:**
- {Time} — {Event} (in X minutes / X hours ago)

**Top Priorities:**
1. {Priority 1}
2. {Priority 2}
3. {Priority 3}

**Job Search:**
- Active apps: {count} ({names})
- Gmail: {new responses or "no new responses"}
- TWC: {X}/4 for the week (due Saturday)

**Alerts:**
- {Follow-ups resolved}
- {New contacts added}
- {Deadlines approaching}
- {Stale threads}

**Learning:**
- {New topics synced, or omit if none}

How can I help today?
```

**Formatting rules:**
- If resuming today's session, acknowledge what was already covered
- Omit empty sections (no "Alerts: none")
- Keep concise — offer details on request
- Use time-relative language ("in 53 minutes", "2 hours ago") for today's events

## Self-Verification Checklist

After completing all steps but BEFORE presenting the briefing, verify:

- [ ] Did I use full datetime (day, date, time, timezone)?
- [ ] Did I check todos.md follow-ups for anything already resolved?
- [ ] Did I pull full content for any new job-related emails (not just flag them)?
- [ ] Did I mark today's events as upcoming/passed based on current time?
- [ ] Did I check/create the TWC weekly CSV?
- [ ] Did I avoid asking permission for reads that are part of the startup flow?
- [ ] Did I cross-reference state files against each other for contradictions?

If any check fails, fix it before presenting.

---

*Skill created: 2026-01-22*
*Rewritten: 2026-04-28 — restored intelligence lost in CLAUDE.md V2 trim, added cross-referencing, Gmail, proactive actions, and self-verification*
