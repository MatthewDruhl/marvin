---
name: job-tracking
description: |
  Track job applications, log work search activities, and manage the weekly TWC
  requirement. Use when the user reports applying for a job, mentions a job search
  activity, asks about TWC progress, or when Gmail surfaces application responses.
license: MIT
compatibility: marvin
metadata:
  marvin-category: career
  user-invocable: false
  proactive: true
---

# Job Tracking Skill

Procedures for tracking applications, logging work search activities, and meeting the Texas Workforce Commission (TWC) weekly reporting requirement.

Data boundaries: live job-search data lives in `~/Resume/jobs/` (outside the repo); only sanitized examples, search strings, and TWC tooling live in `content/jobs/` (generated TWC CSVs/PDFs are gitignored). See `PRIVACY.md`. When in doubt, put live data under `~/Resume/jobs/`.

## Files

- **`~/Resume/jobs/applications.md`** — Active applications with current status
- **`~/Resume/jobs/opportunities.md`** — Roles to research and apply for
- **`~/Resume/jobs/interview-prep/`** — Question banks, mock sessions, company research
- **`~/Resume/jobs/research/`** — Job posting analysis, match scores, salary research, search session outputs (personal evaluation data, never in repo)
- **`~/Resume/jobs/contacts.md`** — Recruiter conversations and follow-ups (personal data, never in repo)
- **`content/jobs/contacts.md.example`** — Sanitized contact example only
- **`content/jobs/TWC/`** — Official TWC reporting (CSV format, gitignored)
  - `job-application-tracker.csv` — Master list of all applications
  - `work-search-week-*.csv` — Weekly activity logs (4 required per week)

## Job Research Workflow

When analyzing a job posting, researching a company, or running a job search session: save output to `~/Resume/jobs/research/` (never to `content/jobs/`). This includes match scorecards, salary context research, and search session summaries.

**File naming:** `{company}-{role}-{jobid}.md` for posting analyses, `{company}-search-{YYYY-MM-DD}.md` for broader searches.

## Tracking New Applications

**Required from user:** URL, Company, Job Title (minimum)

**Optional but useful:** Salary range, location (remote/hybrid/onsite), tech stack, applied via (FlexJobs, LinkedIn, direct, etc.)

**User says:** "applied for [Job Title] at [Company] [URL]" or similar

**Steps:**
1. Add to `~/Resume/jobs/applications.md` with status "Application submitted"
2. Add to `content/jobs/TWC/job-application-tracker.csv` for official reporting
3. Add to current week's `work-search-week-*.csv` (create new week file if needed)
4. If optional details weren't provided, try fetching from URL to fill in salary, location, tech stack
5. Confirm what was added + TWC progress for the week

## Logging Job Search Activities

**User says:** "job search: [what they did]"

**Steps:**
1. Add to current week's `work-search-week-*.csv`
2. Track progress toward 4/week TWC requirement
3. Confirm logging

**Valid activities:** Applied for job, Interview, Follow-up email, Searched online, Job fair, Networking event, Career counseling

**Not valid:** Training/Coursera is NOT a valid TWC work search activity. Log training under the habit tracker (Coding), not TWC CSVs.

## Gmail Response Checking

**When:** At every `/marvin` session start (automatic; see `skills/marvin/SKILL.md` Step 3)

**Steps:**
1. Search Gmail for emails from companies in `~/Resume/jobs/applications.md`
2. Search for keywords: "application", "interview", "thank you for applying"
3. Report any new responses
4. Ask if user wants to update application statuses
5. Update both markdown and CSV files as needed

## Weekly TWC Requirement

- **Required:** 4 job search activities per week
- **Week runs:** Sunday - Saturday
- **Week files named by:** Starting Sunday date in full ISO format (e.g., `work-search-week-2026-01-25.csv`), matching `twc_week_filename()` in `scripts/marvin_start.py`
- **Track:** Activities logged; remind when approaching deadline
- **Create:** New weekly CSV when needed (named with the week's Sunday date); copy the header from `content/jobs/TWC/weekly-work-search-template.csv`
- **Deadline:** End of Saturday to complete 4 activities for the week
- **New week starts:** Sunday (requires new CSV file)

**Important:** Always verify the current day of week when discussing deadlines. Use `date +%A` to confirm. Never assume the day based on the date alone.

---

*Skill created: 2026-06-12 — procedures moved from CLAUDE.md per instruction-ownership rules (marvin#290)*
