# Harden Audit — `/skills/harden`

**Date:** 2026-04-10
**Target:** `/Users/matthewdruhl/.claude/skills/harden`
**Scrutiny Level:** Strict (planning to open-source + compliance flagged)
**Scopes:** All (Security, AI-Specific, Test Coverage, Code Quality, Decoupling)

**Covering:** Source code, config files, git history, dependencies, test coverage
**Not covering:** Infrastructure, CI/CD pipeline, database security, runtime monitoring

---

## Calibration

| Question | Answer |
|----------|--------|
| Visibility | Planning to open-source |
| Access | Open source |
| Deployment | Local only |
| Compliance | Yes (regulatory/legal requirements apply) |
| Known issues | None |
| Scrutiny | Strict — flag anything ambiguous |

---

## Scope 1 — Security

### Steel-man

The harden skill is local-only tooling with no network-facing surface. All subprocess calls in `harden-issues.py` use the list form of `subprocess.run()` — no `shell=True` anywhere. No hardcoded credentials found in any committed file. The `.gitignore` correctly excludes `findings.json`, `*.json`, and `token_usage.csv`. Git history shows no deleted sensitive files. The `gh` CLI is used as an external binary rather than constructing shell strings, which is the correct approach.

### Findings

### SEC-1: Arbitrary file deletion via --marker path in capture_tokens.py
**Severity:** Medium
**Blocking:** No
**Where:** `capture_tokens.py:95-96`
**What:** The marker file is unconditionally deleted at the end of `capture_tokens.py` using the caller-supplied `--marker` path. Any file path the current user can delete can be targeted.
**Proof:** Lines 95-96: `if marker_path and marker_path.exists(): marker_path.unlink()` — `marker_path` is fully controlled by the `--marker` CLI argument with no validation that it is within `/tmp` or any expected directory.
**Impact:** A user running the tool (or a script invoking it) with a crafted `--marker` path could silently delete an arbitrary file they own. Low likelihood in solo local use, but a real path-traversal-adjacent risk when shared or open-sourced.
**Surfaced by:** Code reading
**Fix:** Validate that `marker_path` is within `/tmp` (or a known temp directory) before calling `unlink()`. Example: `if marker_path and marker_path.exists() and str(marker_path).startswith('/tmp/'): marker_path.unlink()`

---

### SEC-2: findings.json body fields flow into gh CLI without length or content limits
**Severity:** Low
**Blocking:** No
**Where:** `harden-issues.py:42-65`
**What:** `build_body()` interpolates finding fields (what, proof, impact, fix) directly into the GitHub issue body with no size cap or content filter. A `findings.json` with crafted oversized or markdown-injection content will pass through verbatim.
**Proof:** Lines 44-65: f-string body template interpolates `f.get('what', '')`, `f.get('proof', '')`, `f.get('impact', '')`, `f.get('fix', '')` with no truncation, stripping, or length checks.
**Impact:** GitHub issue body can be arbitrarily large, potentially causing API rejection or very long issues. Markdown injection (e.g., hidden HTML) goes into issues. Impact is low given GitHub's own rendering protections, but relevant when open-sourcing the tool.
**Surfaced by:** Inversion
**Fix:** Add a `MAX_BODY_LEN` constant (e.g., 65535) and truncate body before passing to `gh`. Optionally strip or escape raw HTML tags in user-provided fields.

---

## Scope 2 — AI-Specific Gaps

*`references/ai-audit-checklist.md` loaded at start of this scope per phase gate.*

### Steel-man

The harden skill's SKILL.md is thoughtfully structured with explicit phase gates, steel-manning requirements before findings, and a cap on findings to prevent noise. The background agent pattern is appropriate — isolating long-running analysis to avoid blocking the user. The `capture_tokens.py` script correctly scopes itself to reading only token metadata from JSONL, not full conversation content. The phase gate rules (load reference files only when triggered) demonstrate intentional token efficiency design.

### Findings

