---
description: Analyze session logs to show time spent, topic frequency, and goal alignment
---

# /analytics - Session Analytics & Trends

Analyze session history to reveal patterns, time allocation, and goal alignment.

## Instructions

### 1. Establish Time Range
Default: Current month. User can specify:
- `/analytics` → This month
- `/analytics last month` → Previous month
- `/analytics all` → All available data

### 2. Gather Session Data
Read all session logs in the time range:
- `sessions/` for current sessions
- `sessions/archive/YYYY-MM/` for archived sessions

For each session, extract:
- Date and approximate duration (based on content volume)
- Topics discussed (from ### Topics sections)
- Projects worked on
- Decisions made
- Content shipped

### 3. Analyze Patterns

#### Topic Frequency
Count mentions of each goal area across sessions:
- Job Search (applications, interviews, TWC, resume)
- DSA Study (algorithms, data structures, sorting, searching)
- Data Engineering (PostgreSQL, FastAPI, Docker, SQL)
- D&D Project (MCP, character sheet, combat engine)
- Recipe App (API, frontend, AWS)
- Exercise/Health
- MARVIN/Meta (setup, configuration, skills)

#### Goal Alignment
Compare stated goals (from `state/goals.md`) against actual time spent:
- Which goals get the most attention?
- Which goals are neglected?
- Is behavior aligned with stated priorities?

#### Productivity Patterns
- Sessions per week (trend)
- Most productive days of week
- Shipped items count
- Decision velocity

### 4. Generate Report

```
## Session Analytics: {month/range}

### Summary
- Total sessions: {N}
- Active days: {N} out of {N} possible
- Items shipped: {N}

### Time Allocation (by goal area)
| Goal Area | Sessions | % of Total | Trend |
|-----------|----------|-----------|-------|
| Job Search | {N} | {%} | {↑↓→} |
| DSA Study | {N} | {%} | {↑↓→} |
| Data Engineering | {N} | {%} | {↑↓→} |
| D&D Project | {N} | {%} | {↑↓→} |
| Recipe App | {N} | {%} | {↑↓→} |
| Exercise | {N} | {%} | {↑↓→} |

### Goal Alignment
**Stated Priority → Actual Time:**
- {goal}: {alignment assessment}

### Insights
- {pattern 1}
- {pattern 2}
- {suggestion for rebalancing}

### Productivity Trend
- Sessions/week: {trend over weeks}
- Most active days: {days}
```

### 5. Save Report
Save to `reports/analytics-{YYYY-MM}.md`.

### 6. Offer Insights
Highlight the most actionable finding:
- "You've been spending 60% on job search but only 5% on DSA — want to rebalance?"
- "Your most productive day is Tuesday — consider scheduling deep work then."
