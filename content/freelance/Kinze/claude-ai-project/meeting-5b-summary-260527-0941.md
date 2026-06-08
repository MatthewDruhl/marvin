# Meeting Summary: Kinze Doors CRM - Bob's Pricing Process Walkthrough

**Date:** May 27, 2026, 9:41 AM
**Duration:** ~44 minutes
**Location:** On-site at Kinze (Williamsburg, Bob's office)

**Attendees:**
- **Susie (Speaker 1)** -- Kinze doors sales coordinator
- **Bob (Speaker 2)** -- Door engineer, pricing and specs
- **Ryan Veatch (Speaker 3)** -- Project lead

Note: Matt was present but mostly observing. Ryan and Susie asked most of the questions.

---

## Purpose

Walk through Bob's end-to-end process from receiving a HubSpot form to sending pricing and a GA drawing back to Susie. This is the "Bob engine" that needs to be automated.

---

## Bob's Current Process

### Step 1: Log the Quote Request
- Bob maintains a spreadsheet with every quote request, searchable by customer last name
- Separate tab for phone call logs (documents every call, incoming and outgoing)
- Highlights callbacks in blue, marks definite "no" responses in yellow
- Uses a pivot table to analyze which door sizes are quoted most (width x height matrix). Currently ~230 quotes total since launch.

### Step 2: Run the Calculator (3-5 minutes)
Bob opens the pricing spreadsheet and enters the door specifications:

**Inputs Bob enters (human-modifiable fields):**
- Door width and height (ft)
- Door thickness (8" standard, 12" for larger/stronger doors)
- Column frame design (4 types: Small Single, Single, Big Single, Truss)
- Electrical power (Single Phase or 3-Phase)
- Truss type (No Truss, L Truss, V Truss, X-Brace/Cross Brace)
- Cylinder bore (keep at 4" standard when possible)
- Hydraulic pump (4hp, 5hp, 8hp, 10hp, selected based on PSI)
- Wind load rating (125 standard, 150 for hurricane/coastal zones)
- Truss dimensions (height, width, quantity) if applicable

**How Bob selects frame design and truss type:**
- Based on experience/intuition, but there IS logic in the spreadsheet
- Eric Sprenchi built a visual "band chart" (like a BMI chart) showing which frame design and truss type fits based on door height and width ranges
- Within each band, there's a lighter and heavier end. Bob aims for the middle.
- The spreadsheet tells Bob which designs are valid, but Bob applies judgment for edge cases

**What the spreadsheet calculates automatically (behind the scenes, across 14 tabs):**
- Cylinder requirements
- Bill of materials (BOM) with part numbers and costs
- Wind load calculations (closed and open deflection)
- Stress calculations (vertical force when closed, gravity + wind when open)
- Safety factor checks (pass/fail for fixed column, pin, cross brace tension)
- Truss cost and column cost, summed to total door cost

**Pass/fail indicators:**
- Wind deflection: shows "FAIL" if the door doesn't meet the wind load rating. Bob then upgrades the truss or changes the frame design.
- Cross brace tension: shows fail if the rod size is too small. Bob can increase rod diameter or switch to a different truss design.
- Factor of safety checks on multiple structural elements.

**Output Bob sends to Susie:**
- Total door cost (Bob's cost, not retail)
- Estimated opening time (seconds)
- Pump type and specs included in the quote
- Any special notes (wind load rating, walk-through door +$500, windows +$500)
- A GA (General Assembly) drawing, either exact match or closest available

### Step 3: Find a GA Drawing (most time-consuming part)
- Bob browses a folder of all existing GA drawings
- Drawing numbers have embedded logic (e.g., numbers starting with "112" are all singles)
- Bob searches by width (e.g., types "40 by" to find all 40-foot doors)
- For a 38-foot request, he'd look at anything 36-40 feet
- If an exact match exists, he sends it. If not, he sends the closest with a note.
- This manual search is where Bob spends the most time. The calculator itself is 3-5 minutes; the drawing search adds more.

### Step 4: Send Back to Susie
- Bob replies to Susie's email with: cost, opening time, pump specs, GA drawing (attached), and any special notes
- Susie then applies the markup (currently 2x) and creates the customer-facing quote

### Step 5: Follow-up
- Bob waits 1-2 weeks after the quote is sent, then calls the customer
- Logs calls in his spreadsheet with dates and notes
- Up to 3 follow-up calls, about a week apart
- Uses calendar reminders for scheduled callbacks (some customers say "call me in January")
- Paper copies spread out on desk during calls for reference

---

## Key Findings for the Build

### Material Cost Updates
- Costs are updated **annually** (fiscal year ends May 31, new costs starting June 1)
- Prices come from Fourshift (their ERP/accounting system), looked up one at a time
- Takes Bob **half a day** to fully update all material costs
- Not many material varieties: tubing (8" and 12"), bar stock, a few purchased parts
- Ryan asked if costs could be pulled from Fourshift automatically via query. Bob thinks so but doesn't have clearance. Accounting could provide a spreadsheet export.

### What Changes vs. What's Stable
- **Formulas/logic: stable.** Bob confirmed the logic doesn't change, just raw material costs.
- **Design concepts: in flux.** Eric is working on new design concepts to reduce costs, which could change the spreadsheet structure. But the core calculation logic (sizing, stress, BOM) is stable.
- **Material costs: annual update,** could be more frequent if steel market moves.

### Pump Selection Logic (not in spreadsheet)
Bob's rule (from experience, not automated):
- Under 1500 PSI → 4hp pump
- 1500-2500 PSI → 5hp or 8hp pump
- This is currently human judgment based on the PSI output from the calculator. It's a simple threshold that could be automated.

### GA Drawing Matching
- Drawings are stored in a folder, sorted by drawing number
- Drawing numbers encode the door type (singles start with 112, etc.)
- Could be stored in a database with dimensions as searchable fields
- System could propose 2-3 closest matches based on width/height/type
- Bob would still have final say on which drawing to send

### Bob's Pain Points
1. **Interruptions** -- The 10-minute quote process gets stretched when he's pulled into meetings or other work. 12-13 quotes over a holiday weekend = 2 days to clear.
2. **Drawing search** -- Most time spent hunting for the right GA drawing.
3. **Manual cost updates** -- Half a day, once a year, looking up costs one at a time from Fourshift.
4. **No one else can do it** -- If Bob is out, quotes stop.

### Bob Wants the System
- Bob explicitly said he'd use a web-based system instead of his manual spreadsheet
- He'd enter phone call logs into the app instead of the spreadsheet
- Others could then see call history (visibility Susie and the team currently lack)
- He wants to build confidence gradually: run the system alongside his manual process, verify it matches

### Quote Volume
- ~230 quotes since launch (started fall 2025, ramped up mid-March 2026)
- From ~70 to 230 since the marketing push in March
- Green (sold) vs. not: tracked in the spreadsheet. Sold count was low (exact number unclear from transcript).
- Most common loss reason: cost (especially ag customers who've never priced a hydraulic door)
- Aviation customers understand the pricing better

---

## Eric's Band Chart Walkthrough (Speaker 4, ~47:00-54:00)

At the end of the meeting, Ryan brought Matt to see Eric Sprenchi's logic spreadsheet. Eric (Speaker 4) walked through it.

### What the Band Chart Does
- For a given door width and height, it calculates rough door weight and center of gravity
- Based on CG and weight, it determines the max hydraulic pressure throughout the full cylinder stroke (not just at the top)
- At 0.1-inch increments through the entire stroke, it finds the true max pressure point (which isn't always at the top; sometimes it's 6 inches into the stroke depending on door geometry)
- Each cell shows which frame designs are valid: SS (Small Single), S (Single), BS (Big Single), T (Truss)
- "ERROR" means no option exists at that pressure level to lift that door size

### How It Works
- Two pressure tiers: 1500 PSI and 2200 PSI
- Pressure x gallons per minute = horsepower, which determines pump selection
- The chart is essentially **binary pass/fail** for each door size + frame combination
- Eric: "I would envision this as you take the choice away. If I have this size door, this is the size [frame] you have. Period."

### Key Insight for the Build
- This chart **eliminates Bob's intuition step.** Given door dimensions, it deterministically tells you which frame design and truss type to use.
- No fuzzy "middle of the band" judgment needed. Eric built it to be definitive.
- It also drives pump selection: if the 1500 PSI option shows ERROR for a door size, you must go to the 2200 PSI (higher hp) pump.
- Opening time is calculated per size, driven by gallons per minute.

Ryan: "This is the human intuition part that they're trying to capture into the system."

---

## People Referenced

| Name | Role |
|------|------|
| **Bob** | Door engineer, pricing, specs, follow-up calls |
| **Susie** | Sales coordinator, quote creation, customer email |
| **Eric / Eric Sprenchi (Speaker 4)** | Design engineer, built the band chart for frame/truss selection, working on cost reduction designs, creates 3D models |
| **Tim** | Breaks down Eric's 3D models into individual part drawings |
| **Dennis** | Creates GA drawings in CAD (~20 min per drawing) |
| **Arlen** | Original creator of the pricing spreadsheet (no longer at Kinze, took a job in Nebraska) |

---

## Impact on the Build

This walkthrough confirmed:

1. **The calculator is 3-5 minutes of work.** The automation payoff is removing the bottleneck (Bob being the only person who can do it), not saving massive per-quote time.
2. **Pump selection can be automated.** Eric's chart makes it binary: given door size, if 1500 PSI shows ERROR, go to the higher pump. No judgment needed.
3. **Frame/truss selection can be fully automated.** Eric's band chart is deterministic, not fuzzy. Given door dimensions, there's one answer.
4. **GA drawing matching can be automated.** Store drawings with dimensions in a DB, search by closest match.
5. **Material costs should come from a price table** that Bob (or accounting) updates annually, not embedded in the spreadsheet. Fourshift (ERP) is the source of truth.
6. **Quote versioning matters.** Quotes are good for 30 days. Steel prices change. Old quotes should lock in the prices they were built with.
7. **Bob is on board.** He wants the system and would use it immediately. He also explicitly wants to keep human oversight until confidence is built.
8. **Eric's chart is the missing piece.** It replaces Bob's intuition for frame/truss/pump selection with deterministic logic. This makes full automation of the pricing engine achievable.

---

*Transcript: `Voice 260527_094129_original.txt`*
