<!-- PHASE GATE: Do not read if 2 or more findings already identified. Load only when finding count is low. -->

# Engineering Blind Spots

Detection questions organized by scope. Use these to probe for issues your initial scan may have missed. These are prompts for investigation, not a checklist of things to flag.

## Security Blind Spots

- **Transitive trust:** Does the app trust data from a source that trusts user input? (e.g., trusting a database value that was populated from unsanitized user input)
- **Error message leakage:** Do error messages reveal internal paths, stack traces, or config values?
- **Default credentials:** Are there any default passwords, API keys, or tokens that ship with the code?
- **Time-of-check vs time-of-use:** Is there a gap between validating a permission and acting on it?
- **Logging sensitive data:** Do logs capture passwords, tokens, PII, or request bodies?

## AI Blind Spots

- **Model as oracle:** Does the code treat AI output as always correct? Where are the sanity checks?
- **Prompt as security boundary:** Is the system prompt relied on to enforce access control? (It can't.)
- **Context accumulation:** Does long-running context accumulate sensitive data that shouldn't persist?
- **Fallback behavior:** What happens when the AI API is down, slow, or returns garbage?
- **Version coupling:** Will a model upgrade break the system? Are prompts fragile to model behavior changes?

## Test Blind Spots

- **Happy path only:** Do tests only verify the success case? What about malformed input, timeouts, partial failures?
- **Mock divergence:** Do mocks reflect actual API behavior, or have they drifted?
- **Missing integration tests:** Are units tested but the integration between them untested?
- **Flaky tests ignored:** Are there tests that sometimes fail and are ignored or retried?
- **Test data as production proxy:** Does test data represent realistic edge cases, or just the obvious scenarios?

## Code Quality Blind Spots

- **Silent failures:** Does the code catch exceptions and do nothing? (`except: pass`)
- **Implicit ordering:** Does correctness depend on functions being called in a specific order with no enforcement?
- **Magic values:** Are there numbers, strings, or thresholds with no explanation?
- **Copy-paste drift:** Are there near-duplicate code blocks that have diverged slightly?
- **Resource leaks:** Are file handles, connections, or locks always released, even on error paths?

## Decoupling Blind Spots

- **Shared mutable state:** Do multiple components read/write the same file or global variable?
- **Hardcoded paths:** Are file paths, URLs, or service addresses baked into the code?
- **Config in code:** Are environment-specific values (dev/staging/prod) in source files instead of config?
- **Circular dependencies:** Do modules import each other? Does changing A require changing B?
- **Mixed concerns:** Does a single file handle business logic, I/O, and presentation?

---

*Detection question pattern inspired by the [devils-advocate skill](https://github.com/notmanas/claude-code-skills/tree/main/skills/devils-advocate) by notmanas.*
