# Meeting Summary: Kinze Doors CRM - Susie Walkthrough & Priority Alignment

**Date:** May 27, 2026, 8:43 AM
**Duration:** ~34 minutes
**Location:** On-site at Kinze (Williamsburg)

**Attendees:**
- **Susie (Speaker 1)** -- Kinze doors sales coordinator, manages quoting and customer communication
- **Matt Druhl (Speaker 2)** -- External developer/consultant
- **Ryan Veatch (Speaker 3)** -- Project lead

---

## Purpose

Susie walked Matt and Ryan through her current quoting workflow end-to-end. The group aligned on priorities: start with automating Bob's pricing process (the bottleneck), not Susie's email workflow.

---

## Susie's Current Workflow

### Lead Intake
1. HubSpot form submissions arrive at a dedicated Kinze Doors email account
2. Forms contain: customer name, address, phone, door dimensions, building type (new/existing), project timeline, extras requested
3. Susie leaves emails in inbox until processed, moves to "Complete" folder when done. This is her tracking system to make sure nobody gets missed.
4. Monday mornings can have 5+ HubSpot forms waiting

### Quote Generation Process
1. Susie forwards the HubSpot form to Bob
2. Bob works through his spreadsheet, determines pricing, sometimes modifies for special requirements (e.g., 150 mph wind load)
3. Bob sends Susie back the cost number and a GA (general arrangement) drawing
4. If Bob has an exact GA drawing for the dimensions, he sends it. If not, he sends the closest match with a note saying "if you proceed, we'll create the correct one"
5. Susie scrolls to the bottom of her quote file to find the last quote number, increments it manually
6. Susie fills out a quote form template: customer info, door dimensions, opening time, lead time notes, 50% deposit requirement
7. She applies Bob's markup (currently 2x), calculates the final price
8. She locks the form (can't edit after locking; mistakes require recreating from scratch)
9. She saves as PDF, attaches the quote + GA drawing to an email using a template
10. Two email template variants: "here's your exact GA drawing" or "here's a similar GA drawing, we'll create the correct one if you proceed"
11. Manual edits for special cases: wind load ratings, multi-door discounts (~1 in 20 quotes), Kinze customer discounts

### Follow-up
- Bob maintains a separate spreadsheet to track customers and follow-up timing
- 2-3 days after the quote is sent, Bob calls to follow up
- Returning customers: Susie searches her email for the old quote, forwards it, and adds the new quote alongside

### Pain Points
- **Bob is the bottleneck.** On a busy weekend, 12-13 quotes can pile up. Takes Bob 2 days to dig out. If Bob is out (vacation, holiday), quotes wait.
- Susie's process is actually fast. She can fill a quote form in about 30 seconds once she has Bob's numbers.
- The current Kinze Doors CRM app adds friction for Susie: save HubSpot email as PDF, upload to the app, then download the output back. Not faster than her current email-based process.

---

## Key Decisions

### 1. Priority: Automate Bob's Process First

Susie, Ryan, and Matt all agreed: Bob's pricing engine is the biggest time saver. Susie's email workflow works and she's fast at it. Bob is the bottleneck.

**Susie:** "I think we probably start with helping him... I don't think [the CRM] is really saving me time."

**Ryan:** "Understanding what Bob's doing and what he needs is important, because I think that's the bigger win right now."

**Matt:** Proposed reprioritizing the roadmap: leave V1 (CRM) as-is, skip V2 (AI queries) for now, jump to V3 (Bob engine) first.

### 2. Susie Wants to Keep Email

Susie explicitly said she wants to keep the doors email account as her primary tracking system. She doesn't want the CRM to replace her email workflow yet. She's concerned about losing track of things if notifications go to Teams/chat instead of email.

**Susie:** "I don't want everything automated. We've got to get the trust in the system and the trust in our organizational form."

### 3. Build Confidence Incrementally

Ryan emphasized a trust-building approach:
1. Build the Bob engine alongside Bob's manual process
2. Bob verifies the system output against his manual calculations
3. Once Bob says "I haven't changed the output in weeks," confidence is established
4. Then decide what else to automate

**Ryan:** "Build what Bob does, and then figure out from there... let them build confidence with the automation."

### 4. GA Drawing Matching

Susie mentioned Bob spends time hunting for the closest existing GA drawing. The system could help by matching door dimensions to existing drawings in a database/spreadsheet. Bob could still manually override if the suggestion isn't right.

### 5. HubSpot Ingestion

Matt noted the current CRM requires PDF upload from HubSpot emails. This could be improved with a direct email check or HubSpot API integration, but that's a lower priority than the Bob engine.

Ryan suggested the app could ingest from the same email account Susie uses (read without deleting), so both Susie and the system see the same data.

---

## Next Steps (from this meeting)

1. **Matt goes to Bob** -- Walk through Bob's process: from receiving the HubSpot form to sending back pricing and GA drawing. Understand his spreadsheet, formulas, and decision logic.
2. **Matt meets with Doug and Steve (IT)** -- Understand infrastructure requirements for bringing the app in-house (servers, security, tech stack).
3. **Accounting touchpoint deferred** -- Mark Miller handles invoicing, but accounting has their own systems. Lower priority. Susie said Bob is the biggest time saver.

---

## People Referenced

| Name | Role |
|------|------|
| **Susie** | Doors sales coordinator, quote creation, customer email |
| **Bob** | Door engineer, pricing/specs, GA drawings, follow-up calls |
| **Mark Miller** | Accounting, handles invoices and deposit tracking |
| **Doug** | IT lead (meeting scheduled next) |
| **Steve** | IT (meeting scheduled next) |

---

## Quotes Worth Noting

**Susie on the bottleneck:** "He's buried. He's the bottleneck. We get a whole bunch of quotes over a weekend, like one weekend we had like 12 or 13. It took 2 days for him to dig out."

**Susie on trust:** "I don't want everything automated... we've got to get the trust in the system."

**Ryan on approach:** "Build what Bob does, and then figure out from there. Build confidence with the automation... let them build comfort with the system."

**Matt on the plan:** "So we need to start with the Bob engine first, get the pricing engine in, and then maybe get to you second. Make his job easier to get to the number."

---

*Transcript: `Voice 260527_084322_original.txt`*
