# Questioning Frameworks

Use these frameworks during the self-check pass after each scope. They help catch false positives, missing findings, and severity miscalibration.

## Pre-Mortem

**Prompt:** "This project shipped. It failed catastrophically. What went wrong?"

Walk through a realistic failure narrative. If you can't construct one from your findings, your Critical/High findings may be inflated. If you can construct one that your findings DON'T cover, you may have missed something.

## Inversion

**Prompt:** "What would guarantee this project fails? Are any of those conditions present?"

Flip the question. Instead of looking for problems, define what failure looks like and check if those conditions exist in the code. This catches systemic issues that individual scope checks miss.

## Five Whys (Reverse)

**Prompt:** For each finding, ask "Why does this matter?" five times.

If you can't get past 2-3 "whys" before the answer becomes "it doesn't really matter," the finding is Low severity at best. Drop it if it doesn't survive 3 whys.

## Steel-Manning

**Prompt:** "What is the strongest argument that this code is correct as-is?"

Before flagging something, articulate why the current approach might be intentional and reasonable. Common reasons:
- Framework handles it (e.g., Django CSRF, React XSS escaping)
- Scope is intentionally limited (prototype, internal tool)
- Trade-off was made deliberately (performance vs safety)
- The "problem" is actually standard practice for the ecosystem

If the steel-man holds, don't flag it. If it partially holds, reduce severity.

## The "So What?" Test

**Prompt:** "If they ignore this finding, what actually happens?"

| Answer | Action |
|--------|--------|
| "Data loss, security breach, or outage" | Keep — Critical or High |
| "Bug in production, degraded experience" | Keep — Medium |
| "Slightly worse code, minor inconsistency" | Demote to Low or drop |
| "Nothing, really" | Drop it |

## Self-Check Process (5 Steps)

Run this after generating findings for each scope:

1. **Review findings** — Drop any where real-world impact is negligible
2. **Verify evidence** — Every Critical/High finding must cite file + line. If you can't point to specific code, it's not a real finding.
3. **No style flags** — Don't flag naming preferences, formatting choices, or "I would have done it differently" as findings
4. **Respect frameworks** — If a framework handles X (CSRF, XSS, SQL injection), don't flag X as missing unless the project bypasses the framework's protection
5. **Inversion pass** — Run the inversion framework once to check for gaps your scope-by-scope scan may have missed

## Performed vs Genuine Thoroughness

Use this table to gut-check your findings across ALL scopes, not just AI. A long list of "considerations" with no concrete code impact is fake thoroughness.

| Fake Thoroughness | Genuine Thoroughness |
|---|---|
| Long list of "considerations" with no concrete code reference | Each finding cites a specific file and line |
| Generic warnings that apply to any project | Findings specific to THIS project's architecture |
| "Could potentially" language without evidence | "This code does X, which means Y" |
| Flagging missing features the project doesn't need | Flagging gaps in features the project actually uses |
| Every finding sounds equally important | Clear severity gradient with most findings at Medium/Low |

## Framework Attribution

Each finding should note which reasoning framework surfaced it. This prevents "gut feeling" findings and ensures the self-check frameworks are actually being used.

Valid attributions:
- **Code reading** — Found by directly reading the source code
- **Pre-mortem** — Surfaced by imagining a catastrophic failure
- **Inversion** — Surfaced by asking "what would guarantee failure?"
- **Five whys** — Severity validated by tracing impact chain
- **Steel-manning** — Survived the "strongest argument this is correct" test
- **Blind spots** — Triggered by a detection question from `engineering-blind-spots.md`

If you can't attribute a finding to a specific framework or code observation, it's likely a generic concern rather than a real finding. Drop it.

---

*Steel-manning, "So What?" test, self-check process, and "Performed vs Genuine Thoroughness" table inspired by the [devils-advocate skill](https://github.com/notmanas/claude-code-skills/tree/main/skills/devils-advocate) by notmanas.*
