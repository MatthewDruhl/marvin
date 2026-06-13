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

### Step 1: Generate the Startup Packet

```bash
uv run python scripts/marvin_start.py --format text --create-twc-week-file
```

The packet is the deterministic foundation of the briefing. It contains:
- **Generated timestamp** — DAY, TODAY (YYYY-MM-DD), TIME, TZ. Use these throughout; never guess the day of week or compute dates yourself.
- **File contents** — `state/current.md`, `goals.md`, `commitments.json`, `todos.md` (legacy reference only, not source of truth), `habits.md`, `projects.md`, CLAUDE/AGENTS/context files, and today's (or the most recent) session log.
- **State file staleness** — last-updated date and age per state file, flagged past 3 days.
- **Commitments health** — overdue, review-due, and stale (7+ days untouched) active commitments with next actions.
- **Session gap** — days since the last session log.
- **Agent runs** — pending background-agent work from `state/agent-runs.json`: runs needing review, still running, or running suspiciously long. If the file is missing, create it from `context/agent-runs.example.json` (empty `runs` list).
- **TWC current week** — Sunday-Saturday window, week file path, activity row count. The `--create-twc-week-file` flag creates the week's CSV from the template if missing; never create it by hand.
- **Active application count** from `~/Resume/jobs/applications.md`.

Do not recompute anything the packet already provides. If the script fails, fall back to `date '+%A %Y-%m-%d %H:%M %Z'` plus manual file reads, and flag the failure in Skipped Checks.

### Step 2: Note Session Continuity

From the packet: if the session log source is `today`, we're resuming today's session — acknowledge what was already covered. If `session_gap_days` > 1, note the gap in the briefing. If `state/commitments.json` is missing, create it from `context/commitments.example.json`.

### Step 3: Check Gmail (delegated to gmail-triage subagent)

**Purpose:** Surface job responses, freelance/business communications, and new contacts proactively, without pulling raw email bodies into this session's context.

**Launch the subagent immediately after Step 1** so it runs while you work Steps 2 and 4 (cross-referencing is the first thing that needs its results):

```
Agent(
  subagent_type: "gmail-triage",
  description: "Gmail triage for startup briefing",
  prompt: today's date
        + active contact/client names (from the packet's current.md priorities)
        + active company names (if the packet shows active applications)
        + "contacts file: ~/Resume/jobs/contacts.md"
        + "session logs: ~/marvin/sessions/"
)
```

The agent owns the searches, newsletter filtering, already-saved dedup, and long-thread handling (#280-282, procedure in `.claude/agents/gmail-triage.md`). It returns structured findings: category, sender, summary, action, and full content only for items needing cross-reference. Trust its `noise` list; do not re-fetch noise items.

**Act, don't ask:** for findings the agent marks with an action (new contact, job response, client request), proceed in the main session without asking permission.

**Fallbacks:**
- `gmail-triage` agent type unavailable in this runtime → run the searches inline following the agent file's procedure (metadata first, filter noise, never full-fetch 3+ message threads).
- Gmail MCP tools unavailable entirely → no shell workarounds, no credential files; mark `Gmail: skipped (Google Workspace MCP unavailable in this runtime)` and continue.
- Calendar MCP tools unavailable → don't query Google Calendar; use `current.md` for today's events in Step 4 and add `Calendar: skipped` to Skipped Checks.

### Step 4: Cross-Reference and Quality Check

Analyze the packet contents from Step 1. Do NOT re-read state files. The mechanical facts (staleness ages, commitment health, TWC counts, session gap) are already in the packet; this step is the judgment layer on top.

**Freshness and drift:**
- Report packet staleness flags with age (e.g., "current.md last updated 9 days ago").
- Scan `current.md` for dates or deadlines that have already passed but are still phrased as upcoming (e.g., "Target: videos done by May 15" when today is May 21). This is prose the script can't parse; it's on you.

**Contradictions:**
- Compare priority descriptions in `current.md` against `goals.md` and `commitments.json`. Flag mismatches (e.g., different rejection counts, different project statuses).
- Check if any active commitment appears resolved per session logs, `current.md`, or Gmail findings.

**Cross-references:**
1. **Commitments vs. reality:** Compare the packet's overdue/review-due/stale commitments against Gmail findings and `current.md`. If a commitment is clearly resolved, prepare a `commitments.json` status update and note it in the briefing.
2. **Today's events:** Check `current.md` for anything scheduled today. Use TIME from the packet to mark each as upcoming or already passed.
3. **TWC week status:** Use the packet's `twc_current_week` (window, row count, file). Calculate days remaining to Saturday.
4. **Stale open threads:** Flag any open thread in `current.md` that hasn't been updated in 7+ days.
5. **New contacts from Gmail:** If Gmail surfaced a new job contact not in `~/Resume/jobs/contacts.md`, prepare to add them.

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

1. **TWC CSV:** Already handled by the Step 1 script (`--create-twc-week-file`). Note in the briefing if the packet says the file was created.
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

**Agent Runs:** (omit if ledger is empty)
- Needs review: {project}/{skill} — {task}; output: {PR URL or path}
- Running: {project}/{skill} — {task} (launched {date})
- Stale: {project}/{skill} — running since {date}, check if it died

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

The startup packet handles datetime, staleness, commitment health, and TWC mechanics. Before presenting the briefing, verify the judgment work:

- [ ] Did I run the startup script (not recompute dates/TWC/staleness by hand)?
- [ ] Did I launch gmail-triage right after Step 1 (or follow its procedure inline as fallback)?
- [ ] Did I check for past deadlines still phrased as upcoming, and contradictions between state files?
- [ ] Did I act on every agent finding with an action attached (not just list them)?
- [ ] Did I mark today's events as upcoming/passed based on current time?
- [ ] Did I avoid treating `state/todos.md` as the source of truth for active commitments?
- [ ] Did I avoid asking permission for reads that are part of the startup flow?
- [ ] Did I note which checks were skipped and why?

If any check fails, fix it before presenting.

---

*Skill created: 2026-01-22*
*Rewritten: 2026-04-28 — restored intelligence lost in CLAUDE.md V2 trim, added cross-referencing, Gmail, proactive actions, and self-verification*
*Updated: 2026-05-21 — merged quality loop into cross-reference step (no double-reads), removed duplicate .claude/commands/marvin.md (#249)*
*Updated: 2026-06-12 — wired Steps 1-2 to scripts/marvin_start.py; deterministic work (datetime, staleness, commitment health, TWC, session gap) moved to the script (#286)*
*Updated: 2026-06-12 — Step 3 delegated to gmail-triage subagent: metadata-first triage, newsletter filter, already-saved dedup, long-thread handling (#291, closes #280-282)*
