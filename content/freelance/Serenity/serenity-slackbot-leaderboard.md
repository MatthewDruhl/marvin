# Serenity Insurance Group - Slackbot Leaderboard

**Client:** Michael Bond, Founder & CEO
**Company:** Serenity Insurance Group
**Referral:** John Eimer
**Status:** In progress. Scope confirmed, POC deployed, refactor needed.
**Price:** $500 flat
**Repo:** `MatthewDruhl/serenity-slackbot` (private), at `~/Projects/serenity-slackbot/`

---

## Confirmed Scope (from May 19 Zoom call)

### What's Being Built
A Slack bot that reads agent production data from two Google Sheets and posts a combined leaderboard to a dedicated Slack channel. Ranked by total production value (money), with application counts also shown.

### Data Sources
Two Google Sheets (Matt has viewer access to both). Both verified from downloaded XLSX files on 2026-05-19. Detailed layout docs are in the project repo at `docs/sheet-layout.md`.

- **Sheet 1: Life Insurance & Annuities** -- 18 agents, 2 product sections
- **Sheet 2: Medicare & Ancillary** -- 28 agents, 4 product sections

### Leaderboard Display
- **Current month** totals (resets to 0 at month end)
- **Year to date** totals (aggregate all monthly tabs)
- **All agents** listed (not just top N)
- **Ranked by total production value** (combined from both sheets)
- **Application count** shown alongside dollar amount
- Agents matched by name across both sheets (normalize case for matching)

### What's NOT in Scope
- Weekly breakdown (data isn't structured for it)
- External webpage (staying within Slack)
- Write access to the sheets (read-only)

### Slack Setup
- Dedicated leaderboard channel with controlled access
- `/leaderboard` slash command for on-demand viewing
- Michael will set up the channel and invite relevant agents

### Handoff Plan
- Matt gets temporary Slack admin access to set up the bot
- After signoff, Michael revokes all Matt's access
- No ongoing hosting cost (Cloud Run free tier)

---

## Next Steps

- [x] Book Zoom call via Michael's Calendly
- [x] Build prototype
- [x] Discovery call (May 19) -- scope, metrics, timeline confirmed
- [x] Deploy to Cloud Run (health check passing)
- [x] Research row labeling -- labels already exist in col A, no changes needed
- [ ] Finish Slack app setup (slash command URL, invite bot to channel)
- [ ] Get Slack admin access from Michael
- [ ] Refactor sheets.py for real sheet layout (column-per-agent, two sheets)
- [ ] Add YTD aggregation (read all monthly tabs)
- [ ] Add rate limiting
- [ ] Test with real data
- [ ] Demo to Michael, get feedback
- [ ] Final signoff, revoke access

---

*Created: 2026-05-13*
*Updated: 2026-05-21 (split technical docs to project repo)*
