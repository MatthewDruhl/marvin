# Kinze Doors quoting & production system — current state, gaps, and what is needed to close them

**Date:** May 13, 2026
**Purpose:** Give the full picture of where the system stands, what it is built to do for each department, and what specifically I need from Bob to take it the rest of the way.

---

## Top objective

The door-quoting and production process today touches many people across many departments. Every quote, every approved job, every shipped door runs through a sequence of handoffs — calculator runs, GA drawings, approval signatures, BOM generation, paint callouts, pump configuration, scheduling, fabrication, invoicing. Each handoff is a place where work can stall, get duplicated, or drift.

**The goal is to streamline the entire process so everyone in this picture does less manual coordination work and more of the work that actually requires their expertise.** The Door product line is the pilot. If the architecture works here, the same pattern extends to other Kinze product lines.

The current approach has many roles, many handoffs, and no shared system of record — every department keeps its own files, emails, and spreadsheets, and most of the day is spent moving information between them. The remainder of this document covers what already exists in the new system, what it is designed to do for each role, and what is needed from Bob to close the last big gap.

---

## What the system does (and is designed to do)

The system is a single web platform that sits across the whole flowchart, not just the quoting step. Capabilities are grouped by who benefits.

Legend: ✅ working today · ⚠️ partial · ❌ not yet built · 🔮 planned

### Sales & front office (Susie)

| Capability | Status |
|---|---|
| Customer record management (contact, address, project details, history) | ✅ |
| Quote pipeline tracking (New Lead → Quoted → Approved → In Production → Shipped) | ✅ |
| Quote PDF generation with Kinze branding | ✅ |
| Follow-up reminders and customer-touch logging | ✅ |
| Customer-facing quote request form | 🔮 |

### Engineering (Bob, Dennis, Eric, Tim)

| Capability | Status |
|---|---|
| Read Bob's calc spreadsheet as source of truth for pricing | ✅ (50×16 reference case) |
| Calculate prices for arbitrary door sizes | ⚠️ (engine fixes pending) |
| Auto-select frame design, truss type, pump from rules | ❌ (requires logic workbook — see Section 4) |
| Generate BOM and specialty views from approved design | ⚠️ (Single column working; other frame designs and truss configs pending) |
| GA drawing attachment and version tracking | 🔮 |
| Calculations & design alignment check (the "2nd set of eyes" step) | 🔮 |
| **Stretch:** attach a similar-size reference drawing from past jobs to the customer-facing quote (auto-selected by size match) | 🔮 |
| **Stretch:** AI-rendered design preview for the customer based on the request, with the production-grade drawing still produced by Kinze EE | 🔮 |

### Production planning (Jeff, Dani)

| Capability | Status |
|---|---|
| Job tracking once a quote is approved | ✅ (pipeline stage) |
| BOM-driven material planning | ⚠️ (depends on BOM generation above) |
| Sub-component pre-purchasing triggers for long-lead items at approval | 🔮 |
| Paint callout generation per customer-specified RAL | 🔮 |
| Customized assembly manual per door | 🔮 |
| Production routing and Door X bundle creation | 🔮 |

### Operations & maintenance (Evan, MFG)

| Capability | Status |
|---|---|
| Shipping planning and crating schedule | 🔮 |
| Timeline / gantt estimation across active jobs | 🔮 |
| Pump configuration and pendant controller setup tracking | 🔮 |
| Fabrication, weld, dry-fit, paint, hardware-gather, crate & ship status | 🔮 |

### Accounting

| Capability | Status |
|---|---|
| Invoice generation tied to approved quote | 🔮 |
| Down-payment tracking (gate to starting production) | ✅ |
| 4th Shift customer setup integration | 🔮 |
| Final-payment receipt tracking (gate to shipping) | ✅ |

### Cross-cutting (everyone)

| Capability | Status |
|---|---|
| Single source of truth for customer, quote, job, and shipping data | ✅ |
| Notifications routed to the right person at each handoff | 🔮 |
| Audit trail for who touched what and when | ⚠️ |

The pattern is the same across every role: **less manual coordination, less duplicated data entry, fewer dropped handoffs.** The system does not replace anyone's judgement — it carries the routine work between the moments where judgement is actually needed.

---

## What follows

1. **The big picture** — target state for the quoting flow specifically
2. **What works today** — quoting-system components currently running
3. **The gaps that need to close** — and which require Bob's input
4. **The proposal** — a second, smaller workbook to capture Bob's design rules
5. **What I need from Bob**

If you only have ten minutes, read the Top objective, sections 1, 4, and 5.

---

## 1. The big picture

Target state for the system in operation:

```
A customer (or salesperson) enters a door request on the site
    ↓
The site looks up your design rules (which frame? which truss? which pump?)
    ↓
The site feeds those choices into your calc spreadsheet
    ↓
Your spreadsheet does the math — same as today
    ↓
The site produces a quote PDF
    ↓
You get an email/notification: "quote ready, please review"
    ↓
You approve → quote goes to the customer
You adjust → site re-runs with your changes → you approve → goes out
```

**You remain the authority on every quote.** The site handles the data entry and the math; you provide the engineering judgement and final review. Your day-to-day shifts from building every quote from scratch to:

