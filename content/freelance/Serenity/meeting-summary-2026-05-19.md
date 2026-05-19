# Serenity Leaderboard - Meeting Summary

**Date:** 2026-05-19, 1:00 PM CDT (Zoom)
**Attendees:** Michael Bond (Serenity Insurance Group CEO), Matt Druhl
**Duration:** ~40 minutes

---

## Key Decisions

1. **Slack bot, not a webpage.** Michael initially asked about a standalone webpage/leaderboard display, but agreed that hosting it within Slack is simpler. Agents already use Slack daily, so the leaderboard lives in a dedicated Slack channel with controlled access.

2. **Two Google Sheets as data sources:**
   - **Medicare & Ancillary** (Medicare Advantage, Medicare Supplement, Prescription Drug Plans)
   - **Life Insurance & Annuities**

3. **Leaderboard scope:**
   - **Current month** and **year to date** (no weekly breakdown, data isn't organized for it)
   - **All agents** listed on the sheets, not just top N
   - **Ranked by total production value (money)**, with application count also displayed
   - Combines totals from both sheets per agent (matched by name)

4. **Data structure (Life & Annuity sheet):**
   - Agents are in columns (one column per agent)
   - Key rows: 4 (life app total value), 6 (life app count), 64 (annuity total value), 66 (annuity app count)
   - Columns with "Agent" as the header are placeholders (skip them)

5. **Data structure (Medicare sheet):**
   - Same column-per-agent layout
   - Key rows: 3 (total value), 4 (application count)

6. **Dynamic agent handling:** If Michael adds a new agent in a new column, the bot picks them up automatically. It scans all columns and skips any that say "Agent" in the header.

7. **Robustness concern:** Matt discussed labeling the key rows so the bot can find them by name rather than hard-coded row numbers. This prevents breakage if rows get shifted. Matt will research whether Google Sheets supports named ranges or row labels for this.

8. **Price: $500 flat.** Michael agreed without pushback.

9. **Hosting cost: $0.** Cloud Run free tier covers expected usage. Matt mentioned adding a daily request cap (e.g., 50/day) as a safety measure against spam.

10. **No timeline pressure.** Michael said it's their slow season. Matt mentioned he's in Iowa with family/appointments but will keep Michael updated on progress.

11. **Access and handoff:** Michael granted Matt viewer access to both sheets. Matt offered to set up the Slack bot with temporary admin access, then have Michael revoke all access after signoff. Standard security practice.

## Clarifications from the Call

- **Why not pull from Slack directly?** Michael's Slack workspace has many agents across multiple teams. Too hard to filter just Serenity's agents from the general channels. Google Sheets is the source of truth.
- **Why not weekly?** Data isn't broken down by week in the sheets. Michael suggested color-coding rows by week, but Matt flagged this as fragile (wrong shade of green breaks the logic). They agreed monthly + YTD is sufficient.
- **Mixed case names** in the sheets. Matt will normalize names (convert to same case) before matching across sheets.
- **Screen sharing didn't work.** Michael shared his screen to show the spreadsheets. Matt couldn't share due to Zoom host settings.

## Action Items

| Owner | Item |
|-------|------|
| Matt | Research row labeling in Google Sheets (named ranges) so bot doesn't break if rows shift |
| Matt | Build POC pulling from both real sheets, post to Slack |
| Matt | Add rate limiting / daily request cap |
| Matt | Keep Michael updated on progress |
| Michael | (Already done) Granted Matt viewer access to both sheets |
| Michael | Will name the key rows if Matt provides instructions |
| Michael | Set up a dedicated Slack channel for the leaderboard |

## Scope Changes from Original Prototype

The current prototype (`~/Projects/serenity-slackbot/`) needs significant updates:

1. **Two sheets instead of one** — need to read from both Medicare and Life/Annuity sheets
2. **Column-per-agent layout** — current code assumes rows-per-agent with Name/Score columns. Sheets have agents in columns with data in specific rows. Major refactor needed.
3. **Multiple metrics** — need both production value (for ranking) and application count (for display), not just a single score
4. **Month-to-date + YTD** — need to read current month's tab plus aggregate all months for YTD
5. **Agent matching** — need to match agent names across two different sheets, normalize case
6. **Skip "Agent" placeholder columns** — dynamic column scanning with sentinel detection
7. **Rate limiting** — add daily request cap to prevent abuse

---

*Created: 2026-05-19*
