---
description: Audit a software project for hardening — security, AI gaps, test coverage, code quality, and decoupling. Use when user wants to harden a project, audit for vulnerabilities, check test coverage, or separate private data from code.
---

Perform a systematic hardening audit of this project. Work through each phase below, exploring the codebase to find real issues — not hypothetical ones.

## Reference Files

**Phase gates — load only when triggered. Do not read before the gate.**

- [ai-audit-checklist.md](references/ai-audit-checklist.md) — Extended AI checks. Load at the start of Scope 2, not before.
- [engineering-blind-spots.md](references/engineering-blind-spots.md) — Detection questions by scope. Load only if initial findings for a scope total fewer than 2.

## Phase 0: Context Gathering

Use `AskUserQuestion` to present all calibration questions at once:

| # | Question | Options |
|---|----------|---------|
| 1 | Is this repo private or could it go public? | Private / Public / Planning to open-source |
| 2 | Who has access to this codebase? | Just me / Small team / Open source |
| 3 | Where does this run? | Local only / Server/cloud / Not deployed yet |
| 4 | Any regulatory or legal requirements? | None / Yes (PII/HIPAA/SOC2/etc.) / Not sure |
| 5 | Areas you already know are problematic? | None / Yes (describe) |
| 6 | Which scopes to audit? | All (default) / Security / AI / Tests / Code Quality / Decoupling |

Skipped scopes are marked N/A in the scorecard and excluded from the overall grade. If the user skips any question, assume worst-case: public, shared access, compliance required.

## Phase 0.5: Background Agent Launch

After Phase 0 calibration is complete, hand off the audit to a background agent:

**Step 1:** Create a start marker (run via Bash tool):
```bash
MARKER=/tmp/harden_audit_$(date +%s) && touch $MARKER && echo $MARKER
```
Note the printed marker path.

**Step 2:** Launch a background agent (Agent tool, `run_in_background: true`) with this prompt — fill in all bracketed values from Phase 0:

> You are running a /harden audit. Calibration is done — skip Phase 0 and 0.5.
>
> **Target:** [absolute path of directory being audited]
> **Calibration answers:**
> - Visibility: [answer]
> - Access: [answer]
> - Deployment: [answer]
> - Compliance: [answer]
> - Known issues: [answer]
> - Scopes selected: [answer]
> - Scrutiny level: [Light / Full / Strict]
>
> Follow all instructions in `~/.claude/skills/harden/SKILL.md` starting from **Severity Definitions** through **Batch Plan**. Write findings to `findings.json` in the audited project directory using the JSON format from `score_audit.py`.
>
> **Scope restriction:** Only write to `[OUTPUT_FILE]` in the audited project directory. Do not modify any other files — in particular, do not write to any MARVIN state files (current.md, goals.md, decisions.md, todos.md, habits.md, learning.md) or any file outside the audited project directory.
>
> **Final step (token capture + state) — run after writing findings.json:**
> ```bash
> uv run python ~/.claude/skills/harden/capture_tokens.py --project [project-name] --scope [scope] --marker [MARKER path from Step 1] --output-dir [absolute path of directory being audited]
> ```
> Then write the state file:
> ```python
> import json, sys
> sys.path.insert(0, 'skills/harden')
> from harden_state import build_initial_state, batches_from_findings, write_state
> from pathlib import Path
> findings = json.loads(Path('[OUTPUT_FILE]').read_text())
> state = build_initial_state(
>     project='[project-name]', target='[absolute path of directory being audited]',
>     repo='[owner/repo]', grade='[OVERALL_GRADE]', token_usage=[TOKEN_TOTAL],
>     findings_file='[OUTPUT_FILE]', batches=batches_from_findings(findings)
> )
> write_state(Path('[absolute path of directory being audited]/harden-state.json'), state)
> print('State written.')
> ```
>
> **Final step (write state file) — run after token capture:**
> ```python
> # Write harden-state.json alongside findings.json
> import json, sys
> sys.path.insert(0, 'skills/harden')
> from harden_state import build_initial_state, batches_from_findings, write_state
> from pathlib import Path
> findings = json.loads(Path('[OUTPUT_FILE]').read_text())
> state = build_initial_state(
>     project='[PROJECT]', target='[TARGET_DIR]', repo='[REPO]',
>     grade='[GRADE]', token_usage=[TOKEN_TOTAL],
>     findings_file='[OUTPUT_FILE]',
>     batches=batches_from_findings(findings)
> )
> write_state(Path('[TARGET_DIR]/harden-state.json'), state)
> print('State written to [TARGET_DIR]/harden-state.json')
> ```

**Step 3:** Tell the user: "Audit running in the background. You'll be notified when it's done. Findings will land in `findings.json`."

