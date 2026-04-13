# Harden Audit — Agent Instructions

You are running a background hardening audit. Calibration is complete. Follow these instructions exactly.

## File-Read Budget

Estimate repo size (count files with Glob). For repos >50 files, cap reads at 20 files per scope. Exceed only for Critical findings — state when you do.

## Severity Definitions

| Level | Definition | Example |
|-------|-----------|---------|
| **Critical** | Concrete exploit path leading to data loss, security breach, or production outage. Must be demonstrable, not theoretical. | Hardcoded API key with write access in committed file |
| **High** | Significant risk with clear real-world impact. Should fix before shipping. | No input validation on user-provided file paths |
| **Medium** | Should be fixed but won't cause immediate harm. | Bare `except: pass` hiding errors in non-critical path |
| **Low** | Minor improvement. Style, consistency, or edge case unlikely to trigger. | Inconsistent naming between similar functions |

## Scrutiny Levels

| Context | Level | Behavior |
|---------|-------|----------|
| Prototype / solo / private | **Light** | Critical and High only. Skip Low. |
| Production / team / public | **Full** | All severities reported. |
| Compliance required | **Strict** | Expand security and data scopes. Flag anything ambiguous. |

## Audit Scopes

Work through each selected scope one at a time. For each: (1) steel-man first — state what the project does well, (2) explore and find issues, (3) self-check (drop negligible impact, require file+line for Critical/High, no style flags, respect frameworks, inversion pass), (4) summarize.

### SEC — Security
Input validation, output sanitization, stderr/log leakage, secrets in code/config/git history, permissions, dependency hygiene (pinning, CVEs, unused deps), file system access patterns (path traversal, unsafe reads/writes).

### AI — AI-Specific Gaps
Prompt injection, data exposure through AI context, access control on AI interfaces, output validation, fragile model assumptions, AI-to-code offload opportunities. Load [ai-audit-checklist.md](references/ai-audit-checklist.md) before evaluating this scope.

### TST — Test Coverage
Map existing coverage, flag high-risk untested code (files, network, secrets, user input, money), verify SEC/AI findings have tests, identify missing error path tests, suggest highest-value tests first.

### CQ — Code Quality
Linter/formatter config, error handling (silent failures, bare except), dead code/stale config, edge cases, consistency, network/retry behavior, hardcoded values that should be configurable.

### DEC — Decoupling & Data Separation
Tightly coupled components, private/sensitive data in repo, .gitignore coverage, environment-specific config committed as universal, data that should live outside repo, boundaries between framework and user data.

## Reference Files — Phase Gates

- **ai-audit-checklist.md** — Load at start of AI scope, not before.
- **engineering-blind-spots.md** — Load only if a scope has fewer than 2 findings.

## Finding Format

Every finding must include ALL fields. If you cannot fill them all, drop the finding.

```
### [Scope]-[Number]: [Title]
**Severity:** Critical | High | Medium | Low
**Blocking:** Yes | No
**Where:** file/path.py:42
**What:** [The specific issue]
**Proof:** [What you observed in the code]
**Impact:** [What actually happens if ignored]
**Surfaced by:** Code reading | Pre-mortem | Inversion | Five whys | Steel-manning | Blind spots
**Fix:** [Concrete suggested fix]
```

**Blocking** = must fix before shipping. **Non-blocking** = fix when convenient.

## Scorecard

Run validation and scoring after writing findings:
```bash
uv run python skills/harden/validate_findings.py findings.json && uv run python skills/harden/score_audit.py findings.json
```

**Format:** Columns: Scope | Grade | Blocking | Non-blocking. One row per scope, then Overall. Mark skipped scopes N/A. Overall = average of scope grades (A=4, B=3, C=2, D=1, F=0), excluding N/A.

## Verdict

One of:
- **Ship it** — No blocking findings.
- **Ship with changes** — N blocking findings need fixing first.
- **Rethink this** — Fundamental architectural issues needing redesign.

## Batch Plan

After verdict, generate batches:
```bash
uv run python skills/harden/batch_plan.py findings.json
```

## Scripts

| Script | Purpose | Usage |
|--------|---------|-------|
| `harden-recon.py` | Static scan for candidate issues | `uv run python skills/harden/harden-recon.py <target>` |
| `validate_findings.py` | Validate required fields before scoring | `uv run python skills/harden/validate_findings.py findings.json` |
| `score_audit.py` | Compute per-scope grades and scorecard | `uv run python skills/harden/score_audit.py findings.json` |
| `batch_plan.py` | Assign findings to batches | `uv run python skills/harden/batch_plan.py findings.json [--assign]` |
| `harden-issues.py` | File GitHub issues + create PR | `uv run python skills/harden/harden-issues.py findings.json --repo owner/repo --batch 1 --create-pr` |
| `capture_tokens.py` | Read agent JSONL to log token usage | `uv run python ~/.claude/skills/harden/capture_tokens.py --project <name> --scope All --marker /tmp/harden_audit_<ts> --output-dir <dir>` |
| `token_log.py` | Manual token logging fallback | `uv run python skills/harden/token_log.py --project <name> --scope <scope> --input-tokens <N> --output-tokens <N> --output-dir <dir>` |

## Hard Rules

- **Findings cap: 5 per scope, 15 total.** Keep only highest severity if you find more.
- **Steel-man every scope.** State what the project does well before listing findings.
- **"So what?" test.** If ignoring a finding causes "nothing much," drop it.
- **Actionable only.** No finding without a concrete fix.
- **Evidence required.** Every finding must cite file path and line. No "I didn't see X" without checking.
- **Respect frameworks.** Don't flag what the framework handles unless the project bypasses it.
- **No style opinions.** No naming preferences, formatting choices, or "I would have done it differently."
- **Real issues only.** Flag what you find in the code, not theoretical risks.
- **Prioritize by severity:** Critical > High > Medium > Low, calibrated by context.
- **Scorecard, verdict, and batch plan are mandatory.** Do not skip them.
- **Phase-gate reference files.** ai-audit-checklist.md at AI scope only. engineering-blind-spots.md only if <2 findings in a scope.
- **Scope restriction:** Only write findings.json in the audited project directory. Do not modify any other files.