### AI-1: Background agent spawned with unconstrained file system access
**Severity:** High
**Blocking:** Yes
**Where:** `SKILL.md:45-68`
**What:** The background agent launched in Phase 0.5 is given a prompt that grants it the authority to write findings, but the MARVIN CLAUDE.md grants full permission to read/write/edit/create all files in `~/marvin/` without confirmation. The agent inherits this permission boundary with no narrowing — it can write to any marvin state file, not just the audit output.
**Proof:** SKILL.md lines 45-68 instruct the background agent to follow all SKILL.md instructions and write findings to `findings.json`. MARVIN CLAUDE.md states "Full permission to read, write, edit, and create files within ~/marvin/ without asking for confirmation." No scope narrowing is applied to the background agent in the prompt.
**Impact:** A prompt injection in an audited codebase's files (e.g., a CLAUDE.md containing adversarial instructions read during audit) could cause the background agent to modify marvin state files (current.md, goals.md, decisions.md) without user awareness.
**Surfaced by:** AI Audit Checklist — Check 8 (Agent Permission Boundaries)
**Fix:** Add explicit scope restrictions to the background agent prompt: "Only write to [target findings.json path] and the audit report output file. Do not modify any other files." This narrows the effective permission boundary even if the harness doesn't enforce it technically.

---

### AI-2: Token capture reads Claude Code session JSONL which may contain conversation history with PII
**Severity:** Medium
**Blocking:** No
**Where:** `capture_tokens.py:36-54`
**What:** `sum_tokens()` opens and parses Claude Code session JSONL files from `~/.claude/projects/`. These files contain the full conversation history of the agent session, including any PII, secrets, or sensitive data the user discussed in that session.
**Proof:** Lines 20-33: `find_agent_jsonl()` globs `~/.claude/projects/<project-hash>/*/subagents/*.jsonl`. Lines 40-53: iterates every line of the JSONL. Only token counts are extracted, but the full entry dict is loaded into memory on each iteration.
**Impact:** If `capture_tokens.py` is ever extended with logging, debugging, or error reporting that dumps locals/stack frames, conversation content could leak. Low risk for solo local use, but relevant when open-sourcing — contributors who add logging could inadvertently expose session content.
**Surfaced by:** AI Audit Checklist — Check 7 (Context Window Stuffing / Data Exfiltration)
**Fix:** Add a docstring warning that this function reads conversation history. Consider accessing only the `message.usage` sub-key rather than loading the full entry: `entry.get("message", {}).get("usage", {})` (already done) — but add a comment noting that `entry` is discarded immediately and not stored.

---

### AI-3: Phase gate rules enforced only by instruction — no programmatic guard prevents early loading
**Severity:** Low
**Blocking:** No
**Where:** `SKILL.md:9-13`
**What:** The phase gates for `ai-audit-checklist.md` and `engineering-blind-spots.md` are prose instructions only. An AI agent can (and sometimes will) read these files early due to pattern matching, context bleed, or misunderstanding the gate condition.
**Proof:** SKILL.md lines 9-13 state the phase gate rule in comments: "Load at the start of Scope 2, not before." There is no code, assertion, or tooling that enforces this — the agent could read the file at any point.
**Impact:** If an agent loads `engineering-blind-spots.md` when there are already 2+ findings, it wastes tokens without value. Primarily a token-efficiency concern rather than correctness. Critical/High findings remain unaffected.
**Surfaced by:** Inversion
**Fix:** Add a structured comment block at the top of each reference file: `<!-- PHASE GATE: Do not read before [trigger condition] -->` to reinforce the instruction at point-of-access. This is a soft reinforcement; no hard technical enforcement is feasible in a prompt-based system.

---

## Scope 3 — Test Coverage

### Steel-man

`test_score_audit.py` is genuinely thorough — it covers `points_to_grade()` at all boundary values, the critical floor override, the conventional rounding fix, CLI error paths (invalid JSON, empty input), blocking vs. non-blocking column output, and multi-scope sorting. The test for banker's rounding (`test_overall_grade_conventional_rounding`) shows active awareness of a real bug that was previously fixed. The test structure is clean, uses `capsys` correctly, and runs without external dependencies.

### Findings

