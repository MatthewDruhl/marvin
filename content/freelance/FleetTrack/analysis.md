# FleetTrack — Project Analysis

> Based on Ryan's email (2026-06-01) with Perplexity audit and porting guide attachments.

---

## Summary

FleetTrack is a fleet equipment management app (asset registry + maintenance/repair logs + issue tracking + usage time-series + email alerts). Currently a single-tenant Next.js/SQLite prototype deployed on Railway. Ryan wants to rebuild it as a multi-tenant SaaS product and is proposing forking his `rdv-expenses` codebase as the foundation instead of starting from scratch.

## What Ryan got right

**The analysis is genuinely good.** The Perplexity audit is thorough. It correctly identifies the 8 business rules that define the product, catalogs the debt honestly (unsalted passwords, mass assignment, no tests, denormalized data), and the PORTING.md is a clean, stack-agnostic rebuild guide. The comparison table between rdv-expenses infrastructure and FleetTrack needs is accurate.

**Option 3 is the right call.** The infrastructure overlap is real. Auth, RBAC, audit logging, sessions, email, deployment pipeline, monorepo structure. Rebuilding all of that from scratch would be weeks of work for the same result.

## Concerns

**1. Scope creep risk.** The email casually mentions legalmind, partmind, mind-core, and a `rdv-base` template repo. Ryan is thinking platform, not product. Signing up for FleetTrack could mean maintaining shared infrastructure across multiple projects. The "2-3 hours to create a template" estimate is optimistic for something that needs to work across multiple apps.

**2. The domain is simple but the ambition isn't.** The audit correctly calls FleetTrack "plain CRUD + RBAC + transactional email + a small time-series." That's straightforward on a clean foundation. But Ryan's vision includes multi-tenancy, AI query agent, SMS notifications, customer portal, satisfaction surveys, job management, and multiple market segments (lawn care, farming, earth moving). The gap between "port 11 tables" and "build a SaaS platform" is large.

**3. Multi-tenancy is underestimated.** The email and docs both flag it, but the framing is "replace the singleton org_settings with a proper organizations table." In practice, multi-tenancy touches every query, every authorization check, every test, and every migration. It's not a schema decision, it's an architecture decision. Getting it wrong means data leaks between tenants.

## Pros

- Infrastructure foundation is solid (Ryan's assessment checks out)
- Domain is well-understood, cleanly documented
- The audit and porting docs are above-average quality for this stage
- Clear v1 scope: machines, maintenance, repairs, issues, usage logs
- Ryan is an engaged collaborator who thinks about architecture

## Cons

- Ryan's ambition (SaaS platform, multiple market segments, template repo) far exceeds the documented v1 scope
- Multi-tenancy complexity is acknowledged but underweighted
- Multiple concurrent projects (rdv-expenses, FleetTrack, legalmind, partmind, mind-core) could fragment focus

---

**Separate topic to discuss with Ryan:** Business terms (rate, ownership, equity, timeline) and IP ownership of the FleetTrack codebase and any shared rdv-base template. Worth settling before committing time.
