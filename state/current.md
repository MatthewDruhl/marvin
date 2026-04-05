# Current State

Last updated: 2026-04-05

## Active Priorities

1. **PMP Certification** — TIA course: 96/~200 videos. Sections 1-7 complete. Section 8 in progress (5/84). Active recall method ready. Also do section-level recall for Sections 1-7.
2. **Job search** — 3 active apps (Conduent, Iterable, Honor). Jelena (Iterable) gave resume feedback: quantify outcomes. Search strings at `content/jobs/search-strings.md`. No SRE roles, Java is weak.
3. **TWC weekly requirement (Apr 5 - Apr 11)** — 0/4 complete.
4. **Slack bot live** — Session continuity fixed (uses `--resume`). Reset command + markdown formatting. Next: heartbeat morning briefing.
5. **Truck service** — Monday Apr 7. Remind: driveshaft lube + engine air filter replacement + 10W-30 CK-4 only.

## Recent Updates
- **Resume skill: 8 bugs fixed** — Keyword matching, hardcoded contact info, duplicate estimation, banned word, military double-check, missing file handling, template docs, compact re-read. All via PRs with 66-test suite.
- **Resume skill: 5 doc cleanup PRs** — Stale paths, genericized examples, voice samples extracted, test comment, architecture refs. PRs #13, #19-#23 ready to merge.
- **Decisions log added** — `state/decisions.md` tracks key decisions with context.
- **Slack bot session fix** — Uses `--resume` instead of `--session-id`. DM threading fixed. Launchd service restarted.

## Open Threads

- **6 PRs to merge** — #13, #19, #20, #21, #22, #23
- **Iterable** — Jelena's resume feedback: quantify drift detection and Terraform consolidation outcomes
- **Honor** — 19 days. Getting stale.
- **Resume: tiered skills** — Finalize Primary/Secondary/Tools grouping
- **Resume: summary rewrite** — Drop "Looking for..." per hiring manager feedback
- **Heartbeat (next build)** — Morning briefing via Slack webhook
- **VR&E:** VA Form 28-1900 submitted Feb 24. Waiting for eligibility review.
- **Post-9/11 GI Bill:** VA Form 22-1990 submitted Mar 23. Expect response by ~Apr 22.
- **Learning reviews overdue:** 50+ Python topics, 29 PMP topics need review.
- **Generic resume skill** — Tabled. Needs PRD before code changes. Saved to memory.

## Projects

| Project | Status | Details |
|---------|--------|---------|
| PMP Certification | In Progress | 96 videos, Section 8 (5/84). Target: May 2026. |
| Job Search | 3 active apps | Conduent, Iterable, Honor. `content/jobs/applications.md` |
| TWC Reporting | Week Apr 5-11: 0/4 | `content/jobs/TWC/` |
| Slack Bot | Session fix deployed | `integrations/slack/bot.py`. Uses --resume. Launchd service. |
| Resume Builder | 8 bugs fixed, 66 tests | `skills/resume-editor/`. 6 PRs pending merge. |
| Truck | Monday Apr 7 | `2021Ram3500/service-tracker.md` |
| VR&E | Application submitted | VA benefits track |
| GI Bill (Ch. 33) | Application submitted | PMP exam reimbursement track |

---

*This file is updated by MARVIN at the end of each session.*
