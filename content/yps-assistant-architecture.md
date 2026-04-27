# YPS Assistant — Architecture Design

**Status:** Design complete — parked until post-PMP (June 2026)
**Related:** `content/cc-dashboard-concept.md` (dashboard UI layer)

---

## Overview

The YPS Assistant is an AI business partner for John & Kirk at YPS auto parts. Built on MARVIN's template system, each operator gets their own install with shared agents and independent state.

## Naming Convention

| Name | What It Is | Analogy |
|------|-----------|---------|
| **YPS Assistant** | The broader AI partner for John & Kirk | Like MARVIN is for Matt |
| **Dispatch** | The email pipeline agent (scan → claim → draft → review → send) | A specific agent within the assistant |
| **CC-DB** | The dashboard UI layer (future) | The frontend for any assistant |

**Dispatch** is an agent that runs inside the assistant — email is just the first capability. Agents are named for what they *do*, not who owns them, so future agents (inventory, etc.) don't conflict.

---

## Template Inheritance Chain

```
marvin-template (Sterling's base — github.com/SterlingChin/marvin-template)
  └── marvin-yps (Matt's YPS template, syncs from marvin-template)
        ├── John's install (syncs from marvin-yps)
        └── Kirk's install (syncs from marvin-yps)
```

**Single-source sync at every level.** Each `.marvin-source` points to exactly one upstream:
- `marvin-yps/.marvin-source` → `marvin-template`
- `john-marvin/.marvin-source` → `marvin-yps`
- `kirk-marvin/.marvin-source` → `marvin-yps`

**Matt is the gatekeeper.** Sterling's MARVIN updates don't flow to John/Kirk until Matt syncs marvin-yps and verifies nothing breaks YPS agents.

### Why This Design

~~Fork MARVIN~~ → Just install MARVIN. ~~Submodules~~ → Too much friction. ~~Single repo with MARVIN merged in~~ → Couples assistant to business logic. ~~Standard MARVIN install + separate YPS skills repo~~ → Requires multi-source sync, manual skill wiring on onboarding.

**Winner:** Template inheritance. `marvin-yps` IS a MARVIN install with YPS agents baked in. Onboarding = clone one repo. Sync = one command, one source. No multi-source complexity.

---

## Components

1. **marvin-yps template** — MARVIN base + YPS agents/skills + YPS CLAUDE.md customizations. Matt maintains this.
2. **Operator installs** — Clone of marvin-yps. Own state, sessions, memory. Fully independent.
3. **SQL Server** — Shared state, claim-based locking, audit trail. Already running in office.
4. **Dashboard** — Web UI with workflow buttons, status cards, claim visibility. SQL Server backend. (Post-PMP)
5. **Slack Bot** — Message the assistant from phone or home. Notifications, quick approvals, skill triggers. (Post-PMP)

---

## Claude Code File Organization

Agents, skills, and commands serve different purposes and live in different directories:

```
.claude/
├── agents/                  ← agent definitions (background workers)
│   ├── dispatch.md          ← email pipeline agent (scan, claim, draft)
│   └── inventory.md         ← future: eBay CRUD agent
├── commands/                ← slash commands (entry points)
│   ├── dispatch.md          ← /dispatch → triggers dispatch agent
│   └── review.md            ← /review → interactive draft approval
└── skills/                  ← reference knowledge (loaded into context)
    └── yps-knowledge/
        └── SKILL.md         ← parts catalog, response templates, DB schema
```

**Key distinction:**
- **Agents** (`.claude/agents/`) — self-contained background workers with their own context window. Named for what they *do*, not who owns them. Enables future agents without naming conflicts.
- **Commands** (`.claude/commands/`) — slash commands that invoke agents or interactive workflows.
- **Skills** (`.claude/skills/`) — reference material and supporting files loaded into context on demand.

---

## Operator Setup

```
John's install (cloned from marvin-yps)
├── CLAUDE.md            ← YPS business context (from template)
├── .marvin-source       ← points to marvin-yps (single source)
├── .claude/
│   ├── agents/
│   │   └── dispatch.md  ← email pipeline agent definition
│   ├── commands/
│   │   ├── dispatch.md  ← /dispatch slash command
│   │   └── review.md    ← /review slash command
│   └── skills/
│       └── yps-knowledge/
│           └── SKILL.md ← parts catalog, templates, DB schema
├── state/               ← John's private state
├── sessions/            ← John's private logs
└── .env                 ← OPERATOR=john, SQL_CONN=...

Kirk's install (same structure, own state)
```

### Agent vs Command vs Skill Classification

| Name | Type | Location | Why |
|------|------|----------|-----|
| `dispatch` | **Agent** | `.claude/agents/dispatch.md` | Background worker: scan Gmail, claim emails, draft responses, write to SQL. Own context window. |
| `/dispatch` | **Command** | `.claude/commands/dispatch.md` | Entry point that triggers the dispatch agent in background. |
| `/review` | **Command** | `.claude/commands/review.md` | Interactive: show drafts, get approval, send. Stays in conversation. |
| `yps-knowledge` | **Skill** | `.claude/skills/yps-knowledge/SKILL.md` | Parts catalog, response templates, DB schema. Loaded into context on demand. |
| `inventory` (future) | **Agent** | `.claude/agents/inventory.md` | Bulk eBay API operations. Isolated background work. |

---

## Dispatch Pipeline (Background Agent + SQL Locking)

**`/dispatch`** command triggers the `dispatch` agent in background:

