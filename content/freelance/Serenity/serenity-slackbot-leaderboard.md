# Serenity Insurance Group - Slackbot Leaderboard

**Client:** Michael Bond, Founder & CEO
**Company:** Serenity Insurance Group
**Referral:** John Eimer
**Status:** In progress. Scope confirmed, POC deployed, refactor needed.
**Price:** $500 flat

---

## Confirmed Scope (from May 19 Zoom call)

### What's Being Built
A Slack bot that reads agent production data from two Google Sheets and posts a combined leaderboard to a dedicated Slack channel. Ranked by total production value (money), with application counts also shown.

### Data Sources
Two Google Sheets (Matt has viewer access to both):

**1. Life Insurance & Annuities**
- Agents in columns (one column per agent)
- Row 4: Life app total value
- Row 6: Life app count
- Row 64: Annuity total value
- Row 66: Annuity app count
- Columns with "Agent" in the header are placeholders (skip)

**2. Medicare & Ancillary** (Medicare Advantage, Supplement, Prescription Drug)
- Same column-per-agent layout
- Row 3: Total value
- Row 4: Application count

Both sheets have one tab per month.

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

## Technical Decisions

**Stack:**
- **Python 3.12+** with **uv** for package management
- **Slack Bolt** (Python SDK) for slash commands and event handling
- **gspread** + **google-auth** for Google Sheets API
- **Flask** as the HTTP framework (Bolt mounts onto it)
- **gunicorn** as the production WSGI server

**Architecture:**
- `Google Sheets (2)` -> `gspread API` -> `aggregate + rank` -> `Slack Block Kit` -> `Slack channel`
- `/leaderboard` slash command for on-demand pulls
- `/trigger` HTTP endpoint for Cloud Scheduler scheduled posts
- `/health` endpoint for monitoring
- Dynamic agent discovery (scan all columns, skip "Agent" placeholders)
- Rate limiting (daily request cap to prevent abuse)

**Hosting:** Google Cloud Run
- Service URL: `https://serenity-slackbot-1043989618770.us-central1.run.app`
- GCP project: `serenity-slackbot`
- Health check passing
- Free tier covers expected usage ($0/month)
- Cloud Scheduler: 3 free jobs, then $0.10/job/month

**Repo:** `MatthewDruhl/serenity-slackbot` (private)
- Located at `~/Projects/serenity-slackbot/`
- Branch: `docs/setup-walkthrough`

---

## Refactor Needed

The current prototype assumes a simple Name/Score row layout. The real sheets use a column-per-agent layout with data in specific rows. Changes needed:

1. **Two sheets instead of one** -- read from both Medicare and Life/Annuity
2. **Column-per-agent parsing** -- transpose the current row-based logic
3. **Multiple metrics** -- production value (for ranking) + application count (for display)
4. **Monthly tab + YTD aggregation** -- read current month tab, aggregate all months for YTD
5. **Cross-sheet agent matching** -- normalize names, combine totals
6. **Skip placeholder columns** -- detect "Agent" sentinel in header
7. **Row labeling research** -- see if named ranges can replace hard-coded row numbers (prevents breakage if rows shift)
8. **Rate limiting** -- daily request cap

---

## Next Steps

- [x] Book Zoom call via Michael's Calendly
- [x] Build prototype
- [x] Discovery call (May 19) -- scope, metrics, timeline confirmed
- [x] Deploy to Cloud Run (health check passing)
- [ ] Finish Slack app setup (slash command URL, invite bot to channel)
- [ ] Get Slack admin access from Michael
- [ ] Refactor sheets.py for real sheet layout (column-per-agent, two sheets)
- [ ] Add YTD aggregation (read all monthly tabs)
- [ ] Add rate limiting
- [ ] Research named ranges for row identification
- [ ] Test with real data
- [ ] Demo to Michael, get feedback
- [ ] Final signoff, revoke access

---

*Created: 2026-05-13*
*Updated: 2026-05-19 (scope confirmed from Zoom call)*
