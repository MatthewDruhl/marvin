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
3. `state/commitments.json` — Local source of truth for active commitments, due dates, review dates, owners, and next actions. If missing, create it from the structure in `context/commitments.example.json`.
4. `state/todos.md` — Legacy human-readable reference; do not treat as source of truth for active commitments
5. `state/habits.md` — Habit streaks
6. `state/projects.md` — Project registry (repos, branches, PRs, issues)
6. `sessions/{TODAY}.md` — If exists, we're resuming today's session
7. If no today file, read the most recent file in `sessions/` for continuity

### Step 3: Check Gmail

**Purpose:** Surface job responses, freelance/business communications, and new contacts proactively.

Before searching, verify Google Workspace MCP tools are available in the current runtime. Project `.mcp.json` may not be loaded automatically outside Claude Code.

If Calendar MCP tools are unavailable, do not query Google Calendar. Use `current.md` for today's events in Step 4 and add `Calendar: skipped (Google Workspace MCP unavailable in this runtime)` to Skipped Checks.

If Gmail MCP tools are unavailable:

1. Do not attempt shell workarounds or read credential files.
2. Mark Gmail checks as skipped with the reason, e.g. `Gmail: skipped (Google Workspace MCP unavailable in this runtime)`.
3. Continue the rest of the startup flow.

If Gmail MCP tools are available:

#### 3a: Active contacts and clients
1. Read `state/current.md` Active Priorities for freelance client names and key contacts (e.g., Ryan, Bryan, Jana, Doug, Bob, Michael Bond)
2. Search Gmail for emails from each active freelance/business contact by name (last 7 days)
3. Pull full content for any new emails from these contacts

#### 3b: Job search
1. Read `~/Resume/jobs/applications.md` for active company names
2. If active apps exist, search Gmail for emails from those companies (last 7 days)
3. If active apps exist, search Gmail for job keywords: "application", "interview", "thank you for applying" (last 7 days)

#### 3c: Recruiter outreach
1. **Always run (even with 0 active apps):** Search Gmail for recruiter outreach (last 7 days). Use keywords: "opportunity", "role", "position", "candidate". Cross-reference senders against `~/Resume/jobs/contacts.md`. Flag emails from new senders.
2. **Always run:** Search spam for job-related emails (last 7 days)

#### 3d: Act on findings
1. **Act, don't ask:** If results include unrecognized senders or new job-related emails, pull the full content immediately. Do NOT ask permission to read — just read and include findings in the briefing.
2. For email threads (introductions, recruiter outreach), pull the full thread to understand context

### Step 4: Cross-Reference and Quality Check

Analyze the state files already loaded in Step 2. Do NOT re-read them. The goal is to catch drift, contradictions, and stale data so the briefing reflects reality.

**Freshness and drift:**
- Check the `Last updated:` line in each state file. Flag any not updated in the last 3 days with age (e.g., "current.md last updated 9 days ago").
- Scan `current.md` for dates or deadlines that have already passed but are still phrased as upcoming (e.g., "Target: videos done by May 15" when today is May 21).

**Contradictions:**
- Compare priority descriptions in `current.md` against `goals.md` and `commitments.json`. Flag mismatches (e.g., different rejection counts, different project statuses).
- Check if any active commitment appears resolved per session logs, `current.md`, or Gmail findings.

**Cross-references:**
1. **Commitments vs. reality:** Compare active commitments against Gmail findings and `current.md`. If a commitment is clearly resolved, prepare a `commitments.json` status update and note it in the briefing.
2. **Today's events:** Check `current.md` for anything scheduled today. Use TIME from Step 1 to mark each as upcoming or already passed.
3. **TWC week status:** Determine current TWC week (Sun-Sat). Check if a CSV exists for this week. Count activities logged. Calculate days remaining.
4. **Stale open threads:** Flag any open thread in `current.md` that hasn't been updated in 7+ days.
5. **New contacts from Gmail:** If Gmail surfaced a new job contact not in `~/Resume/jobs/contacts.md`, prepare to add them.
6. **Commitment health:** From `commitments.json`, flag overdue commitments, commitments with `review_after` today or earlier, and commitments whose `last_touched` is more than 7 days old unless status is `waiting`, `done`, or `dropped`.

**Session gap:**
- Calculate the gap between today and the most recent session log.
- If gap > 1 day, note the gap in the briefing (e.g., "3 days since last session"). Context is already in `current.md` Recent Updates.
- If resuming today's session, skip this.

**Confidence tracking:**
- Track which checks succeeded and which could not complete (e.g., Gmail MCP unavailable, no active applications).
- In the briefing, distinguish confirmed facts from skipped checks. Format: "(skipped: reason)".

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
2. **Contacts:** If Gmail found a new job contact, add to `~/Resume/jobs/contacts.md`
3. **TWC logging:** If Gmail found a networking event or job search activity, log to current week's TWC CSV
4. **Commitments:** If Step 4 resolved, changed, or discovered commitments, preview the `commitments.json` changes before writing. Do not scatter new active commitments into `todos.md`.

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
- Gmail: {new responses or "no new responses"} {or "(skipped: reason)"}
- TWC: {X}/4 for the week (due Saturday)

**Commitments:**
- Overdue: {title} — due {date}; next action: {next_action}
- Review today: {title} — next action: {next_action}
- Stale: {title} — last touched {date}

**Alerts:**
- {Stale state files with age: "current.md last updated 9 days ago"}
- {Past deadlines still phrased as future}
- {Contradictions between state files}
- {Commitments resolved or updated}
- {New contacts added}
- {Stale open threads}

**Learning:**
- {New topics synced, or omit if none}

**Skipped Checks:** (omit if all checks completed)
- {Check name}: {reason it was skipped}

How can I help today?
```

**Formatting rules:**
- If resuming today's session, acknowledge what was already covered
- Omit empty sections (no "Alerts: none", no "Commitments" if nothing is actionable, no "Skipped Checks" if all passed)
- Keep concise — offer details on request
- Use time-relative language ("in 53 minutes", "2 hours ago") for today's events
- Alerts should be actionable. "current.md is 9 days stale" is useful. "Everything looks fine" is not.

## Self-Verification Checklist

After completing all steps but BEFORE presenting the briefing, verify:

- [ ] Did I use full datetime (day, date, time, timezone)?
- [ ] Did I run quality checks (staleness, past deadlines, contradictions) on already-loaded state files?
- [ ] Did I check `commitments.json` for overdue, review-due, stale, or resolved commitments?
- [ ] Did I pull full content for any new job-related emails (not just flag them)?
- [ ] Did I mark today's events as upcoming/passed based on current time?
- [ ] Did I check/create the TWC weekly CSV?
- [ ] Did I avoid treating `state/todos.md` as the source of truth for active commitments?
- [ ] Did I avoid asking permission for reads that are part of the startup flow?
- [ ] Did I note which checks were skipped and why?

If any check fails, fix it before presenting.

---

*Skill created: 2026-01-22*
*Rewritten: 2026-04-28 — restored intelligence lost in CLAUDE.md V2 trim, added cross-referencing, Gmail, proactive actions, and self-verification*
*Updated: 2026-05-21 — merged quality loop into cross-reference step (no double-reads), removed duplicate .claude/commands/marvin.md (#249)*
