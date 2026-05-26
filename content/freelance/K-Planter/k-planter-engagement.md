# K-Planter Engagement - Brian & Jana

**Date:** 2026-05-26
**Context:** Building a software solution for K-Planter (Wholegoods & Repair Parts business). Introduced by Ryan Veatch but potentially a separate client relationship.

---

## Key Questions to Clarify

- Who is the client? Brian and Jana directly, or through Kinze/Ryan?
- How does billing work? Invoice K-Planter, invoice Kinze, or invoice Ryan?
- Does Ryan expect to be involved, or was he just making the introduction?
- What entity is K-Planter? (Separate business, division of Kinze, Ryan's venture?)

## What We Know So Far

- Workflow mapped: Wholegoods & Repair Parts share 11 steps (see k-planter-workstreams.svg/png)
- Three data sources: Kinze Europe Webshop, SAGA (Romanian accounting), FGO (invoicing)
- Heavy manual processes: handwritten part lists, Excel entry, manual document creation, code substitution lookups
- Meeting with Brian and Jana scheduled for 5/26 to learn more

## Engagement Model

### Phase 1: Discovery (Hourly)

**Rate:** $100-150/hr
**Scope:** Understand the full business process, pain points, and system landscape.

Already started:
- Workflow diagram (k-planter-workstreams)
- Identified three separate data sources with no integration

Still needed:
- Full inventory of manual steps and time spent on each
- Understanding of data flow between Webshop, SAGA, and FGO
- Volume: how many orders per week/month? How many part lookups?
- What does Brian/Jana's day actually look like?
- What's costing them the most time or causing the most errors?

**Deliverable:** Written assessment with recommended solution, estimated cost, and timeline.

### Phase 2: Build (Fixed Price Per Milestone)

**Scope:** Defined after discovery. Each milestone is a working deliverable they can see and test.

**Example milestones** (speculative, refine after discovery):
- Part code lookup and substitution tool
- Automated quotation generation
- Webshop integration for order entry
- Invoice and shipping document automation
- Dashboard / reporting

**Each milestone gets its own price, timeline, and acceptance criteria.** Don't bundle everything into one big delivery.

### Phase 3: Maintenance (Retainer or Hourly)

**After delivery:**
- Monthly retainer for ongoing support, updates, bug fixes
- Or hourly as needed
- Define response time expectations

## Automation Opportunities (From Workflow Diagram)

| Step | Current Process | Opportunity |
|------|----------------|-------------|
| Repair Parts Step 1 | Handwritten lists, manual Excel entry | Intake form or scanner that populates directly |
| Repair Parts Step 3 | Manual code substitution from a list | Automated lookup against substitution database |
| Shared Step 2 | Manual quotation document creation | Auto-generate from Webshop order data |
| Shared Steps 4-5 | Pro-forma invoice handling (receive, recreate) | Pass-through or auto-convert between systems |
| Shared Step 9 | Shipping docs based on Kinze Europe docs | Template-driven generation from order data |
| Shared Step 11 | Final invoice + inventory removal | Trigger from delivery confirmation |

## Pricing Guidance

- **Discovery:** Bill hourly. You're still learning. Don't quote a fixed price before understanding the full scope.
- **Build:** Fixed price per milestone after discovery. Protects both sides.
- **Don't start building before a written agreement.** Discovery itself is paid work.
- **The workflow diagram is already deliverable-quality work.** You're providing value now.

## Next Steps

- [ ] Meet with Brian and Jana (5/26) to learn full scope
- [ ] Clarify client/billing relationship (direct, through Kinze, through Ryan?)
- [ ] Document pain points and time costs
- [ ] Deliver discovery assessment with recommended solution and pricing
- [ ] Get written agreement before starting build phase