- **Maintaining the calc spreadsheet** (prices, materials, formulas) — same as today.
- **Maintaining a new, smaller rules spreadsheet** when your design rules change.
- **Reviewing and approving quotes** drafted by the site. Routine quotes are a 30-second click; unusual ones get your normal treatment.
- **Spot-checking** quotes periodically to confirm the system hasn't drifted.

The remainder of this document covers what stands between the current state and that target.

---

## 2. What works today

| Part of the system | Status | Notes |
|---|---|---|
| Customer records (contact, address, project details) | ✅ Working | The site stores all the customer info, project history, follow-ups, etc. |
| Quote pipeline (New Lead → Quoted → Approved → In Production → Shipped) | ✅ Working | Tracks where every customer is in the process. |
| Manual quote PDF generation | ✅ Working | The site produces a clean PDF with your logo. Layout polish completed last week. |
| Reading your calc spreadsheet | ✅ Working **for the 50×16 reference case** | The site opens the file, reads every sheet, and accesses your inputs and outputs. |
| Calculating prices for other door sizes | ⚠️ **Partially working** | The math engine handles most formulas but fails on a few specific patterns — covered in Section 3. |
| Bill of materials display | ⚠️ **Partial** | Currently reads only the "Single" design column. Needs to be extended to the other frame designs and the truss sub-sections. |
| Design selection | ❌ **Not yet** | The site does not know which frame/truss/pump to pick — that decision currently lives only with you. **This is the primary gap.** |

---

## 3. The gaps that need to close

There are two categories: **technical gaps** (my side) and **knowledge gaps** (your side).

### 3a. Technical gaps — my responsibility

Your calc spreadsheet is sound. The math is correct, and every number comes out as expected when the file opens in Excel or LibreOffice. The issues are in how my web-based math engine handles a few specific patterns — engine bugs, not spreadsheet bugs.

**Three engine fixes** will get the system working for every door size and frame/truss combination:

| Issue | Cause | Fix |
|---|---|---|
| The SKU/Gang Code formula uses `VALUE()` | My engine does not implement that function | One-line addition. ~5 minutes. |
| The truss material lookup fails when a truss config is not selected | My engine does not handle empty cells the same way Excel does | Small code change. ~15 minutes. |
| The door-weight HLOOKUPs reference a 919-row range when only the first ~200 hold data | My engine fails on oversized empty ranges | Either I trim the ranges in code, or you trim them in the file. |

**Two cleanups in the calc spreadsheet** that I would like to make with your permission:

| Cell | Issue | What I'd change |
|---|---|---|
| `Door Components!W6 = 0.25` | This value does not match any entry in the weld table (`Process!K16:K22` holds 0.123, 0.133, 0.172, 0.227, 0.259, 0.319, 0.455). Appears to be a stale hardcode. | **Need your call:** should this be 0.227, 0.259, or am I misreading the cell's purpose? |
| `Cylinder Calc!Y10` returns `#DIV/0!` | Divide-by-zero in a cell that does not appear to feed any output | Wrap in `IFERROR(..., 0)` to suppress the error. No output changes. |

Optional, not blocking: adding **named ranges** for the calibration inputs (`DOOR_WIDTH`, `DOOR_HEIGHT`, `FRAME_DESIGN`, etc.) so the file is more self-documenting and the engine can reference cells by name rather than position. Zero impact on your formulas; meaningful impact on long-term maintainability.

### 3b. The knowledge gap — and why this one matters most

The key finding from auditing the calc spreadsheet:

**Your spreadsheet does not choose a design. It assumes someone has already chosen one.**

The dropdowns on the Data Entry sheet (D5 frame_design, D9 truss_type) let *you* tell the spreadsheet which path to take. The spreadsheet then prices that choice. Nothing in the file encodes rules like "for a 60-foot wide door, use Big-Single" or "above 130 mph wind, use V-Truss." That logic lives in your head.

That is not a flaw — the spreadsheet was built to price, not to recommend. But it means **the site does not know what to put in those dropdowns**, and until that gap closes, the system cannot quote anything autonomously.

This is the single highest-value item I need from you.

---

## 4. The proposal: a companion "logic" spreadsheet

I propose a second, much smaller workbook — `Door-Design-Logic.xlsx` — that captures your selection rules in the same medium you already work in.

**Same look and feel as the calc file.** Same Excel format, same dropdowns, same column-and-row structure you already use daily.

### What it would contain

| Sheet | What's in it | Who fills it |
|---|---|---|
| Inputs | The customer-facing fields (width, height, building type, wind zone) | The site writes these from the customer record |
| **Frame Rules** | A lookup table: given the inputs, which frame design? | **You** |
| **Truss Rules** | Given the frame + size, which truss type and size? | **You** |
| **Pump Rules** | Given the door weight + open-time target, which pump? | **You** |
| **Hard Constraints** | Guard rails ("above 50ft must be Big-Single") | **You** |
| Recommended Inputs | The 17 cells that feed your calc spreadsheet | Calculated automatically from the rules above |
| Notes | Any explanations or exceptions you want recorded | **You** |

