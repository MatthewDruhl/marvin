# Questioning Frameworks — Attribution Reference

The self-check steps and reasoning frameworks are defined inline in SKILL.md.

This file exists as a reference for valid `Surfaced by` attributions in the finding format.

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
