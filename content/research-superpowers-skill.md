Agent "Research Superpowers skill for MARVIN" completed

⏺ Here's the Superpowers breakdown:

  ---
  What's Worth Borrowing

  1. Hard gate before code starts — Superpowers explicitly forbids writing code until the user approves a committed design doc. MARVIN's write-a-prd and
  grill-me don't enforce this. For agentic/background work, this would prevent runaway sessions that build the wrong thing.

  2. Systematic debugging skill — 4 phases: reproduce → compare working vs. broken → single-variable hypothesis testing → test-first fix. Three named
  techniques: root-cause-tracing, defense-in-depth, condition-based-waiting. MARVIN has nothing like this — it's a clean add.

  3. Stop-on-blocker discipline — executing-plans has explicit halt conditions: missing dependency, unclear instruction, repeated verification failure.
  Never guesses. Worth adding to how MARVIN instructs background agents.

  4. Two-stage review per task — Spec compliance check first, code quality second, before moving to the next task. No MARVIN equivalent.

  5. Committed plan artifacts — Saves specs + plans as files before execution starts (docs/superpowers/specs/, docs/superpowers/plans/). A content/specs/
  convention in MARVIN would make agentic sessions more reviewable.

  ---
  Already Covered by MARVIN

  - Session flow + state tracking (MARVIN does this better)
  - TDD (tdd skill)
  - PRD / brainstorming (write-a-prd + grill-me)
  - Git workflow hard rules (CLAUDE.md)
  - Background agents + skill authoring

  ---
  My Recommendation

  Don't install Superpowers as-is — it would conflict with MARVIN's existing session flow. Instead, cherry-pick three things:

  1. New debug skill — port the systematic-debugging 4-phase approach directly
  2. Stop-on-blocker rules — add to CLAUDE.md or background agent instructions
  3. Hard design gate — add a "no code before approval" step to write-a-prd or a new plan skill with a committed spec output

  Want me to start on any of those?

❯ breakdown each recommendation: detail:pros:cons

⏺ 1. New debug Skill — Port Systematic Debugging

  What it is: A skills/debug/SKILL.md with a 4-phase methodology:
  1. Reproduce & trace backward (never guess before reproducing)
  2. Compare working vs. broken state
  3. Single-variable hypothesis testing
  4. Test-first fix

  Pros:
  - Clean, self-contained — no conflict with anything existing
  - Fills a real gap; debugging is the most common unstructured activity in Claude sessions
  - The named techniques (root-cause-tracing, defense-in-depth, condition-based-waiting) give Claude a shared vocabulary to reference mid-session
  - Low maintenance — skill doesn't need updates as MARVIN evolves
  - Directly supports your job search: debugging discipline is a demonstrable, interviewable skill

  Cons:
  - You have to remember to invoke /debug — Claude won't auto-detect that you're debugging unless you trigger it
  - If you're already mid-debug when you invoke it, the "reproduce first" gate creates friction
  - Some of it overlaps with what a good engineer does anyway; may not change behavior much in practice

  ---
  2. Stop-on-Blocker Rules — Add to CLAUDE.md or Agent Instructions

  What it is: Explicit halt conditions for agentic/background work: stop immediately on missing dependency, unclear instruction, or repeated verification
  failure. Never guess. Surface the blocker and wait.

  Pros:
  - Highest ROI of the three — prevents the most painful failure mode (agent runs for 10 minutes in the wrong direction)
  - No new files needed; just a few lines added to CLAUDE.md or to the background agent prompt template in relevant skills
  - Applies retroactively to all existing skills that spawn agents
  - Easy to verify: you'll notice immediately when it works

  Cons:
  - Too aggressive a threshold and Claude stops constantly for trivial things — requires tuning
  - "Unclear instruction" is subjective; Claude may interpret it too broadly or too narrowly
  - Adds friction to simple tasks where you'd rather it just make a reasonable call
  - Doesn't help in foreground (interactive) sessions where you're already present to course-correct

  ---
  3. Hard Design Gate — No Code Before Approval

  What it is: A mandatory user-approval checkpoint in write-a-prd or a new plan skill: Claude must produce a committed spec document and get explicit
  approval before any code is written or files are changed.

  Pros:
  - Highest quality impact for complex multi-step features — catches wrong-direction work before it starts
  - Committed spec in content/specs/ becomes a permanent artifact (reviewable, referenceable in PRs)
  - Directly mirrors how real teams work; good habit to reinforce while job searching
  - Forces Claude to surface assumptions and trade-offs upfront instead of mid-implementation

  Cons:
  - Most disruptive to add — requires restructuring write-a-prd or building a new skill from scratch
  - Heavy overhead for small tasks; you don't want a formal spec before fixing a typo
  - Gate enforcement is still instruction-based, not technical — Claude can still be prompted past it
  - Risk of spec-theater: writing a doc that gets approved but doesn't actually constrain what gets built
  - MARVIN sessions are already structured; adding another gate may make the flow feel bureaucratic

  ---
  Ranking by ROI

  ┌─────┬───────────────────────┬────────┬────────┬────────┐
  │  #  │    Recommendation     │ Effort │ Impact │  Risk  │
  ├─────┼───────────────────────┼────────┼────────┼────────┤
  │ 2   │ Stop-on-blocker rules │ Low    │ High   │ Low    │
  ├─────┼───────────────────────┼────────┼────────┼────────┤
  │ 1   │ Debug skill           │ Low    │ Medium │ None   │
  ├─────┼───────────────────────┼────────┼────────┼────────┤
  │ 3   │ Hard design gate      │ High   │ High   │ Medium │
  └─────┴───────────────────────┴────────┴────────┴────────┘

  Stop-on-blocker is the obvious first move. Debug skill is a quick win with no downside. Design gate is worth doing eventually but only if you find
  yourself building the wrong thing repeatedly.