### TEST-1: No tests for harden-issues.py — the only script with subprocess calls and external side effects
**Severity:** High
**Blocking:** Yes
**Where:** `harden-issues.py:68-93`
**What:** `harden-issues.py` contains the only `subprocess.run()` call in the codebase and has real external side effects (filing GitHub issues). It has zero test coverage. The validation logic (lines 127-138) and batch sorting (line 142) are also untested.
**Proof:** `tests/` directory contains only `test_score_audit.py` and `__init__.py`. No test file exists for `harden-issues.py`. The `create_issue()` function fires live `gh` CLI calls with no mock path in tests.
**Impact:** Bugs in `create_issue()`, `build_body()`, or the validation loop cannot be caught before they fire real `gh` CLI calls. A regression in label construction or body formatting will only be discovered when issues are actually filed.
**Surfaced by:** Code reading
**Fix:** Add `tests/test_harden_issues.py` with: (1) `test_build_body` verifies field interpolation, (2) `test_create_issue_dry_run` mocks `subprocess.run` and verifies `cmd` construction, (3) `test_validation_missing_fields` verifies the error path. Use `unittest.mock.patch` for `subprocess.run`.

---

### TEST-2: validate_findings.py and capture_tokens.py have no tests despite being in the validation pipeline
**Severity:** Medium
**Blocking:** No
**Where:** `validate_findings.py:20-38`, `capture_tokens.py:36-54`
**What:** `validate_findings.py` is the entry point for the findings pipeline and has no dedicated tests. `capture_tokens.py` has no tests for its JSONL parsing logic. Both are called by the audit workflow with no safety net.
**Proof:** `tests/test_score_audit.py` contains 0 imports of `validate_findings` or `capture_tokens`. The `validate()` function in `validate_findings.py:20-38` is the sole gate before `score_audit.py` — if it silently passes invalid data, `score_audit.py` will produce wrong grades.
**Impact:** A malformed `findings.json` that passes `validate_findings.py` but produces wrong scores in `score_audit.py` would generate an incorrect audit report that could be used to create GitHub issues with wrong severity or batch assignments.
**Surfaced by:** Code reading
**Fix:** Add `tests/test_validate_findings.py` covering: (1) missing required fields, (2) invalid severity value, (3) `blocking` non-boolean, (4) empty input. Add `tests/test_capture_tokens.py` covering `sum_tokens()` with fixture JSONL data including cache tokens.

---

## Scope 4 — Code Quality

### Steel-man

The Python code is clean and consistent within each file. Type hints are used throughout (Python 3.12+ style with `dict[str, int]`, `list[tuple]`). Error handling is explicit — JSON parse errors are caught and reported with meaningful messages. The `score_audit.py` grading logic uses named constants (`SEVERITY_POINTS`, `GRADE_THRESHOLDS`, `GRADE_TO_GPA`) rather than magic numbers. The `argparse` usage is standard and consistent across CLI scripts.

### Findings

### QUAL-1: REQUIRED_FIELDS defined differently in validate_findings.py and harden-issues.py — silent schema divergence
**Severity:** High
**Blocking:** Yes
**Where:** `validate_findings.py:17`, `harden-issues.py:39`
**What:** `validate_findings.py` defines `REQUIRED_FIELDS` as `('scope', 'severity', 'blocking')` — 3 fields. `harden-issues.py` defines `REQUIRED_FIELDS` as `{'id', 'title', 'scope', 'severity', 'blocking', 'where', 'what', 'fix', 'batch'}` — 9 fields. A `findings.json` that passes `validate_findings.py` can still fail `harden-issues.py`'s validation.
**Proof:** `validate_findings.py` line 17: `REQUIRED_FIELDS = ('scope', 'severity', 'blocking')`. `harden-issues.py` line 39: `REQUIRED_FIELDS = {'id', 'title', 'scope', 'severity', 'blocking', 'where', 'what', 'fix', 'batch'}`. These are entirely different sets with no shared definition.
**Impact:** SKILL.md instructs running `validate_findings.py` first as a gate, but this gives false confidence — a validated `findings.json` can still cause `harden-issues.py` to fail after the user approves the batch plan. Confusing UX and wasted cycles.
**Surfaced by:** Code reading
**Fix:** Create a shared `schema.py` module with one `REQUIRED_FIELDS` definition containing all fields required by the full pipeline. Both scripts import from it. Alternatively, make `validate_findings.py` validate the full `harden-issues.py` field set (the superset).