### How this is made easy for you

This is not a blank workbook. The **pre-populated template** already includes:

- All frame designs your calc spreadsheet recognizes (Single / Truss / Big-Single / Small-Single)
- All ten truss configurations from your calc spreadsheet (L Truss 1×30, X-Brace 1×30 through 3×65, V-Truss 2×45 through 3×65, etc.), pulled directly from your file
- All pump options (Pump 1, 4, 5, 8, 10, No Pump) and their electrical compatibilities
- The 50×16 Big-Single X-Brace case pre-filled as a worked example
- Empty rule grids sized for typical door dimensions (8–72 ft width, 8–30 ft height)
- Common building types (Agricultural, Commercial, Industrial, Residential, Custom) ready for edits

**Your job is to fill in the cells**, not design the workbook. The structure is a guided form that already knows your parts catalog, because that information is pulled directly from the calc file.

### Realistic time estimate

| Activity | Bob's time |
|---|---|
| Review the pre-populated template, decide what's missing | 30-60 minutes |
| Fill in Frame Rules (5-6 width × height bands × 3-4 building types) | 1-2 hours |
| Fill in Truss Rules (frame × size → truss type + size) | 1-2 hours |
| Fill in Pump Rules (door weight → pump selection) | 30-60 minutes |
| Fill in Hard Constraints (the "must" and "cannot" rules) | 30 minutes |
| Walk through 5-10 recent real quotes to validate the rules work | 1-2 hours |
| **Total** | **5-8 hours, spread over 2-3 sessions** |

After the initial pass, the workbook is only touched when your rules change — likely a couple of hours per year.

### What this saves you

Today, anyone who needs to know what to quote has to ask you. That adds up to hundreds of "what frame for X?" interruptions per year.

With the logic workbook in place:

- **Routine quotes (~80%):** the site applies your rules, you click approve, the quote goes out.
- **Edge-case quotes (~20%):** the site flags "no rule fires for this combination," you make the call, and you optionally add the rule so the next one runs automatically.
- **Spot-checks:** roughly 10 minutes a week pulling a recent quote and confirming the rules still match your intent.

The 5–8 hours of up-front effort pay back within roughly the first month of operation.

---

## 5. What I need from you

### Primary discussion (most of our time)

1. **How you choose a frame design.** Walk me through 2–3 recent quotes. Width × height × building type — what drove each pick? I capture as you talk; nothing for you to write down. The goal is to surface the pattern.
2. **The same for truss type and truss size.** When does X-Brace become V-Truss? When does 1×30 become 2×45?
3. **Hard rules.** Things that *must* or *cannot* happen regardless of other factors (e.g., "above a certain span, always Big-Single").
4. **Soft preferences.** Defaults you would recommend but would override for the right customer.

### Sign-offs (5–10 minutes total)

5. **`Door Components!W6 = 0.25`** — what is this cell meant to hold? It does not match the current weld table.
6. **Permission to wrap `Cylinder Calc!Y10` in `IFERROR(..., 0)`** to suppress the cached `#DIV/0!`.
7. **Permission to trim the Door Weight HLOOKUP ranges** from `$F$3:$J$919` down to approximately `$F$3:$J$200`.
8. **Permission to add named ranges** for the calibration inputs in the calc file. Zero impact on your formulas.

---

## What I am NOT proposing

To be clear about what stays the same:

- **You remain the source of truth for pricing.** The calc spreadsheet is yours. No AI invents prices and no one overrides your math.
- **You remain the source of truth for design.** The logic workbook captures *your* rules and no one else's. You are the only one with edit rights.
- **No quote ships without your approval.** Every quote the site produces lands in front of you first.
- **The calc spreadsheet does not change** beyond the two hygiene fixes noted above, which require your sign-off.

The system exists to serve your expertise, not replace it.

---

## Success criteria

- **Typical quote:** customer fills out a form → site applies your rules → site produces a draft → you receive a notification → you click "approve" → PDF goes to the customer. Roughly 2 minutes of your time per routine quote.
- **Unusual quote:** customer fills out a form → site flags "outside the rules, Bob review" → you make the design call → site produces the quote → you approve. Roughly 10–15 minutes of your time.
- No more interruptions to answer "what frame should I quote?"
- When something changes (new truss config, price adjustment, new building type), you update the relevant workbook, I redeploy, and the system stays in sync.
- If you take a week off, the system continues producing quotes correctly. Edge cases queue for your return; routine quotes ship unblocked.

This conversation is about confirming the path, pinning down what specifically I need from Bob to make it real, and surfacing input from everyone else in the room on the capabilities most worth building next.

---

## And beyond doors

The Kinze Doors product line is the pilot. The architecture — customer pipeline, product-specific calc workbook, product-specific logic workbook, role-aware notifications, single source of truth — is not door-specific. Once it is proven here, the same approach extends to other Kinze product lines that follow a similar quote → engineer → plan → build → ship → invoice pattern. Lessons learned from the door rollout directly reduce the cost and risk of every product line that follows.

---

**Questions or pushback?** Email or call anytime. Nothing in this document is locked in — it is a starting point for the conversation.

— Ryan
