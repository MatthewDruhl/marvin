---
description: Audit a software project for hardening — security, AI gaps, test coverage, code quality, and decoupling. Use when user wants to harden a project, audit for vulnerabilities, check test coverage, or separate private data from code.
---

Perform a systematic hardening audit of this project. Work through each phase below, exploring the codebase to find real issues — not hypothetical ones.

## Reference Files

Load these as needed during the audit — do not read all upfront.

- [ai-audit-checklist.md](references/ai-audit-checklist.md) — Extended AI checks (read before Scope 2)
- [questioning-frameworks.md](references/questioning-frameworks.md) — Self-check frameworks (read after each scope)
- [engineering-blind-spots.md](references/engineering-blind-spots.md) — Detection questions by scope (read if a scope feels thin)

## Phase 0: Context Gathering

Before scanning, ask these questions to calibrate the audit. The user can answer inline or say "skip" to assume worst-case (strictest ratings).

1. **Visibility** — Is this repo private, or could it go public?
2. **Access** — Just you, a team, or open source?
3. **Deployment** — Local only, server, or cloud?
4. **Compliance** — Any regulatory or legal requirements? (government forms, PII rules, HIPAA, etc.)
5. **Known issues** — Areas you already know are problematic? (prioritize or skip)

If the user skips, assume: public visibility, shared access, compliance required.

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
3. **Self-check** — Read [questioning-frameworks.md](references/questioning-frameworks.md) and run the 5-step self-check. Drop findings that don't survive the "so what?" test.
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
**Fix:** [Concrete suggested fix]
```

**Blocking** = must address before shipping. **Non-blocking** = fix when convenient.

## Scorecard

After completing all scopes, present a scorecard.

**Grading formula:**
- Points per finding: Critical = 4, High = 3, Medium = 2, Low = 1
- **Any critical finding in a scope = D minimum (cannot grade above D until resolved)**

| Grade | Points |
|-------|--------|
| A | 0 |
| B | 1-4 |
| C | 5-9 |
| D | 10-14 |
| F | 15+ |

**Scorecard format:**

```
| Scope | Grade | Blocking | Non-blocking |
|-------|-------|----------|--------------|
| Security | C | 1 critical, 1 high | 1 medium |
| AI | B | — | 2 high |
| Tests | D | 3 high | — |
| Code Quality | B | — | 1 medium, 2 low |
| Decoupling | C | 1 high | 1 high |

Overall: C
```

**Overall grade:** Average of scope grades (A=4, B=3, C=2, D=1, F=0), rounded.

## Verdict

Based on blocking findings, give one clear recommendation:

- **Ship it** — No blocking findings. Non-blocking items are nice-to-haves.
- **Ship with changes** — N blocking findings need fixing first. See batch plan.
- **Rethink this** — Fundamental architectural issues that need redesign before individual fixes make sense.

## Batch Plan

After the verdict, propose batches for fixing the findings.

**Batching rules:**
1. **Blocking findings go in Batch 1** — always
2. **Dependencies first** — if finding X blocks finding Y, X goes in an earlier batch
3. **Logical grouping** — findings that touch the same files or fix related problems go together
4. **Non-blocking findings in later batches** — ordered by severity

**Batch format:**

```
### Batch 1 — [description] ([count] issues)
Resolves: [finding numbers]
Blocking: [Yes — must fix before shipping / No — quality improvement]
Dependency: [what must be done first, or "None — do this first"]
Effort: [Low / Medium / High]
```

After presenting the batch plan, ask: **"Ready to create GitHub issues? I'll file them in batch order."**

Only create issues after the user reviews and approves the batches.

## Rules

**Hard rules — no exceptions:**
- **Steel-man every scope.** Before listing findings, state what the project does well. If you skip this, your findings are noise.
- **"So what?" test.** For every finding, ask: "If they ignore this, what actually happens?" If the answer is "nothing much," drop it.
- **Findings cap: 5 per scope, 15 total.** If you found more, keep only the highest severity. This forces prioritization.
- **Actionable only.** No finding without a concrete fix. If you can't say what to do about it, don't raise it.
- **Evidence required.** Every finding must cite a file path and line. No finding based on "I didn't see X" without checking.
- **Respect frameworks.** If the framework handles it (Django CSRF, React XSS escaping, etc.), don't flag it as missing unless the project bypasses the protection.
- **No style opinions.** Don't flag naming preferences, formatting choices, or "I would have done it differently."

**Standard rules:**
- Explore the codebase yourself before asking questions. Read files, check configs, scan for patterns.
- Only flag real issues you find in the code — not theoretical risks.
- Prioritize findings by severity: critical > high > medium > low, calibrated by Phase 0 context.
- The scorecard, verdict, and batch plan are mandatory outputs. Do not skip them.
