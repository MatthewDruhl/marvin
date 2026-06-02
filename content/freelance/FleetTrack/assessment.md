# FleetTrack -- Technical Assessment

**Date:** May 30, 2026
**Repo:** [Veatch-Kinze/fleettrack](https://github.com/Veatch-Kinze/fleettrack)
**Live:** https://fleettrack-production-fe0c.up.railway.app/
**Owner:** Ryan Veatch
**Codebase:** ~7,900 lines TypeScript
**Audit Grade:** C (4 blocking, 7 non-blocking)

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Frontend | Next.js 16, TypeScript, Tailwind CSS (dark theme) |
| Backend | Next.js API routes |
| Database | SQLite with Drizzle ORM, WAL mode |
| Auth | Custom HMAC-SHA-256 session tokens (7-day TTL) |
| Email | Resend API (Gmail SMTP fallback for dev) |
| Deploy | Railway, Nixpacks builder, Node 22 |
| Storage | SQLite on mounted /data volume |

---

## What's Built

- Machine registry with full metadata (make, model, year, VIN, category, status)
- Six equipment categories (agricultural, construction, vehicle, ATV/SUV, marine, other)
- Maintenance logging with next-service date tracking
- Repair logging with labor/parts cost breakdown and warranty flags
- Issue tracking with priority levels (low/medium/high/critical) and status workflow
- Usage history tracking (hours and miles over time)
- Categorized machine notes (oils, fluids, tires, consumables, general)
- Dealership and service tech management with archiving
- Multi-user with roles: admin (full control), mechanic (read+write), viewer (read-only)
- Email notifications on issue creation/resolution
- Audit logging (login/logout with IP and user agent)
- Dashboard with fleet stats, open issues by priority, machine counts by category

---

## Database Schema (10 tables)

`users`, `machines`, `maintenanceLogs`, `repairLogs`, `machineNotes`, `issues`, `usageHistory`, `dealerships`, `serviceTechs`, `accessLog`, `notifications`

**Good:** proper foreign keys, cascade deletes, 3NF normalization, timestamps on all tables
**Missing:** no indexes on frequently queried columns, no unique constraints on dealership names

---

## Strengths

1. **Clean architecture.** Proper separation between UI, API, DB, and auth layers. Easy to follow.
2. **Full TypeScript with strict mode.** Drizzle ORM generates types from the schema.
3. **Comprehensive data model.** Covers all major equipment management workflows.
4. **Recent security hardening.** Session tokens and route auth were patched in PR #2. Tokens now use HMAC-SHA-256 with constant-time verification. All data routes require auth.
5. **Good security documentation.** SECURITY_REVIEW.md tracks all known vulnerabilities with severity, status, and links to GitHub issues.
6. **Smart deployment.** Railway auto-deploy, volume persistence, proper Node version pinning, auto-restart on failure (up to 10 retries).
7. **Responsive UI via Tailwind breakpoints.** Works on mobile, though not optimized for it.

---

## Harden Audit Scorecard

| Scope | Grade | Blocking | Non-blocking |
|-------|-------|----------|--------------|
| Security | D | 3 high | 1 medium, 1 low |
| Tests | C | 1 high | 1 medium |
| Code Quality | B | -- | 1 medium, 1 low |
| Decoupling | B | -- | 1 medium, 1 low |
| **Overall** | **C** | **4 blocking** | **7 non-blocking** |

---

## Open Issues -- Batch 1 (Blocking)

These must be fixed before shipping to untrusted users.

| # | ID | Title | Severity | File |
|---|-----|-------|----------|------|
| [#11](https://github.com/Veatch-Kinze/fleettrack/issues/11) | SEC-1 | Weak password hashing -- SHA-256 with global pepper, no per-user salt | High | `src/lib/auth.ts:55-61` |
| [#12](https://github.com/Veatch-Kinze/fleettrack/issues/12) | SEC-2 | Default admin credentials committed to the repo | High | `src/db/seed.ts:18` |
| [#13](https://github.com/Veatch-Kinze/fleettrack/issues/13) | SEC-3 | No rate limiting or lockout on login endpoint | High | `src/app/api/auth/login/route.ts` |
| [#14](https://github.com/Veatch-Kinze/fleettrack/issues/14) | TST-1 | Zero test coverage -- no test files exist anywhere | High | `src/` (entire directory) |

---

## Open Issues -- Batch 2 (Non-blocking, Security + Tests + Code Quality)

| # | ID | Title | Severity | File |
|---|-----|-------|----------|------|
| [#17](https://github.com/Veatch-Kinze/fleettrack/issues/17) | SEC-4 | Mass assignment -- request body spread directly into DB writes | Medium | `src/app/api/machines/route.ts:46-50` + 6 other routes |
| [#18](https://github.com/Veatch-Kinze/fleettrack/issues/18) | SEC-5 | HTML injection in notification emails -- user content inserted unescaped | Low | `src/lib/notifications.ts:25-33` |
| [#19](https://github.com/Veatch-Kinze/fleettrack/issues/19) | TST-2 | No regression tests for critical security fixes from PR #2 | Medium | `src/lib/auth.ts`, `src/middleware.ts` |
| [#15](https://github.com/Veatch-Kinze/fleettrack/issues/15) | CQ-1 | Duplicate user-creation logic between register and admin/users | Medium | `src/app/api/auth/register/route.ts`, `src/app/api/admin/users/route.ts` |
| [#16](https://github.com/Veatch-Kinze/fleettrack/issues/16) | CQ-2 | Non-constant-time password comparison | Low | `src/lib/auth.ts:63-65` |

---

## Open Issues -- Batch 3 (Non-blocking, Decoupling)

| # | ID | Title | Severity | File |
|---|-----|-------|----------|------|
| [#20](https://github.com/Veatch-Kinze/fleettrack/issues/20) | DEC-1 | Raw user-supplied HTML stored in notifications.body column | Medium | `src/lib/notifications.ts:39-47` |
| [#21](https://github.com/Veatch-Kinze/fleettrack/issues/21) | DEC-2 | No .env.example -- required environment variables undocumented | Low | Project root |

---

## Additional Engineering Gaps (not yet filed)

These were identified in the initial assessment but not included in the formal harden audit (capped at 15 findings). Consider filing separately as the blocking issues are resolved.

- **No CI/CD pipeline.** No GitHub Actions. Any push to main auto-deploys with no automated checks.
- **No input validation.** No zod or yup. Malformed data can reach the database. (Related to [#17](https://github.com/Veatch-Kinze/fleettrack/issues/17))
- **No pagination.** All machines/logs fetched in a single request. Will degrade at scale.
- **No database indexes.** Queries on status, machineId, priority will slow down as data grows.
- **No monitoring or health checks.** No /health endpoint, no metrics, no alerting.
- **No automated backups.** SQLite on a Railway volume. If the volume fails, data is lost.
- **Generic error handling.** All API routes return generic 500 errors.
- **Spoofable x-forwarded-for in audit logs.** Used without validation.

---

## Mobile Readiness

Functional on mobile via Tailwind responsive breakpoints. Not optimized for touch:

- Some buttons are too small (6x6 pixel delete buttons)
- No mobile keyboard hints on numeric fields
- Images stored as base64 data URLs (heavy on mobile data)
- No PWA manifest or service worker (no offline support)
- No companion mobile app

---

## Ryan's Vision (from May 28 email)

Ryan wants FleetTrack to grow beyond machine maintenance into industrial job tracking:

- Ingest email/text work requests tied to a scheduling calendar
- Customer contact system with photos and property notes
- Job time tracking (tap start/end) with auto-generated invoices
- AI agent for reports and maintenance insights
- Companion mobile app or mobile-optimized web

The vision is achievable. The stack (Next.js + SQLite) is right for this scale. The architecture is clean enough to extend. But the hardening work listed above should happen before adding features. Building on top of weak foundations creates compounding problems.

---

## Recommended Priorities (in order)

1. Fix password hashing (argon2id) and remove default credentials ([#11](https://github.com/Veatch-Kinze/fleettrack/issues/11), [#12](https://github.com/Veatch-Kinze/fleettrack/issues/12))
2. Add rate limiting on login ([#13](https://github.com/Veatch-Kinze/fleettrack/issues/13))
3. Add vitest and write auth integration tests ([#14](https://github.com/Veatch-Kinze/fleettrack/issues/14), [#19](https://github.com/Veatch-Kinze/fleettrack/issues/19))
4. Add zod request validation on all API routes ([#17](https://github.com/Veatch-Kinze/fleettrack/issues/17))
5. Extract createUser helper to eliminate duplication ([#15](https://github.com/Veatch-Kinze/fleettrack/issues/15))
6. Set up GitHub Actions CI (lint + type-check + test gates)
7. Add pagination and database indexes
8. Set up automated SQLite backups
9. Add a /health endpoint and basic monitoring
10. Then start on new features (job tracking, mobile, AI)

---

## Bottom Line

FleetTrack is a solid first project. The codebase is clean, the architecture is sound, and Ryan shows good instincts (proper ORM, TypeScript, security awareness). It works today for a small trusted group tracking equipment.

It is not ready for untrusted users or a commercial product without the hardening work above. The foundation is there. The stack is right. Fix the security and testing gaps first, then build toward the bigger vision.
