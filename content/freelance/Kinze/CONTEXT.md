# Kinze (kinzedoors) — Context Manifest

Last updated: 2026-06-12

## What This Is

AI consulting for Kinze Manufacturing (Williamsburg, IA): replacing the Excel-based hydraulic door pricing/quoting process with a database-backed system. A React/Node CRM prototype exists (repo `Veatch-Kinze/kinzedoors`, Railway-hosted); the production rebuild targets Kinze's own stack so their IT can support it long-term. The core business case is removing Bob as the single point of failure for quoting, not per-quote time savings.

## Stakeholders

- **Ryan Veatch** — engagement partner and repo owner. Drives momentum, runs his own AI analyses (sent the ultracode feasibility report). Watch: enthusiasm oscillates (pause email 5/28 after aligned meetings 5/27).
- **Bob** — engineering; owns the 14-sheet pricing workbook and the End Vertical Calculator. The quoting bottleneck the system replaces. Has 11 open questions pending (see below).
- **Eric** — engineering; his band chart makes frame/truss/pump selection deterministic, which is what makes full automation possible.
- **Susie (Susanne Veatch)** — sales coordinator. Her process works; explicitly out of scope for Phase 1.
- **Doug Weaver + Steve** — Kinze IT. Set the non-negotiable target stack (5/27).
- **Gary Newell** — Kinze; invoicing contact and AI follow-up meetings.

## Key Decisions

- **Target stack is non-negotiable** (2026-05-27, Doug): C#/Blazor Server, .NET Web API, SQL Server 2023, SAML SSO, Windows IIS.
- **Hardcode pricing logic, kill the .xlsx** — formulas are stable, only material prices change; prices live in a SQL table Bob edits via admin page.
- **Fresh build, not a port** — Phase 1: pricing engine + admin UI; Phase 2: CRM features.
- **Run parallel to the manual process before transition** — every stakeholder independently demanded trust-before-automation.
- **Price must gate on safety checks** (2026-06-09 feasibility report): the workbook prices cleanly even when structural checks fail; the engine must treat the 7 pass/fail checks as a hard validity gate.

## Current Status (2026-06-12)

- NDA signed 5/15. Vendor W-9 and ACH forms completed 6/12. Invoice flow with Gary working (first invoice 6/8-6/9).
- **Feasibility report received 6/9** (Ryan's 27-min ultracode run over Bob's + Eric's spreadsheets): verdict "build it, high confidence." Pricing reconciles to $16,143.43 on the 50'x20' trace; End Vertical Calculator already automates frame auto-selection. Matt reviewing 6/13.
- Harden audit of the kinzedoors repo (5/15): 22 findings, grade C; SEC-1/SEC-3 fixed, 18 issues remain. CI/CD pipeline (Gitflow, version bump) built 5/22.
- Blocker before build: spreadsheet formula walkthrough with Bob/Ryan, plus answers to the open questions.

## Open Questions

- Bob's 11 from the feasibility report (owner: Bob, via Ryan): door-coding/GA chart, column-frame size breakpoints, cylinder bore strategy, walk-through door adder, center-section selection, wind/location rules, pole-foundation assumptions, door thickness options, pin diameter inconsistency, quote-blocking on failed checks, material constants.
- "Truss" taxonomy: retired column-frame option or orthogonal door-leaf truss? (owner: Bob)
- Weight discrepancy in the new calculator's pressure formula (omits fixed 1,000 lb): intentional or bug? (owner: Bob)
- Pump strategy: engine iterates pumps for cost, or pump stays a sales input? (owner: Ryan/Bob)

## Where to Find Details

- `kinzedoors-notes.md` — tech stack, conversion plan, workbook contract (17 inputs / 10 outputs / 52 BOM rows), 5/27 meeting takeaways
- `kinze-vendor-forms-cheatsheet.md` — vendor onboarding paperwork
- `meetingTranscripts/` — raw transcripts (local only, gitignored)
- FEASIBILITY_REPORT.md — attachment on Ryan's 6/9 email ("Claude Ultracode Kinze Doors output report"); save locally when review starts
- Diagrams: `kinze-doors-current-process.svg`, `kinze-doors-proposed-system.svg`
- Session logs: 2026-05-18, 05-20, 05-27, 06-12

## Reviews

- Harden audit (Claude, 2026-05-15): grade C, 22 findings, 18 open
- Feasibility (Ryan's ultracode run, 2026-06-09): build-it verdict; Matt's cross-review pending 6/13 — candidate for the #284 cross-review experiment
