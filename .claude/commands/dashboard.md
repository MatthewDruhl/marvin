---
description: Show project momentum dashboard with activity and staleness
---

# /dashboard - Project Momentum Dashboard

Single-view showing all projects with activity, staleness, and next actions.

## Instructions

### 1. Establish Date
Run `date +%Y-%m-%d` to get today's date.

### 2. Gather Project Data
Read these files:
- `state/current.md` — Active priorities and project statuses
- `state/goals.md` — Goal progress
- `content/dnd-project.md` — D&D project details
- `content/recipe-app.md` — Recipe app details
- `~/Resume/jobs/applications.md` — Job search activity

### 3. Scan Session Logs for Activity
Read recent session logs from `sessions/` to determine:
- Last activity date per project (when was it last mentioned/worked on?)
- Sessions per week per project (velocity)
- What was done in the most recent session for each project

### 4. Compute Staleness
For each project:
- **Active** (✅): Activity within last 3 days
- **Idle** (🟡): 4-7 days since last activity
- **Stale** (🔴): 7+ days since last activity
- **Dormant** (⚫): 14+ days since last activity

### 5. Display Dashboard

```
## Project Momentum Dashboard
*As of {date}*

| Project | Status | Last Active | Staleness | Velocity | Next Action |
|---------|--------|-------------|-----------|----------|-------------|
| D&D Character Sheet | Phase 3 ✅ | {date} | {icon} {N} days | {N} sessions/wk | {next step} |
| Recipe Book App | Phase 1 API ✅ | {date} | {icon} {N} days | {N} sessions/wk | {next step} |
| Job Search | Active | {date} | {icon} {N} days | {N} sessions/wk | {next step} |
| DSA Study | In Progress | {date} | {icon} {N} days | {N} sessions/wk | {next step} |
| Data Engineering | In Progress | {date} | {icon} {N} days | {N} sessions/wk | {next step} |

### Attention Needed
- {any stale or dormant projects with suggestions}

### This Week's Focus
- {top 2-3 priorities based on goals and staleness}
```

### 6. Offer Actions
Suggest:
- "Want to work on [stale project] today?"
- "Should we update the status of [project]?"
- "Want a deeper dive into any project?"
