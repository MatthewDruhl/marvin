# YPS-AI Code Review

**Date:** 2026-05-30
**Repo:** Your-Part-Source-Inc/yps-ai
**Scope:** Folder structure, code quality, dependencies, configuration, documentation, state management, security

---

## Critical Issues (Must Fix)

### SEC-1: Real OAuth Credentials in .env

- **File:** `.env`
- **Issue:** Live Google OAuth client ID and secret present. File is gitignored but if ever committed to history, credentials are permanently recoverable.
- **Risk:** Anyone with repo access can use these credentials to access the YPS Gmail account.
- **Action:** Regenerate OAuth credentials in Google Cloud Console immediately.

### SEC-2: Customer PII in Git History

- **Files:** `temp_ebay_messages.json`, `temp_inventory.csv`
- **Issue:** Committed to git before being gitignored (commit `8a56916`). Commits `c4fa68a`, `d3a3bb1`, `4efed85`, `f5faee8`, `ebc03e8` contain customer phone numbers, first names, eBay usernames.
- **Risk:** Anyone with read access can run `git show c4fa68a:temp_ebay_messages.json` and recover PII.
- **Fix:** Requires `git filter-repo` history rewrite + forced re-push + all collaborators re-clone.
- **Status:** Already documented in `findings.json` (SEC-1).

### TEST-1: PostToolUse Hook Broken on Windows (Validation Gate Offline)

- **File:** `scripts/validate-on-draft-save.js`, line 36
- **Issue:** Path normalization missing. On Windows, Claude Code passes paths with backslashes (`state\drafts.md`), but the gate checks `filePath.endsWith("state/drafts.md")` (forward slash). Hook silently exits without running validation.
- **Impact:** The 15-check validator (greeting, pricing, fitment warning, etc.) never fires on Windows. This is a critical safety gate that is effectively offline in production.
- **Fix:**
  ```javascript
  const normalized = filePath.replace(/\\/g, '/');
  if (!normalized.endsWith('state/drafts.md')) { process.exit(0); }
  ```

---

## High-Priority Issues

### CODE-1: Stale .xml File References

- **Files:** `.claude/commands/draft.md` (lines 7, 28), `.claude/commands/redraft.md` (lines 7, 66)
- **Issue:** Commands reference `temp_ebay_messages.xml` but the actual file is `temp_ebay_messages.json`.
- **Impact:** Every eBay-source `/draft` attempts to read a non-existent .xml, fails, then recovers. Token waste + operator confusion.
- **Fix:** Replace `temp_ebay_messages.xml` with `temp_ebay_messages.json` (4 lines).

### CODE-2: Validator Hook Runs with Incomplete Context

- **File:** `scripts/validate-on-draft-save.js`, lines 105-120
- **Issue:** Hook runs validator with hardcoded empty defaults: `productType=""`, `make=""`, `customerText=""`, `attachment=""`.
- **Impact:** 5 of 15 checks cannot fire (attachment-required, terminology-match, Dodge PN format, rebuilt-GM-ABS, no_volunteered_policy exceptions).
- **Fix:** Parse `queue.md` row for productType/make; extract attachment from drafts.md `**Attachment:**` line.

### No pytest Unit Tests for Python Modules

- Python modules (`jazva_notes.py`, `ingest.py`) are only tested via integration fixtures, not isolated unit tests.

---

## Medium-Priority Issues

- **PLAN.md outdated** -- references Phase 3/4 as future but Phase 1 is live. Mark as historical or version it.
- **CLAUDE.md path inconsistency** -- references `~/yps/` but actual path is repo root.
- **Folder naming inconsistency** -- `order_scan/` (snake_case) vs `coordination/`, `notifications/`.
- **No runtime .env validation** -- missing vars only fail when the relevant feature is called, not at startup.
- **State file schema not validated** -- if an operator manually edits and breaks a markdown table, no automated check catches it.
- **findings.json not linked from README** -- good audit data but not discoverable.
- **Test fixtures may contain real PII** -- `test/data/part_number_missing/email[1-6].txt` use realistic personal names. Confirm if synthetic or real.

---

## Strengths

- **Knowledge system is excellent.** Operator-graduated rules with citations and dates in `knowledge/`. Voice guide is detailed and practical.
- **28 deterministic tests** (D1-D28, ~2600 LOC) with CI gating via GitHub Actions.
- **PII lint (D21)** scans knowledge files for VINs, phone numbers, AWS keys.
- **Comprehensive .gitignore** (26 patterns covering state, temp data, secrets, artifacts).
- **Good documentation** -- CLAUDE.md (31.8 KB), handoff guide, setup guide, CI pipeline guide all thorough.
- **Safety-conscious design** -- prompt-injection threat model documented, draft-only mode by default, 15-check validator.
- **Defensive coding** -- Python scripts never echo env var values, error classes are structured, prod protection requires `--confirm-prod`.

---

## Recommendations (Priority Order)

1. **Rotate OAuth credentials** and verify `.env` was never committed to history (SEC-1)
2. **Rewrite git history** with `git filter-repo` to remove PII (SEC-2)
3. **Fix Windows path normalization** in validator hook -- one-line fix (TEST-1)
4. **Fix .xml references** in draft/redraft commands (CODE-1)
5. **Enrich validator hook context** by parsing queue.md (CODE-2)
6. **Add pytest** for Python modules
7. **Update PLAN.md** and documentation paths
8. **Link findings.json** from README
