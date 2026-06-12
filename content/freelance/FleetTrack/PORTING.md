# FleetTrack — Porting & Rebuild Guide

> A practical guide for rebuilding FleetTrack on a more robust tech stack, or
> hosting it inside an existing application. Pairs with the read-only
> [`spec/audit.md`](spec/audit.md) (findings & debt) and
> [`spec/product/`](spec/product/) (scope & user stories).
>
> The current stack is Next.js 16 + SQLite (better-sqlite3) + Drizzle, custom
> session auth, Resend email, deployed on Railway. This guide is **stack-agnostic**
> — it tells you *what* to recreate, not *how* in a specific framework.

---

## 1. Host-fit checklist

FleetTrack's domain is CRUD + RBAC + transactional email + a small time-series,
so most modern app foundations can host it. A candidate host should provide:

| Need | Why | Priority |
|---|---|---|
| **Auth + RBAC**, ≥3 role tiers | Map onto `admin` / `mechanic` / `viewer` (or a permissions model) | Required |
| **Relational DB** with FK cascades + migrations | 11 related tables; cascade delete from machines | Required |
| **Transactional email** | Issue create/resolve alerts to admins | Required |
| **Background job / queue** | Move email out of the request path (today it's fire-and-forget) | Recommended |
| **Object / blob storage** | Upgrade `imageUrl` text fields to real machine + issue photo uploads | Recommended |
| **Multi-tenancy** | Only if the host is multi-org — see §5 | Conditional |

If the host **permits outbound SMTP**, you can drop the Resend-specific
workaround (it exists only because Railway blocks SMTP ports 465/587).

## 2. Recommended port order

Port the *logic* first, the *UI* last:

1. **Schema** — recreate the 11 tables (§3) with the corrections from
   `spec/audit.md` §5 (real dates, no denormalized contact copies, typed
   `parts`, strong password hashing column). Prefer Postgres over SQLite for
   concurrency and proper date/JSON types.
2. **Auth + RBAC** — sessions/tokens, the role matrix (§4), `isActive`
   enforcement, and login auditing.
3. **Business rules** — the non-obvious logic that defines the product
   (§4 below): monotonic usage + auto usage-history, issue email triggers,
   cascade deletes, archive semantics.
4. **API surface** — the ~26 endpoints (§6), with a validation layer
   (zod/valibot) replacing the current mass-assignment pattern.
5. **UI** — dashboard, machine inventory + detail tabs, quick-usage, archive,
   admin panel. Mostly forms over the API; rebuild last.

## 3. Data model (ERD)

```
                         ┌──────────────┐
                         │    users     │
                         │  role enum   │
                         └──────┬───────┘
            recipientId │       │ userId
        ┌───────────────┘       └───────────────┐
        │                                        │
┌───────▼────────┐                       ┌───────▼────────┐
│ notifications  │                       │   access_log   │
└───────┬────────┘                       └────────────────┘
        │ issueId / machineId
        │
┌───────────────┐         ┌──────────────┐        ┌────────────────┐
│  dealerships  │◄────────│   machines   │───────►│  service_techs │
│  (reusable)   │ FK +    │   (central)  │  FK +  │   (reusable)   │
└───────────────┘ denorm  └──────┬───────┘ denorm └───────┬────────┘
                                  │ machineId (CASCADE)    │ dealershipId
        ┌─────────────┬───────────┼────────────┬──────────┴────┐
        ▼             ▼           ▼            ▼                ▼
┌──────────────┐ ┌─────────┐ ┌────────┐ ┌────────────┐ ┌───────────────┐
│maintenance_  │ │repair_  │ │ issues │ │machine_    │ │ usage_history │
│logs          │ │logs     │ │        │ │notes       │ │ (time-series) │
└──────────────┘ └─────────┘ └────────┘ └────────────┘ └───────────────┘
```

- **machines** is the hub; all child records cascade-delete with it.
- **dealerships** / **service_techs** are referenced by machines (and a tech
  belongs to a dealership). Today machines *also* copy name/phone inline — drop
  that in the rebuild and join instead.
- **notifications** and **access_log** reference users for audit/logging.

Full column lists and enum values are in [`spec/audit.md`](spec/audit.md) §2.

## 4. Business rules to re-implement

These define the product; don't lose them in translation:

1. **Monotonic usage.** `currentHours` / `currentMiles` may only stay equal or
   increase. Reject backwards values (HTTP 400) — enforce server-side, not just
   in the UI.
2. **Auto usage-history.** On any machine update where hours/miles changed,
   insert a `usage_history` row dated today. Powers the usage-over-time graph.
3. **Issue notifications.**
   - On **create** → email every active admin with `notifyByEmail` + an email.
   - On **resolve** (status → `resolved` from a non-resolved state) → email them
     again, including who resolved it.
   - Send asynchronously (don't fail the request on email error); log each
     attempt to `notifications` with `sent`/`failed`. A queue is the clean home
     for this.
4. **RBAC matrix.** GET = any authed role; mutations = admin/mechanic; viewer is
   read-only; `/admin/*` = admin only. Enforce at the edge/middleware AND
   per-route.
5. **Sessions.** Server-enforced TTL (7 days), re-check `isActive` every request.
   Add revocation in the rebuild (token-version column or server-side store).
6. **Archive semantics.** Status `sold`/`inactive` leaves the active inventory,
   carries a reason note + date, and shows in the archive view.
7. **trackingType-driven forms.** Show hours and/or miles fields based on the
   machine's `hours` / `miles` / `both` tracking type.
8. **Login auditing.** Record success/failure/logout with IP + user agent;
   update `lastLoginAt` on success.

## 5. The multi-tenancy decision

FleetTrack is **single-fleet** today — one shared organization, no tenant key
anywhere. This is the single biggest structural choice when hosting it inside a
multi-tenant app:

- **Keep single-tenant** → simplest; deploy one instance per organization.
- **Make multi-tenant** → add an `organizationId` (or `tenantId`) to **every**
  table, scope **every** query by it, and scope uniqueness constraints
  (e.g. `username` and `dealerships.name` become unique *per org*). This touches
  all routes and the auth layer — plan for it up front, not as a retrofit.

## 6. API surface (port targets)

Roughly 26 endpoints. Methods reflect the RBAC matrix in §4.

### Auth (public except `register`/`me` behavior noted)
| Method | Path | Purpose |
|---|---|---|
| POST | `/api/auth/login` | Authenticate, set session cookie, audit |
| POST | `/api/auth/logout` | Clear session, audit |
| GET  | `/api/auth/me` | Current user (null if unauthenticated) |
| POST | `/api/auth/register` | Create account (defaults to `mechanic`) |

### Core data (GET = any authed; writes = admin/mechanic)
| Method | Path | Purpose |
|---|---|---|
| GET/POST | `/api/machines` | List (filter by status/category) / create |
| GET/PUT/DELETE | `/api/machines/[id]` | Read / update (usage rules) / delete (cascade) |
| GET/POST | `/api/machines/[id]/maintenance` | List / add maintenance |
| PUT/DELETE | `/api/machines/[id]/maintenance/[logId]` | Edit / remove |
| GET/POST | `/api/machines/[id]/repairs` | List / add repair |
| PUT/DELETE | `/api/machines/[id]/repairs/[logId]` | Edit / remove |
| GET/POST | `/api/machines/[id]/notes` | List / add note |
| PUT/DELETE | `/api/machines/[id]/notes/[noteId]` | Edit / remove |
| GET/POST | `/api/machines/[id]/issues` | List / report (→ email) |
| PUT/DELETE | `/api/machines/[id]/issues/[issueId]` | Update (resolve → email) / remove |
| GET | `/api/machines/[id]/usage-history` | Usage time-series |
| GET/POST | `/api/dealerships`, `/api/dealerships/[id]` | Reusable dealership list |
| GET/POST | `/api/service-techs`, `/api/service-techs/[id]` | Reusable tech list |
| GET | `/api/dashboard` | Active count, open issues, recent maintenance, by-category |

### Admin only (`/api/admin/*`)
| Method | Path | Purpose |
|---|---|---|
| GET/POST | `/api/admin/users` | List / create users |
| PUT/DELETE | `/api/admin/users/[id]` | Edit / deactivate |
| POST | `/api/admin/users/[id]/reset-password` | Reset a user's password |
| POST | `/api/admin/users/[id]/test-email` | Send a test email |
| GET | `/api/admin/access-log` | Recent login/logout activity |
| GET | `/api/admin/notifications` | Recent notification send log |

## 7. Do-not-copy list (carry the fixes, not the bugs)

From [`spec/audit.md`](spec/audit.md) §5 — address these *during* the rebuild:

- Replace SHA-256+pepper hashing with **argon2id/bcrypt + per-user salt**.
- Never commit a default admin credential; require env-supplied/random.
- Add **input validation**; stop spreading raw request bodies into writes.
- Add **login rate limiting / lockout**.
- **Escape user content** before embedding in notification email HTML.
- Derive client IP from a **trusted proxy hop**, not raw `x-forwarded-for`.
- Add **session revocation**.
- Fix the modeling smells: real date types, drop denormalized contact copies,
  typed `parts`.
- Add **tests** for the §4 business rules.
</content>