```
/dispatch  →  .claude/agents/dispatch.md (background)
              ├── connects to SQL Server
              ├── loads yps-knowledge skill (parts catalog, templates)
              ├── scans Gmail for new inbound
              ├── INSERTs new emails (status=queued, claimed_by=NULL)
              ├── claims unclaimed for this operator
              │   (atomic: UPDATE ... WHERE claimed_by IS NULL)
              ├── drafts responses for claimed emails
              ├── writes drafts to SQL
              ├── notifies operator (Slack/dashboard)
              │   "3 drafts ready for review"
              └── done
```

**`/review`** is a separate interactive command (not an agent):

```
/review   →  .claude/commands/review.md (interactive, in conversation)
              ├── pulls drafts from SQL (filtered by OPERATOR)
              ├── shows drafts for approval
              ├── operator approves/edits
              ├── sends approved emails
              └── marks complete in SQL
```

**Two-step by design.** Background agent does the heavy lifting. Review is human-in-the-loop. No long-lived agent waiting for input.

**Evolution path:**
1. **Now:** `/dispatch` runs on demand, `/review` is manual
2. **Later:** dispatch gains confidence scoring — high-confidence drafts auto-send
3. **Eventually:** dispatch runs on a schedule (`/loop` or `/schedule`), review only for edge cases

---

## Multi-Operator Architecture

**Problem:** Two operators, one inbox, shared resources. Need concurrency control.

**Solution:** Claim-based locking via SQL Server (already running in YPS office).
- Each email gets claimed by whoever scans/touches it first
- Atomic UPDATE with `WHERE claimed_by IS NULL` prevents race conditions
- Each assistant only shows/works on emails claimed by its operator
- Optional: expiring claims (auto-release after 2 hours of inactivity)

**Infrastructure:** SQL Server already on office LAN. No cloud costs. No new infra.

### SQL Server Schema

```sql
emails:
  email_id (PK), from_addr, subject, date_received, category,
  status (queued/drafting/drafted/approved/sent/skipped/flagged),
  claimed_by (john/kirk/NULL), claimed_at, draft_text, created_at

archive:
  email_id (PK), from_addr, subject, category, final_status,
  date_completed, handled_by

feedback:
  id (PK), email_id (FK), original_draft, edited_draft,
  changes_summary, edited_at, edited_by
```

---

## Sync Flow

**Sterling updates MARVIN:**
1. Matt syncs `marvin-yps` from `marvin-template`
2. Matt tests — verifies YPS agents still work
3. Matt commits/pushes to `marvin-yps`
4. John/Kirk run `/sync` → get both MARVIN updates and any YPS agent changes

**Matt builds a new YPS agent:**
1. Matt builds and tests in `~/Projects/marvin-yps`
2. Commits to `marvin-yps` template
3. John/Kirk run `/sync` → new agent appears

**John/Kirk tweak something** (e.g., email template):
1. Run `/yps-commit` → assistant creates branch in marvin-yps, commits, opens PR
2. Matt reviews → merges
3. Everyone gets it on next `/sync`

**No one touches git directly. The assistant IS the git interface.**

---

## Access Layers

| Who | Where | Interface |
|-----|-------|-----------|
| John (office) | Desktop | Dashboard or Claude Code terminal |
| Kirk (office) | Desktop | Dashboard |
| John (home/phone) | Mobile/laptop | Slack bot |
| Kirk (home/phone) | Mobile/laptop | Slack bot |

---

## Session Handoff (Future Feature)

**Problem:** Can't hand off a live Claude Code session to Slack or dashboard. Each interface starts fresh.
**Opportunity:** YPS Assistant should support seamless handoff between interfaces — terminal → Slack → dashboard. State files + SQL Server carry continuity, but the active conversation context is lost.
**Possible approach:** On handoff, serialize the current conversation summary to a shared location (SQL Server or state file). The receiving interface loads it as context. Not seamless replay, but close enough.

---

## Why This Wins

- **Decoupled** — Assistants are independent. YPS is just an agent set, not the system.
- **No new patterns** — Uses MARVIN's existing `/sync` mechanism. Nothing new to learn.
- **Portable** — If MARVIN goes open-source, YPS is a proof case: "here's how a real business plugged in domain agents."
- **Survivable** — Remove the YPS agents and the assistant still works. Remove the assistant and YPS agents repo still exists.
- **Non-technical friendly** — John and Kirk never touch git. The assistant handles everything.

---

## Open Questions

- **GitHub issues migration:** Decided Option C — leave issues in `MatthewDruhl/yps`. That repo becomes the legacy codebase archive. New assistant-level issues go in `marvin-yps` when it exists. **Before starting marvin-yps:** triage and clean up open yps issues (target: week of 2026-04-27).
- **SQL Server info:** Waiting on John (yps#74) for version/architecture details.

---

## Decision History

| Date | Decision | Superseded By |
|------|----------|---------------|
| 2026-04-24 AM | Single YPS repo with MARVIN patterns merged in | Option 4+5 |
| 2026-04-24 AM | Option 4+5: MARVIN fork + YPS submodule | Standard installs |
| 2026-04-24 PM | Standard MARVIN installs + YPS as skill package + multi-source `/sync` | Template inheritance |
| 2026-04-25 | Template inheritance + single-source sync + skill/agent classification | Corrected file org |
| 2026-04-26 | **Current:** Agents in `.claude/agents/`, commands in `.claude/commands/`, skills in `.claude/skills/`. Agent named `dispatch` (function, not company). Doc split from cc-dashboard-concept.md. | — |

*Created: 2026-04-24 — Updated: 2026-04-26 — Revisit after PMP exam*