Do not proceed further — the background agent handles all scopes.

---

**File-read budget:** Before starting, estimate repo size (count files with Glob). For repos >50 files, cap reads at 20 files per scope. Exceed this only if a Critical finding warrants deeper exploration — state explicitly when you do.

**After calibration, state assumptions and set scrutiny level:**

| Context | Scrutiny Level |
|---------|---------------|
| Prototype / solo / private | **Light** — focus on Critical and High only. Skip Low findings. |
| Production / team / public | **Full** — all severities reported. |
| Compliance required | **Strict** — expand security and data scopes. Flag anything ambiguous. |

Tell the user what this audit covers and what it doesn't:
- "Covering: source code, config files, git history, dependencies, test coverage"
- "Not covering: infrastructure, CI/CD pipeline, database security, runtime monitoring"
- "Does this match your expectations, or should I adjust?"

## Severity Definitions

Every finding must use one of these levels. Definitions are anchored to real-world outcomes, not vibes.

| Level | Definition | Example |
|-------|-----------|---------|
| **Critical** | Concrete exploit path leading to data loss, security breach, or production outage. Must be demonstrable, not theoretical. | Hardcoded API key with write access in committed file |
| **High** | Significant risk with clear real-world impact. Should fix before shipping. | No input validation on user-provided file paths |
| **Medium** | Should be fixed but won't cause immediate harm. | Bare `except: pass` hiding errors in non-critical path |
| **Low** | Minor improvement. Style, consistency, or edge case unlikely to trigger. | Inconsistent naming between similar functions |

## Audit Scopes

Work through these one at a time. For each scope:

1. **Steel-man first** — Before listing findings, state why the current approach is reasonable. Acknowledge what the project does well in this area. If you skip this step, your findings will be noisy.
2. **Explore and find issues** — Read files, check configs, scan patterns.
3. **Self-check** — Run these 5 steps. Drop findings that don't survive.
   1. Drop any where real-world impact is negligible
   2. Every Critical/High must cite file + line — no citation means it's not a real finding
   3. No style flags — don't flag naming preferences or formatting choices
   4. Respect frameworks — don't flag X if the framework handles X
   5. Inversion pass — check for gaps your scope-by-scope scan may have missed
4. **Summarize** — Present findings, then ask if the user wants to go deeper or move on.

### 1. Security
- Input validation and output sanitization (including stderr/log leakage)
- Secrets in code, config, and git history (not just current files — check committed history)
- Permission and access control
- Dependency hygiene (pinning, unused deps expanding attack surface, known CVEs)
- File system access patterns (path traversal, unsafe reads/writes)

### 2. AI-Specific Gaps
- Prompt injection risks (user input flowing into prompts unsanitized)
- Data exposure through AI context (secrets, PII, or sensitive content visible to the model)
- Access control on AI interfaces (who can invoke the AI, rate limits, cost controls)
- Output validation (does the system verify AI outputs before acting on them?)
- Fragile model assumptions (hardcoded model names, unpinned versions, deterministic output expectations)
- AI-to-code offload opportunities (tasks done by multi-step AI reasoning that a script or cheaper model could handle)

For the full extended checklist (10 additional checks including tool use validation, context stuffing, agent permissions, cost control, and more), read [ai-audit-checklist.md](references/ai-audit-checklist.md) before evaluating this scope.