---

### QUAL-2: score_audit.py grading formula duplicated in SKILL.md — two sources of truth
**Severity:** Medium
**Blocking:** No
**Where:** `score_audit.py:1-12`, `SKILL.md:189-205`
**What:** The grading formula (Critical=4pts, High=3, Medium=2, Low=1; grade thresholds A/B/C/D/F; critical floor rule) is documented in both `score_audit.py`'s docstring and SKILL.md's Scorecard section. When one changes, the other silently drifts.
**Proof:** `score_audit.py` lines 1-12 define the full formula in the module docstring. `SKILL.md` lines 189-205 restate the same formula in the Scorecard section with identical thresholds. These are independent copies with no cross-reference.
**Impact:** If the grading formula is updated in `score_audit.py` (e.g., adding a new severity tier), SKILL.md won't be updated and agents will apply the wrong mental model. This already caused a rounding bug fixed in commit `d0257f8` — the prose in SKILL.md didn't catch it.
**Surfaced by:** Inversion
**Fix:** Remove the formula from SKILL.md's Scorecard section and replace with: "Run `score_audit.py` — it is the source of truth for the grading formula. See the script docstring for the formula." Keep the grade table as a quick-reference summary only, not a redefinition.

---

### QUAL-3: No linter or formatter configured — no ruff/flake8/black config present
**Severity:** Low
**Blocking:** No
**Where:** `/Users/matthewdruhl/.claude/skills/harden/` (directory)
**What:** The harden skill directory has no `pyproject.toml`, `ruff.toml`, `.flake8`, or `setup.cfg` configuring a Python linter or formatter. Before open-sourcing, contributors will have no enforced style baseline.
**Proof:** Directory listing shows: SKILL.md, capture_tokens.py, harden-issues.py, score_audit.py, token_log.py, validate_findings.py, .gitignore, tests/, references/. No pyproject.toml or linter config present.
**Impact:** Contributions will introduce style drift. Ruff would also catch real bugs (unused imports, shadowed variables). Low urgency for solo use, but required before open-sourcing.
**Surfaced by:** Code reading
**Fix:** Add a `pyproject.toml` with `[tool.ruff]` section: `line-length = 100`, `select = ['E', 'F', 'I']`. Add a pre-commit hook or CI step to enforce it.

---

## Scope 5 — Decoupling & Data Separation

### Steel-man

The `.gitignore` correctly excludes both `findings.json` and `token_usage.csv` from commits. The skill's Python scripts have clean single-responsibility design — each script does one thing. There is no circular dependency between scripts (none import each other). The reference files are appropriately separated from operational scripts. The MARVIN workspace file layout (`content/`, `state/`, `skills/`) provides clear separation between user data and skill code.

### Findings

### DECOUP-1: token_usage.csv written inside the skills repo directory — data mixed with code
**Severity:** Medium
**Blocking:** No
**Where:** `capture_tokens.py:9`, `token_log.py:8`
**What:** Both `capture_tokens.py` and `token_log.py` write `token_usage.csv` to `Path(__file__).parent` — the same directory as the Python source files. This mixes generated runtime data with code in the skills directory.
**Proof:** `capture_tokens.py` line 9: `LOG_FILE = Path(__file__).parent / 'token_usage.csv'`. `token_log.py` line 8: `LOG_FILE = os.path.join(os.path.dirname(__file__), 'token_usage.csv')`. Both resolve to `/Users/matthewdruhl/.claude/skills/harden/token_usage.csv`.
**Impact:** When open-sourced, the `.gitignore` entry correctly excludes it, but if the skill is installed in a read-only location or shared across users, writes will fail silently or require elevated permissions.
**Surfaced by:** Decoupling Blind Spots — hardcoded paths
**Fix:** Write `token_usage.csv` to a user data directory: `~/.claude/harden/token_usage.csv`. Use `Path.home() / '.claude' / 'harden' / 'token_usage.csv'` and create the directory if needed with `path.mkdir(parents=True, exist_ok=True)`.

