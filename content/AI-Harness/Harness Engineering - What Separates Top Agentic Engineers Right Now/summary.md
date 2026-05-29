# Harness Engineering: What Separates Top Agentic Engineers Right Now

**Source:** https://www.youtube.com/watch?v=ulNsa0sD8N0
**Creator:** Cole (The Algorithm / Archon)
**Length:** ~15 minutes
**Date transcribed:** 2026-05-27

---

## Core Concept

Harness engineering = building the wrapper around the model. It's the next evolution of context engineering (2025's buzzword). An agent is the LLM + the harness around it that provides context and defines processes.

## Two Layers of Harness

1. **The tool layer** (not yours to build): The coding agent you choose (Claude Code, Codex, etc.) is itself a harness. It gives the LLM file system access, command execution, and a system prompt. You pick this layer by choosing your tool.

2. **The AI layer** (yours to build): The wrapper you define on top. Six components:
   - Global rules (constraints, conventions, patterns)
   - Skills (workflow definitions: plan, implement, validate)
   - MCP servers (capabilities)
   - Codebase searching (LSP, knowledge graphs)
   - Hooks (security, validation, linting)
   - Sub-agents

## Key Insight: The Mindset Shift

The real difference between harness engineering and context engineering isn't technical. It's a reframe: **every mistake becomes a rule.** Instead of blaming the model and waiting for the next version, you improve your harness. Add a hook to block destructive commands. Update a skill to prevent the same process error. Evolve the system over time.

The author calls this "system evolution": taking ownership of the AI layer you control, feeding mistakes forward into better rules, hooks, and skills.

## Practical Recommendations

- **Separate plan, implement, and validate into different coding agent sessions.** Each session stays token-efficient and focused. Use markdown artifacts as handoffs between sessions.
- **Hooks are underused.** Three high-value hook patterns:
  - Pre-tool security hooks (block reading sensitive files, destructive commands)
  - Stop-validation hooks (force tests/lint/type-check to pass before the agent can declare "done")
  - Post-edit lint hooks (keep codebase clean, which improves future agent reliability)
- **Don't hand a massive PRD to a single session.** The LLM will be overwhelmed regardless of how good your AI layer is.

## RALF Loop (Orchestration Pattern)

The "peak evolution" of harness engineering: automating multi-session workflows.

- A script (Python/bash) takes a large scope of work (PRD)
- Splits it into individual tasks
- Runs coding agent sessions one at a time, with handoff artifacts
- Can run parallel review agents (security, correctness, simplicity)
- Loop exits only when a done indicator is produced and all validation passes

Creator: Jeffrey Huntley. One of the first examples of automating multi-session orchestration.

## Relevance to MARVIN

This maps directly to how Matt already works:
- `CLAUDE.md` = global rules
- `/skills/*.md` = skills
- `.claude/hooks/` = hooks
- Background agents with worktrees = multi-session orchestration
- The "every mistake becomes a rule" mindset = what the feedback memory system does

The gap: Matt doesn't have an automated RALF-style loop yet. The plan/implement/validate cycle is manual. Could be worth exploring for larger features.

---

*Companion repo mentioned in video (Archon): open-source harness builder for custom agentic engineering workflows.*
