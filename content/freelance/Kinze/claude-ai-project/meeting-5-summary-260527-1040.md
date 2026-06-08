# Meeting Summary: Kinze Doors CRM - IT Requirements & Tech Stack

**Date:** May 27, 2026, 10:40 AM
**Duration:** ~16 minutes
**Location:** On-site at Kinze (Williamsburg)

**Attendees:**
- **Doug Weaver (Speaker 1)** -- Kinze IT lead, driving infrastructure and security requirements
- **Steve Stumpff (Speaker 2)** -- Kinze IT, security and code review
- **Ryan Veatch (Speaker 3)** -- Project lead, business decisions
- **Speaker 4** -- Kinze IT staff (brief)
- **Speaker 5** -- Kinze IT staff (Daniel referenced)
- **Matt Druhl (Speaker 6)** -- External developer/consultant

---

## Purpose

Align on the tech stack, infrastructure, and security requirements Kinze IT needs before Matt starts rebuilding the Doors CRM so they can support it long-term. Ryan framed it: "so we don't end up having to cook it twice, or cook it wrong."

---

## Key Decisions

### 1. Code Review / Vulnerability Scanning

Kinze is purchasing code review software for vulnerability management (API keys, listening code, critical vulnerabilities). Two tools evaluated. Doug preferred the more expensive option. Steve noted the cheaper one was selected at 1/3 the price. The tool will run before deployment and can also audit after the fact.

### 2. Internal-Only Application (Phase 1)

Confirmed the CRM is internal Kinze users only. Ryan noted it could go on the website as a customer-facing quoting tool someday, but that's not in scope now. Steve was okay publishing it before code review is in place, then fixing issues as they go.

### 3. Authentication: SAML SSO

Doug requires SSO authentication so users log in with their existing credentials (no separate login). Steve clarified it's SAML-based, any IDP works, not tied specifically to Windows. This affects the scope of the build.

### 4. Deployment: Windows IIS with Load Balancer

- Deploy on existing Kinze IIS servers (not new infrastructure)
- Load balancer in front for zero-downtime maintenance (take one server down, leave the other running)
- Only 2-3 concurrent users, so load is minimal
- Load balancer is more about maintenance windows than performance

### 5. Deterministic System (No LLM)

Doug asked directly: is there an LLM involved? Matt confirmed no, it's deterministic. Ryan noted they want to keep the door open for future AI features (asking questions about data), but Matt is intentionally separating LLM calls from deterministic code.

### 6. Tech Stack Requirements

| Layer | Requirement | Notes |
|-------|------------|-------|
| **Frontend** | C# / Blazor (strongly preferred) | Doug: "my preference is anything C-sharp." Will accept Node.js/React but limited skill sets to support it. Blazor Server mode mentioned (all rendering server-side). |
| **Backend** | .NET web services | Must be documented. JWT or equivalent auth between front and back end. |
| **Database** | SQL Server 2023 | Existing DB server. Will add a new database, not a new server. Doug mentioned embeddings work on SQL 2023 if needed later. |
| **Repository** | GitHub (for now) | No Azure DevOps license needed yet. Build on GitHub, transition later. Ryan: "don't buy any huge license." |
| **IDE** | VS Code or Visual Studio | Doug: "not too particular, but you will need to talk to Daniel." |

### 7. Development & Handoff Workflow

Matt laid out the plan, Doug and Ryan agreed:

1. Matt develops in his own environment (GitHub)
2. Build V1, run test cases externally
3. Susie and Bob review the product and give feedback (nitpicky stuff, not major functionality)
4. Package as a release, hand to Kinze IT
5. Kinze runs through their test → prod pipeline
6. Future feature requests come as versioned releases (V1 → V2 → V3)
7. At handoff, Matt provides deployment instructions. Kinze IT plugs in their infrastructure (DB connection, SSO, IIS config).

Matt offered: once functionality is solid, Kinze can decide whether they want Matt to handle cosmetic fixes or do them in-house.

### 8. Role-Based Access

Doug confirmed: if there are different roles, bake them in from the start. Users will be grouped in AD. Restrict access to only those who need it.

### 9. Email / Notifications

No automated emails in scope. Susie will see the quote, see Bob's info, see the PDF, then bundle and send manually. Ryan: "down the road it might be nice to hit a send button, but not yet." Steve noted they have an internal SMTP relay available if needed later.

### 10. Dev/Test/Prod Environments

Doug initially asked about dev/test/prod. Speaker 5 clarified that since Matt is developing externally, the transition happens when Kinze brings it into their DevOps. Matt doesn't need their dev/test environments to build. Kinze will run it through test → prod on their side after handoff.

---

## Action Items

| Item | Owner | Notes |
|------|-------|-------|
| Build CRM in C#/.NET/Blazor with SQL Server | Matt | Per Kinze IT requirements |
| SAML SSO integration | Matt | Any IDP, JWT between front/back end |
| Coordinate with Daniel on IDE/tooling | Matt | VS Code or Visual Studio |
| Provide deployment instructions at handoff | Matt | IIS config, DB setup, SSO config |
| Set up DB on SQL Server 2023 | Kinze IT | Add database to existing server |
| Configure IIS + load balancer | Kinze IT | Existing infrastructure |
| Code review software purchase | Kinze IT | Already in progress |

---

## Impact on Existing Plan

Two changes from the earlier tech stack discussion:
1. **SQL Server 2023, not MySQL** -- Kinze has existing SQL Server infrastructure
2. **Windows IIS deployment, not containerized** -- Existing IIS servers with load balancer
3. **SAML SSO required** -- Not in original scope, adds to Phase 1 work
4. **Blazor Server mode** -- Server-side rendering preferred, aligns with Kinze's support capabilities

---

*Transcript: `Voice 260527_104014_original.txt`*