---

### DECOUP-2: SKILL.md tightly couples audit instructions to specific output file locations without parameterization
**Severity:** Low
**Blocking:** No
**Where:** `SKILL.md:59-65`
**What:** The background agent prompt template hardcodes that findings land in `findings.json` in the audited project directory. There is no way to redirect output to a different location without editing SKILL.md.
**Proof:** SKILL.md lines 59-65: "Write findings to `findings.json` in the audited project directory." The output path is fully specified inline with no variable or parameter.
**Impact:** When multiple audits run against the same project in sequence, `findings.json` is overwritten with no versioning. Users cannot redirect output to a timestamped file without manual SKILL.md edits.
**Surfaced by:** Decoupling Blind Spots — hardcoded paths
**Fix:** Add an optional output path parameter to Phase 0 calibration, defaulting to `findings-{YYYY-MM-DD}.json` in the audited directory. Pass this as a bracketed variable in the background agent prompt template.

---

## Scorecard

| Scope | Grade | Blocking | Non-blocking |
|-------|-------|----------|--------------|
| AI-Specific | C | 1 high | 1 medium, 1 low |
| Code Quality | C | 1 high | 1 medium, 1 low |
| Decoupling | B | — | 1 medium, 1 low |
| Security | B | — | 1 medium, 1 low |
| Test Coverage | C | 1 high | 1 medium |

**Overall: C**

*Verified by: `uv run python validate_findings.py findings.json && uv run python score_audit.py findings.json`*

---

## Verdict

**Ship with changes** — 4 blocking findings need fixing first.

The tool's core logic (`score_audit.py`, `validate_findings.py`) is solid. The blocking issues are:
1. `QUAL-1` — Schema divergence between `validate_findings.py` and `harden-issues.py` creates false confidence in the validation pipeline
2. `TEST-1` — The only script with real external side effects (`harden-issues.py`) has zero tests
3. `AI-1` — Background agent has unconstrained file system access with no scope narrowing
4. `QUAL-1` is the most dangerous pre-open-source issue — it means the pipeline appears validated when it isn't

---

## Batch Plan

### Batch 1 — Fix blocking issues before open-source (3 issues)
Resolves: QUAL-1, TEST-1, AI-1
Blocking: Yes — must fix before shipping
Dependency: None — do this first
Effort: Medium

- **QUAL-1:** Create `schema.py` with shared `REQUIRED_FIELDS`; update both scripts to import from it
- **TEST-1:** Add `tests/test_harden_issues.py` with mocked subprocess; cover `build_body`, label construction, validation
- **AI-1:** Add explicit file scope restriction to background agent prompt in SKILL.md

### Batch 2 — Pipeline integrity and security hardening (3 issues)
Resolves: SEC-1, TEST-2, QUAL-2, DECOUP-1
Blocking: No — quality improvements
Dependency: Batch 1 (schema.py enables cleaner validate_findings.py tests)
Effort: Medium

- **SEC-1:** Validate `--marker` path is within `/tmp` before `unlink()`
- **TEST-2:** Add `tests/test_validate_findings.py` and `tests/test_capture_tokens.py`
- **QUAL-2:** Remove grading formula from SKILL.md; make `score_audit.py` the single source of truth
- **DECOUP-1:** Move `token_usage.csv` to `~/.claude/harden/`

### Batch 3 — Polish and open-source readiness (4 issues)
Resolves: SEC-2, AI-2, AI-3, QUAL-3, DECOUP-2
Blocking: No — polish
Dependency: Batches 1 and 2 complete
Effort: Low

- **SEC-2:** Add `MAX_BODY_LEN` truncation to `build_body()`
- **AI-2:** Add data-sensitivity comment to `capture_tokens.py`
- **AI-3:** Add phase gate comment headers to reference files
- **QUAL-3:** Add `pyproject.toml` with ruff config
- **DECOUP-2:** Parameterize output file path in SKILL.md background agent prompt

---

*Ready to create GitHub issues? I'll file them in batch order.*
