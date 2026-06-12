# Calc workbook color-coding request

**Date:** May 13, 2026
**Scope:** `Door Pricing Calculator.xlsx`, the **Data Entry** sheet only
**Effort for Bob:** ~15 minutes, one time
**Decision needed:** sign-off on the proposed color scheme below

---

## What I'm asking for

Apply a consistent fill color to each cell on the **Data Entry** sheet according to the cell's role (input, calculated, output, or locked reference). Nothing else changes — no formulas move, no values change, no other sheets touched.

The other 13 sheets stay exactly as they are today.

---

## Why this is worth 15 minutes

### Reason 1 — for the engine (the website's math layer)

Right now my engine knows that `G2`, `G3`, and `G4` are the Total Truss / Column / Door cost cells because I told it so in code. If those cells ever move, or if a new output is added to the workbook, the engine breaks silently until I update the code.

With fill color used consistently, the engine can **auto-discover** the contract:

- Anything green = output → expose to the website
- Anything yellow = input → wire to the customer form
- Anything blue = derived / calculated → display as read-only
- Anything gray = locked reference → leave alone

This makes the engine more resilient when the workbook evolves, and removes one whole class of "Ryan forgot to update the code after Bob edited the file" failures.

### Reason 2 — for any human who opens the file

Today the Data Entry sheet is dense and undocumented. Someone opening it for the first time cannot tell which cells they are meant to touch and which they are meant to leave alone. After color coding, the contract is visible at a glance:

- New hires can read the sheet without a tutorial
- Bob's own future-self (six months from now, after a vacation) can re-orient in seconds
- Anyone reviewing a quote can see which cells drove the result
- Mistakes (typing into a calculated cell) become visually obvious

This is the lowest-cost, highest-yield documentation pass available — the workbook documents itself.

---

## Proposed color scheme

| Color | Hex | Cell role | Examples on Data Entry |
|---|---|---|---|
| 🟨 **Yellow** | `#FFF2CC` | **Customer input** — values the customer or salesperson provides | Door width, door height, building type, wind zone, open-time target, paint RAL |
| 🟦 **Blue** | `#DAE3F3` | **Derived / calculated** — values the workbook computes from inputs and lookups | Door weight, gang code, intermediate sums |
| 🟩 **Green** | `#E2EFDA` | **Final output** — the prices and headline numbers the site reads | `G2` Total Truss Cost, `G3` Total Column Cost, `G4` Total Door Cost |
| ⬜ **Gray** | `#EDEDED` | **Locked reference** — catalog values, lookups, hardcoded constants | Frame design list, pump options, weld table references |
| (no fill) | — | **Pass-through / structural** — labels, headers, layout cells | Sheet titles, column headers, separator rows |

All four fill colors are soft and printer-friendly. They sit comfortably under existing borders and text formatting, and none of them clash with the conditional-format colors already on the sheet.

---

## How to apply (suggested approach)

1. Open `Door Pricing Calculator.xlsx`, go to the **Data Entry** sheet.
2. Select all the cells in one role at a time (e.g., all customer inputs).
3. Apply the corresponding fill color.
4. Save.

If easier, I can deliver a pre-colored copy for Bob to review and either accept as-is or adjust. Just say the word.

---

## What I'm not asking for

- ❌ No changes to other sheets (BOM, Door Weight, Cylinder Calc, etc.)
- ❌ No formula changes
- ❌ No structural changes (no moving cells, no renaming)
- ❌ No removal or replacement of existing conditional formatting
- ❌ No commitment to maintain colors across future edits — the engine will degrade gracefully if a new cell shows up uncolored

This is a one-time, additive pass on a single sheet.

---

## Pairs naturally with the named-ranges ask

The named-ranges proposal in Section 3a of the main gap document (`DOOR_WIDTH`, `DOOR_HEIGHT`, `FRAME_DESIGN`, etc.) is the *machine-readable* version of the same idea. Color coding is the *human-readable* version. Doing both gives the workbook a self-documenting contract that survives whoever maintains it next.

— Ryan
