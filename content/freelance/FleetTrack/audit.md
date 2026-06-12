# FleetTrack — Port / Rebuild Audit

> **Purpose:** A read-only study of the shipped FleetTrack application, intended
> for someone evaluating a rebuild on a more robust tech stack (and/or hosting it
> inside an existing project). Focuses on *scope, data model, business rules, and
> debt* — not implementation details to copy verbatim.
>
> **Method:** Reverse-engineered from the schema, all API route handlers,
> auth/middleware, email + notification libs, seed, and `SECURITY_REVIEW.md`
> (as of 2026-06). Companion docs: [`product/product-spec.md`](product/product-spec.md),
> [`product/user-stories.md`](product/user-stories.md), and the rebuild guide
> [`../PORTING.md`](../PORTING.md).

---

## 1. What it actually is

A **single-tenant, role-based CRUD app** for one organization's mixed equipment
fleet. There is **no multi-org concept** — every user shares one fleet.
Functionally it is:

- an **asset registry** (machines), plus
- four **child log types** (maintenance, repairs, issues, notes), plus
- a **usage time-series**, plus
- two **reusable contact lists** (dealerships, service techs), plus
- **email alerts** on issues, plus
- an **admin panel** (users, access log, notification log).

That is the entire product. It maps cleanly onto a conventional "records with
sub-resources and RBAC" shape, which makes it a low-risk port.

> ⚠️ **Stale documentation warning.** `memory-bank/product.md`, `brief.md`,
> `architecture.md`, and `tech.md` are leftover boilerplate from the Next.js
> starter template this project was forked from — they describe a generic
> template, not FleetTrack. Do not treat them as authoritative. The `spec/`
> documents and the code are the real source of truth.

## 2. Data model (tech-agnostic — the part worth carrying over)

11 tables. FKs to `machines` are `ON DELETE CASCADE` unless noted.

| Entity | Key fields | Notes |
|---|---|---|
| **users** | username (unique), passwordHash, displayName, role (`admin`/`mechanic`/`viewer`), email, phone, lastLoginAt, isActive, notifyByEmail, createdAt | role enum + soft-active flag + per-user email-notify toggle |
| **machines** | name, category (6-value enum), make/model/year/vin/serialNumber/color/description, purchaseDate/purchasePrice, currentHours, currentMiles, trackingType (`hours`/`miles`/`both`), status (`active`/`sold`/`inactive`), statusNote/statusDate, imageUrl, **dealershipId + serviceTechId AND denormalized dealershipName/serviceTechName/serviceTechPhone**, created/updatedAt | central record |
| **maintenance_logs** | date, type, description, performedBy, hoursAtService, milesAtService, **nextServiceHours/Miles/Date**, cost, parts (JSON-in-text), notes | scheduled/routine service |
| **repair_logs** | date, description, performedBy, shopName, hoursAtRepair, milesAtRepair, cost, laborCost, partsCost, parts (JSON-in-text), warrantyWork, notes | corrective work |
| **machine_notes** | category, title, content | reference info |
| **issues** | title, description, priority (`low`/`medium`/`high`/`critical`), status (`open`/`in_progress`/`resolved`), imageUrl, reportedBy/reportedDate, resolvedBy/resolvedDate, resolutionNotes, resolutionCost | defect tracking |
| **usage_history** | date, hours, miles | time-series |
| **dealerships** | name (unique), phone, isArchived | reusable list |
| **service_techs** | name, phone, dealershipId, isArchived | reusable list |
| **access_log** | userId, username, action (`login_success`/`login_failed`/`logout`), ipAddress, userAgent, createdAt | audit trail |
| **notifications** | type (`issue_created`/`issue_resolved`), recipientId, issueId, machineId, subject, body, status (`sent`/`failed`), sentAt | email send log |

### Enums (preserve these)
- **MachineCategory:** `ag`, `construction`, `vehicle`, `atv_suv`, `marine`, `other`
- **MachineStatus:** `active`, `sold`, `inactive`
- **TrackingType:** `hours`, `miles`, `both`
- **IssuePriority:** `low`, `medium`, `high`, `critical`
- **IssueStatus:** `open`, `in_progress`, `resolved`
- **UserRole:** `admin`, `mechanic`, `viewer`

## 3. Business rules / behaviors worth preserving

These are encoded in route handlers and easily lost in a rebuild:

1. **Monotonic usage** — `currentHours` / `currentMiles` can only stay the same
   or increase. Enforced in *both* the quick-update UI and the
   `PUT /api/machines/[id]` handler (returns 400 on a backwards value).
2. **Auto usage-history** — when a machine's hours/miles change on update, a
   `usage_history` row is auto-inserted dated today. The time-series is a side
   effect of edits, not separately managed.
