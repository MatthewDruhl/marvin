# Kinze Doors CRM - Notes

## Tech Stack

**Frontend:**
- React 18
- Vite (build tool)
- Tailwind CSS (styling)
- React Router (navigation)

**Backend:**
- Node.js + Express

**Database:**
- PostgreSQL

**Libraries:**
- `pdf-parse` (PDF intake for HubSpot lead notifications)

**Hosting:**
- Railway (auto-deploy from `main`, features integrate on `development` first)

**CI/CD:**
- GitHub Actions (Gitflow, version-bump workflow, sync-development workflow)

---

## Tech Stack Conversion Plan

Kinze wants to support the app long-term in their own stack. Requirements confirmed in meeting with Doug Weaver (Kinze IT) on 2026-05-27.

### Target Stack (confirmed by Kinze IT)

| Layer | Requirement | Notes |
|-------|------------|-------|
| **Frontend** | C# / Blazor Server | Server-side rendering. Doug's strong preference for C# supportability. |
| **Backend** | .NET Web API | JWT or equivalent between front/back end. Documented. |
| **Database** | SQL Server 2023 | Existing DB server at Kinze. Add new database, not new server. |
| **Auth** | SAML SSO | Users log in with existing AD credentials. Any IDP. No separate login. |
| **Deployment** | Windows IIS | Existing servers with load balancer (zero-downtime maintenance). |
| **Repository** | GitHub (for now) | Azure DevOps later when Kinze takes over. No license needed yet. |
| **Code Review** | Vulnerability scanner | Kinze purchasing. Runs pre-deploy and post-deploy audits. |

### Approach: Hardcode Pricing Logic, Kill the .xlsx

The spreadsheet formulas are stable. Only material base prices change. So instead of porting the Excel dependency (EPPlus, etc.), extract the formulas into a C# `PricingEngine` class and store material prices in a SQL Server `MaterialPrices` table. Bob updates prices via admin page, no developer needed.

### Phased Build (fresh project, not a port)

**Phase 1: Pricing Engine + Admin UI**
- .NET Web API + Blazor Server frontend
- SQL Server 2023 with material prices table
- Hardcoded formulas from the 14-sheet workbook
- Bob inputs door specs (17 inputs), gets quote with BOM breakdown (10 outputs + 52 BOM rows)
- Admin page for material price updates
- SAML SSO + role-based access (admin vs regular user)
- Estimated effort: 2-3 sessions (SSO may add to this)

**Phase 2: CRM Features (bolt on later)**
- Customer pipeline (7-column kanban)
- Quote snapshots, PDF generation
- Activity timeline, follow-up flagging
- Estimated effort: 6-9 additional sessions

### Handoff Workflow

1. Matt develops on GitHub in own environment
2. Build V1, run test cases externally
3. Susie and Bob review, give feedback
4. Package release with deployment instructions (IIS config, DB setup, SSO config)
5. Kinze IT runs through test → prod
6. Future features as versioned releases (V1 → V2 → V3)

### Blocker Before Starting

Need a walkthrough of the spreadsheet formulas with Bob or Ryan. The workbook contract maps inputs/outputs but the intermediate calculations (truss calc, cylinder calc, width/height calc, BOM lookups) span 14 sheets and need to be traced accurately before codifying.

### Current Workbook Contract (for reference)

**17 Inputs** (all on "Data Entry" sheet):
- Door width/height (ft) - required
- Door thickness (in), frame design, cylinder bore, pump type, electrical type, truss type
- Center section, vert/hori truss dimensions and quantities
- Insulation density/thickness, tin weight, wind load

**10 Outputs:**
- Truss cost, column cost, total cost, gang code
- Engineering: reaction force/moment, hydraulic pressure/hp, open time, wind rating pass

**BOM:** 52 rows of components with quantities and costs

**Calibration case:** 50x16 Big-Single X-Brace = $15,434.02 total ($6,941 truss + $8,493 column)

---

## Takeaways from On-Site Meetings (2026-05-27)

Three meetings: Susie (sales coordinator), Bob + Eric (engineering), Doug + Steve (IT).

### Matt's Assessment

Bob's current spreadsheet process can be moved to a more robust system backed by a database and code. It would take some of Bob's and Eric's time to verify correctness of the formulas during the transition. The system should be written in Kinze's tech stack (C#/.NET/Blazor/SQL Server) to ensure their team can support it after build and turnover. HubSpot could be automated to push quote requests directly into the system, which would generate the quote and email it to the right people. GA drawing matching would search by exact size first, then fall back to fuzzy matching by closest dimensions.

### Key Observations

1. **Bob is the single point of failure.** If he's out, quotes stop. The core business case is removing that bottleneck, not per-quote time savings.
2. **Eric's band chart makes full automation possible.** Frame, truss, and pump selection become deterministic lookups. Without this chart, you'd be encoding Bob's intuition. With it, the system can run without Bob.
3. **Susie is fast and happy.** Her process works. Don't touch it in Phase 1. The ROI is in Bob's workflow, not hers.
4. **The calculator is simple, the drawing search is not.** Bob's pricing calc is 3-5 minutes. GA drawing matching is where he loses time. A database with dimensions as searchable fields solves this.
5. **Everyone wants trust before automation.** Susie, Bob, and Ryan all said the same thing independently: run the system alongside the manual process, verify it matches, then transition.
6. **Tech stack is non-negotiable.** C#/.NET/Blazor/SQL Server/IIS. Doug was clear. Building in anything else means Kinze IT can't support it long-term.
7. **SAML SSO adds real scope.** Not in the original plan. It's a Phase 1 requirement now.
8. **Material costs are the only moving input.** Formulas and logic are stable. Costs update annually from Fourshift. A simple price table replaces embedded spreadsheet values.
9. **Low conversion rate signals a young market.** ~230 quotes, low sold count. Ag customers get sticker shock on hydraulic doors. Quote volume will stay high relative to sales, making the bottleneck worse over time.
10. **Ryan's pause email contradicts yesterday's momentum.** Three meetings, all stakeholders aligned, action items assigned, Bob eager. Then 12 hours later Ryan says it "may pause." Worth watching, not reacting to yet.
