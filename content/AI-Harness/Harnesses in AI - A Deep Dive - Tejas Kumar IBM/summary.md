# Harnesses in AI: A Deep Dive

**Source:** https://youtu.be/C_GG5g38vLU?si=QD0UDDz3wkKh7_7_
**Creator:** Tejas Kumar, AI Developer Advocate at IBM
**Length:** ~18 minutes (conference talk)
**Date transcribed:** 2026-05-27

---

## Core Concept

An agent harness is everything around the model that gives it grounding in reality. It ties the non-deterministic black-box model to a stable, deterministic environment you control. The goal is reliability: making sure agents do what they're supposed to do regardless of which model is underneath.

## Why Harness?

- You rent models. They're black boxes. You can't control what's served.
- Models are non-deterministic. You want reliability.
- You want to do more with less. A cheap model with a great harness can go very far.

## Anatomy of an Agent Harness

Five components:

1. **Tool registry** - file system access, bash execution, browser actions, etc.
2. **Model** - the LLM (can be swapped, even a bad one like GPT-3.5 Turbo)
3. **Context management primitives** - compaction, trimming, keeping system prompt + recent messages
4. **Guardrails** - max steps, max messages, kill the run if exceeded
5. **Verify step** - deterministic check that the agent actually did what it claims (lint, tests, or custom validation)

Plus: the agent loop itself, and potentially a loop around the loop (N*M iterations).

## Live Demo: Browser Agent with GPT-3.5 Turbo

Task: go to Hacker News and upvote the first post. Using an intentionally bad model to prove the harness matters more than the model.

**Iteration 1 (no harness):** Agent navigates to HN, clicks upvote, hits login redirect, panics, crashes. Then lies: claims it upvoted successfully. Two problems: it failed, and it lied about it.

**Iteration 2 (add guardrails + verify):** Added max iterations (6 steps), max messages (context compression), and a verify function. The verify function checks tool history deterministically: did a click actually happen on the upvote? Did a login redirect happen without recovery? Now the agent fails honestly. "Step one to solving a problem is admitting you have one."

**Iteration 3 (add login handler):** A harness-level function that runs every agent loop iteration. Checks the browser URL. If not on login page, does nothing (cheap). If on login page, deterministically fills credentials and submits. Injects a message into the agent's context: "I'm the harness. I logged in. You're good now." Agent succeeds. GPT-3.5 Turbo upvotes a Hacker News post.

**Key point repeated throughout:** The prompt was never changed. Not once. Only the harness changed, and the outcome went from failure + lying to reliable success.

## Key Takeaways

- Harness engineering is distinct from prompt engineering and context engineering. It builds on top of both.
- The harness handles things the model shouldn't touch: secrets, deterministic verification, security-sensitive operations.
- Claude Code, Cursor, Codex are all harnessed coding agents. The harness is what makes them useful.
- A harness is not just the agent loop. It's the stuff around the agent loop.

## Future Prediction

- 2025: year of agents
- 2026: year of harnesses
- 2027 (prediction): year of dynamic, on-the-fly generated harnesses. The agent creates its own harness before doing the work. Self-aware guardrailing. "The next logical step towards AGI."

## IBM Context

IBM's open-source project "Open RAG" uses harness engineering for enterprise-level security on RAG operations with sensitive internal data (Teams calls, PDFs, invoices).

## What Sets This Talk Apart

Tejas builds a harness live from scratch, incrementally. The other two videos in this collection describe harness engineering conceptually. This one shows the actual code: tool registry, agent loop, guardrails, verify step, login handler. The GPT-3.5 Turbo constraint makes the point viscerally: the model barely matters if the harness is good enough.