3. **Issue → email triggers** — creating an issue emails all active admins with
   `notifyByEmail` + an email on file. Resolving an issue (status transitioning
   *to* `resolved` from a non-resolved state) emails them again, including
   `resolvedBy`. Both are **fire-and-forget** (`.catch()` logged), so email
   never blocks or fails the request, and every attempt writes a `notifications`
   row with `sent`/`failed`.
4. **RBAC matrix** —
   - `GET` on data routes → any authenticated role (admin/mechanic/viewer)
   - `POST`/`PUT`/`DELETE` on data routes → admin or mechanic (viewer read-only)
   - `/api/admin/*` → admin only

   Enforced server-side per route, *plus* edge middleware that HMAC-verifies the
   session cookie and redirects (pages) or 401s (APIs) before the route runs.
5. **Cascade deletes** — deleting a machine removes all its logs, issues, notes,
   and usage history.
6. **trackingType drives the UI** — hours-only machines hide miles fields and
   vice-versa; `both` shows both.
7. **Archive** — status `sold` or `inactive`; carries a reason note + date and
   leaves the active inventory.
8. **Session model** — HMAC-SHA256 signed cookie
   `base64url(userId:issuedAt).base64url(sig)`, 7-day **server-enforced** TTL
   (independent of cookie Max-Age), `isActive` re-checked on every request.
   Stateless — no individual revocation.
9. **Login auditing** — every login success, login failure, and logout writes an
   `access_log` row with IP + user agent. `lastLoginAt` updated on success.

## 4. External integration points

- **Email:** Resend (HTTP API) is primary **specifically because Railway blocks
  outbound SMTP ports 465/587**; nodemailer/Gmail SMTP is a dev-only fallback.
  On a host that permits SMTP, this constraint disappears.
- **Database:** SQLite via better-sqlite3 — single embedded file. On Railway it
  needs a mounted volume or it is ephemeral.
- **Images:** `imageUrl` (on machines and issues) is **just a text field — there
  is no upload mechanism.** Obvious upgrade point if the host has blob storage.
- **Env vars:** `DATABASE_URL`, `SESSION_SECRET` (≥32 chars; hard-fails startup
  in production if missing), `RESEND_API_KEY`, `RESEND_FROM`,
  `GMAIL_USER` / `GMAIL_APP_PASSWORD`.

## 5. Known debt — do NOT carry these over

`SECURITY_REVIEW.md` is candid. Criticals were fixed (session forgery, open API
routes, missing route protection). **Still open / to address in a rebuild:**

| Area | Issue | Recommended fix |
|---|---|---|
| Password hashing | Unsalted SHA-256 + single global pepper, no stretching | argon2id / bcrypt with per-user salt |
| Seeded admin | `rveatch` / `rveatch` committed in `seed.ts` | Require env-supplied or random one-time password |
| Mass assignment | Handlers spread `...req.body` straight into insert/update, no allow-list | Validation layer (zod/valibot), explicit field picks |
| Login | No rate limiting / lockout | Per-IP + per-account throttle |
| Email | User-supplied issue title/description interpolated unescaped into HTML | Escape before embedding |
| Audit | `x-forwarded-for` trusted directly (spoofable) | Derive IP from trusted proxy hop |
| Sessions | Stateless, no revocation | Token-version column or server-side session store |
| Tests | None anywhere | Add coverage for the §3 rules |

### Modeling smells to fix while porting
- **Denormalized dealership/tech** — machines carry both FK *and* copied
  name/phone strings; these can drift. Keep the FK, drop the copies, join.
- **Dates as text** — `purchaseDate` is "ISO string *or the literal `N/A`*"; log
  dates are text. Use real date/timestamp types.
- **`parts` as JSON-in-a-text-column** — promote to a typed column or a child
  table if you ever need to query it.

## 6. Surface inventory

- **Pages (10):** `/` (dashboard), `/login`, `/register`, `/machines`,
  `/machines/new`, `/machines/[id]`, `/machines/[id]/edit`, `/quick-usage`,
  `/archive`, `/admin`.
- **API routes (~26):** auth (login/logout/me/register), dashboard, machines
  (+ nested maintenance / repairs / notes / issues / usage-history), dealerships,
  service-techs, and admin (users + reset-password + test-email, access-log,
  notifications). Full list and methods in [`../PORTING.md`](../PORTING.md).
- **Machine detail tabs:** Overview, Maintenance, Repairs, Notes, Issues.

## 7. Bottom line

The domain is plain CRUD + RBAC + transactional email + a small time-series.
The valuable, hard-to-reconstruct parts are the **data model (§2)** and the
**business rules (§3)** — port those deliberately. The UI is mostly forms over
the API and can be rebuilt last. The security/modeling debt (§5) is well
understood and should be fixed *as part of* the rebuild rather than copied.
See [`../PORTING.md`](../PORTING.md) for the host-fit checklist and port order.
</content>
