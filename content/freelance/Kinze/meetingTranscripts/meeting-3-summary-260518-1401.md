# Meeting Summary: Kinze AI Readiness & Data Infrastructure

**Date:** May 18, 2026, 2:01 PM
**Duration:** ~53 minutes
**Location:** On-site at Kinze (part of a full-day series of meetings)

**Attendees:**
- **Matt Druhl** -- AI consultant/freelancer
- **Jamie** -- Kinze data/analytics lead (IT background, 3 years at company, CS and Business Administration double major)
- **Gary** -- Kinze engineering/product leader (coordinating the AI council initiative)

Other people referenced: Doug and Steve (met earlier, IT), Jay (HR/compliance), Zach (met before this session), Ryan, Gary (wrap-up at 4 PM), Joe (North Liberty IT, meeting Wednesday)

---

## Key Topics Discussed

### 1. Current State of AI at Kinze

- Company is at an "infancy stage" with AI adoption
- Current use is primarily "Google search 4.0" -- getting better answers and building proof of concepts
- Greatest limitation: moving from proof of concept to production
- Challenges: skill sets, education, data quality, process consistency
- Lack of project management coordination around AI opportunities

### 2. Competitive Pricing Tool (Jamie's Current Project)

- Building a data pipeline to extract text from competitor PDF documents for pricing analysis
- Using AI to build scraping scripts and the software itself (Python)
- Pricing optimization rules: 30% margin requirement, stay within 25% of competitors, no single price change greater than 25%
- Focused on top 500 repair parts (out of 14,000 total), narrowed to ~300 competitively relevant parts
- Identified parts where Kinze's cost exceeds lowest competitor price (no margin opportunity), feeding back to supply chain
- Needs better requirements gathering: personas, use cases, stakeholder input from director of sales
- People who previously handled competitive pricing are no longer with the company; knowledge was lost

### 3. Shadow IT Concerns

- Major concern about "shadow IT on steroids" as people build AI solutions independently
- Numerous refreshable spreadsheets and macros already exist with no governance
- Business continuity risk: when creators leave, their tools and knowledge go with them
- Excel spreadsheets with macros described as "the old AI" -- same problem now amplified

### 4. Standardization and Governance (Central Theme)

- Need for a standard process covering: testing, ownership transfer from POC to enterprise release, code structure consistency, security hardening
- Discussion of tiered user skill levels with different permissions for AI tool usage
- Balance needed between process rigor and not being so burdensome that people bypass the system
- Transfer of ownership from individual accounts to service-based accounts for business continuity
- Agents and knowledge repositories need the same governance as coded solutions

### 5. Tech Stack Definition (Top Priority)

- No defined tech stack exists for AI development at Kinze
- AI tools (primarily Cursor/Copilot) default to outputting Python, but almost nobody at the company can read or support Python code
- Jamie faces a daily dilemma: build properly in Python (nobody else can maintain it) vs. use drag-and-drop/workflow tools (easier to support but less capable)
- Need to define both: which AI tools to use AND what languages/frameworks AI should produce code in
- **Identified as one of the two most immediate items for the AI council**

### 6. Data Infrastructure Gaps

- No enterprise data warehouse exists
- ERP system is the primary data store, with connected and sometimes disconnected processes
- Data pipelines are ad hoc: various scripts pushing data where it needs to go, no data governance system
- Jamie uses Power BI for dashboards, Power Query for ETL
- Microsoft Fabric license is on the to-do list but keeps getting pushed off
- Company is primarily a Microsoft shop (Office 365, SharePoint, Teams) through North Liberty
- North Liberty IT uses some Azure; another group uses AWS -- split creates complexity
- Cloud adoption is minimal outside of Office 365

### 7. Data Quality and Cleanliness

- "You can't have a good AI solution without good quality data"
- Data cleanliness is questionable, especially in engineering (history of migrations: hand-drawn to AutoCAD to MonoCAD to Inventor to SolidWorks)
- Data ownership is also a concern
- Open question: "Is our data even ready to convert?"

### 8. Order Code Problem (Concrete Example)

- Kinze changes order codes for products year over year (e.g., a 3605 12-row 30-inch machine may have four different order codes across recent years)
- Makes it impossible to track sales/forecasting for a given model over time
- Jamie had to manually create a mapping table (model, row number, spacing, size) to work around this
- SLT asked for sales forecasting/prediction, which is nearly impossible without this mapping
- Potential AI project: give AI access to the data to create a cross-reference lookup table
- Alternative: create a persistent secondary attribute that never changes, regardless of order code changes
- Led to discussion of whether the better fix is an AI tool or a process change

### 9. Process Documentation via AI

- Matt suggested using AI to transcribe and analyze conversations about current processes to generate workflow documentation
- Record people talking through their processes, have AI create the workflow diagram, then review/iterate
- Addresses the gap of not having documented process flows

---

## Decisions Made

No formal decisions finalized. This was an information-gathering and brainstorming session as part of a larger AI strategy day.

**Consensus direction:** The AI council needs to prioritize two items first:
1. Approved AI tools
2. The tech stack that AI tools should produce code in

---

## Action Items / Next Steps

1. **AI Council to define tech stack** -- Both approved AI development tools and programming languages/frameworks. Agreed-upon first priority.
2. **Wednesday meeting with Joe** (North Liberty IT) -- discuss cloud infrastructure and IT alignment
3. **Jamie and Gary follow-up tomorrow** -- discuss forecasting, production, and other AI opportunities not covered
4. **Subject matter expert from supply chain** to join a future meeting for purchasing data and supply chain AI opportunities
5. **Wrap-up meeting with Gary at 4 PM** same day
6. **Large group session** immediately following this meeting
7. **ROI framework** -- Gary intends to build an ROI structure for small-scale AI projects, iterating over time
8. **Order code cross-reference** -- identified as a potential AI project. Needs evaluation of AI approach vs. process change before proceeding.
9. **Cataloging/repository system** needed for mid-tier AI tools and scripts (not enterprise-scale but still need visibility and business continuity)

---

## Important Context

- Kinze manufactures agricultural equipment (planters, ~14,000 repair parts)
- A canceled ERP implementation followed by ag market downturn and budget tightening stalled data infrastructure investments
- Jamie's background: 12 years in IT prior to Kinze, can interpret Python but doesn't use it daily
- This meeting was part of a full-day on-site consulting engagement. Matt and Gary are conducting an AI readiness assessment across the organization.