### 3. Test Coverage
- Map existing test coverage (what has tests, what doesn't)
- Flag high-risk untested code (touches files, network, secrets, user input, money)
- Verify security and AI findings from Scopes 1-2 have test coverage
- Identify missing error path tests (what happens when things fail?)
- Suggest highest-value tests to add first, prioritized by risk

### 4. Code Quality
- Linter and formatter configuration (is one configured? If not, recommend one for the language/framework)
- Error handling (silent failures, bare `except`, swallowed exceptions)
- Dead code and stale config (unused functions, abandoned imports, orphaned files from refactors)
- Edge cases (empty inputs, nulls, unexpected types, boundary values)
- Consistency (naming, patterns, structure across similar components)
- Network and retry behavior (connection limits, timeout handling, backoff)
- Hardcoded values that should be configurable (paths, filenames, magic numbers)

### 5. Decoupling & Data Separation
- Tightly coupled components that should be independent (shared state, circular dependencies, components modifying same files)
- Private or sensitive data committed to the repo (PII, personal content, customer data)
- `.gitignore` coverage for sensitive and generated files
- Environment-specific config committed as if universal
- Data that should live outside the repo (personal content, user-specific state, local config)
- Clear boundaries between framework code and user data

## Checkpoint Questions

During each scope, if you encounter something ambiguous — **ask before rating severity**. Only ask questions the codebase can't answer.

Examples:
- "This file has what looks like a real SSN — is this test data or production?"
- "This API key is in a committed file — is this a throwaway/dev key or production?"
- "Two skills modify the same file — is this intentional or a gap?"

**If the codebase can answer it, don't ask. If only the user knows, ask.**

Do NOT turn the audit into an interview. The skill's strength is autonomous exploration. Reserve questions for decisions that change severity or skip/prioritize a finding.

## Finding Format

Every finding must include all of these. If you can't fill them all in, the finding isn't real — drop it.

```
### [Scope]-[Number]: [Title]
**Severity:** Critical | High | Medium | Low
**Blocking:** Yes | No
**Where:** file/path.py:42
**What:** [The specific issue]
**Proof:** [What you observed in the code that triggered this]
**Impact:** [What actually happens if ignored]
**Surfaced by:** [Code reading | Pre-mortem | Inversion | Five whys | Blind spots]
**Fix:** [Concrete suggested fix]
```

**Blocking** = must address before shipping. **Non-blocking** = fix when convenient.
**Surfaced by** = Code reading | Pre-mortem | Inversion | Five whys | Steel-manning | Blind spots

## Scorecard

After completing all scopes, present a scorecard.

> Run `uv run python skills/harden/validate_findings.py findings.json && uv run python skills/harden/score_audit.py findings.json` to validate then auto-generate this scorecard. `score_audit.py` is the source of truth for the grading formula — see its module docstring for point values, grade thresholds, and the critical-floor rule.

**Scorecard format:** Columns: Scope | Grade | Blocking | Non-blocking. One row per scope, then Overall grade. Mark skipped scopes as **N/A — not in scope** and omit them from the grade columns.

**Overall grade:** Average of scope grades (A=4, B=3, C=2, D=1, F=0), rounded. Exclude N/A scopes from the average.

## Verdict

Based on blocking findings, give one clear recommendation:

- **Ship it** — No blocking findings. Non-blocking items are nice-to-haves.
- **Ship with changes** — N blocking findings need fixing first. See batch plan.
- **Rethink this** — Fundamental architectural issues that need redesign before individual fixes make sense.

## Batch Plan

After the verdict, generate the batch plan using `batch_plan.py`:

```bash
uv run python skills/harden/batch_plan.py findings.json
```

This deterministically groups findings: blocking findings in Batch 1, non-blocking grouped by scope in severity order. To write batch numbers back to `findings.json`, add `--assign`.

**Batch format (for reference):**

```
### Batch 1 — [description] ([count] issues)
Resolves: [finding numbers]
Blocking: [Yes — must fix before shipping / No — quality improvement]
Dependency: [what must be done first, or "None — do this first"]
Effort: [Low / Medium / High]
```

After presenting the batch plan, ask: **"Ready to create GitHub issues? I'll file them in batch order."**

Only create issues after the user reviews and approves the batches. Once approved, run:

```bash
uv run python skills/harden/harden-issues.py findings.json --repo <owner>/<repo> --batch 1 --create-pr
```

To preview without filing: add `--dry-run`.

## On Notification

When the background agent task notification arrives, do the following before responding to the user:

**Step 1:** Read `harden-state.json` from the audited project directory:
```python
import json
from pathlib import Path
state = json.loads(Path('[TARGET_DIR]/harden-state.json').read_text())
```

**Step 2:** Render a findings summary table derived from the state file. Each row corresponds to one batch. Derive blocking / non-blocking counts from `findings.json` if needed.

**Step 3:** Present the notification summary and action menu:

```
Audit complete — Grade: [grade] | [total findings] findings | [token_usage] tokens

| Batch | Description       | Status  | Issues |
|-------|-------------------|---------|--------|
| 1     | [description]     | pending | N      |
| 2     | [description]     | pending | N      |
...

[1] File Batch 1 (N issues) — uv run python skills/harden/harden-issues.py findings.json --repo <repo> --batch 1 --create-pr
[2] File all batches now
[3] Skip — I'll come back later (/harden resume <path> to return)
```

**Step 4:** Execute the chosen action:
- **[1]** — run `harden-issues.py --batch 1 --create-pr` for the selected batch
- **[2]** — run `harden-issues.py` without `--batch` to file all batches, then `--create-pr` per batch
- **[3]** — acknowledge and remind user they can resume with `/harden resume [TARGET_DIR]`

Use the `repo` field from `harden-state.json` if available; otherwise prompt the user for `--repo owner/repo`.

## Phase 7: Resume

**Trigger:** Arguments start with `resume` (e.g. `/harden resume skills/harden` or `/harden resume --state /path/to/project/harden-state.json`).

**Purpose:** Pick up a completed audit and file remaining batches without re-running the audit.

**Usage:**
```
/harden resume <project-directory>
/harden resume --state <path-to-harden-state.json>
```

**Steps:**

1. Locate `harden-state.json`:
   - If `--state <path>` is given, use that path directly.
   - Otherwise look for `<project-directory>/harden-state.json`.
   - If not found, tell the user: "No harden-state.json found at `<path>`. Run `/harden <project>` first to generate one."

2. Read the state file and display the batch status table:

```
Project: [project]  Repo: [repo]  Grade: [grade]  Date: [date]  Tokens: [token_usage]

| Batch | Description       | Status  | Issues filed |
|-------|-------------------|---------|--------------|
| 1     | [description]     | filed   | 3            |
| 2     | [description]     | pending | 0            |
...
```

3. Present the action menu (same as the notification handler, filtered to pending batches):

```
[1] File Batch 2 (N issues)
[2] File all pending batches now
[3] Skip — come back later
```

4. Execute the chosen action using `harden-issues.py` with the batch number and `--create-pr`. Use the `repo` field from `harden-state.json`; prompt if missing.

## Rules

**Hard rules — no exceptions:**
- **Phase gate reference files.** `ai-audit-checklist.md` loads at Scope 2, not before. `engineering-blind-spots.md` loads only if fewer than 2 findings per scope. No reference file loads before its gate.
- **Steel-man every scope.** Before listing findings, state what the project does well. If you skip this, your findings are noise.
- **"So what?" test.** For every finding, ask: "If they ignore this, what actually happens?" If the answer is "nothing much," drop it.
- **Findings cap: 5 per scope, 15 total.** If you found more, keep only the highest severity. This forces prioritization.
- **Actionable only.** No finding without a concrete fix. If you can't say what to do about it, don't raise it.
- **Evidence required.** Every finding must cite a file path and line. No finding based on "I didn't see X" without checking.
- **Respect frameworks.** If the framework handles it (Django CSRF, React XSS escaping, etc.), don't flag it as missing unless the project bypasses the protection.
- **No style opinions.** Don't flag naming preferences, formatting choices, or "I would have done it differently."

## Scripts

| Script | Purpose | Usage |
|--------|---------|-------|
| `validate_findings.py` | Validate all required fields before scoring | `uv run python skills/harden/validate_findings.py findings.json` |
| `score_audit.py` | Compute per-scope grades and overall scorecard | `uv run python skills/harden/score_audit.py findings.json` |
| `batch_plan.py` | Deterministically assign findings to batches | `uv run python skills/harden/batch_plan.py findings.json [--assign]` |
| `harden-issues.py` | File GitHub issues and create PR with auto-close links | `uv run python skills/harden/harden-issues.py findings.json --repo owner/repo --batch 1 --create-pr` |
| `capture_tokens.py` | Read agent JSONL to log token usage automatically | `uv run python ~/.claude/skills/harden/capture_tokens.py --project <name> --scope All --marker /tmp/harden_audit_<ts> --output-dir <audited-project-dir>` |
| `token_log.py` | Manually log token usage (fallback if capture_tokens.py fails) | `uv run python skills/harden/token_log.py --project <name> --scope <scope> --input-tokens <N> --output-tokens <N> --output-dir <audited-project-dir>` |

**Prerequisites for harden-issues.py:** `gh` CLI authenticated; labels `harden`, `blocking`, `Critical`, `High`, `Medium`, `Low` must exist in the target repo.

**Token logging:** The background agent runs `capture_tokens.py` automatically at the end of every audit. Token counts are read from the agent's Claude Code session JSONL and written to `harden_{date}_token_usage.csv` in the audited project directory (gitignored, stays local). Use `token_log.py` only if automatic capture fails.

**Browsing usage:** Use `npx ccusage daily --breakdown` to view token spend by project/model/time period across all Claude Code sessions. Complements `token_usage.csv` (which tracks per-audit scope breakdowns).

## Rules

**Standard rules:**
- Explore the codebase yourself before asking questions. Read files, check configs, scan for patterns.
- Only flag real issues you find in the code — not theoretical risks.
- Prioritize findings by severity: critical > high > medium > low, calibrated by Phase 0 context.
- The scorecard, verdict, and batch plan are mandatory outputs. Do not skip them.

**Performed vs. Genuine Thoroughness** — gut-check your findings across all scopes before presenting:

| Fake Thoroughness | Genuine Thoroughness |
|---|---|
| Long list of "considerations" with no concrete code reference | Each finding cites a specific file and line |
| Generic warnings that apply to any project | Findings specific to THIS project's architecture |
| "Could potentially" language without evidence | "This code does X, which means Y" |
| Flagging missing features the project doesn't need | Flagging gaps in features the project actually uses |
| Every finding sounds equally important | Clear severity gradient with most findings at Medium/Low |
