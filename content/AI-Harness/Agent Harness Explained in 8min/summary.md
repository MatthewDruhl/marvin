# Agent Harness Explained in 8min

**Source:** https://www.youtube.com/watch?v=1a1VXDdIyrk
**Creator:** Caleb Bright
**Length:** ~8 minutes
**Date transcribed:** 2026-05-27

---

## Core Concept

Harness engineering is the layer above context engineering. It puts the agent into a structured environment with a loop, fresh context per iteration, and strict start/finish rules for each task.

## Evolution Timeline

1. **Prompt engineering** (2022, ChatGPT era) — 4K token windows, single-shot responses. Limited.
2. **Context engineering** — tool calling, MCP, RAG to manage the context window more efficiently. Gave rise to coding agents (Cursor, Windsurf, Kline, Roo, Aider).
3. **The scaling problem** — as tasks got longer, context summarization became the bottleneck. Agents would summarize mid-task and lose track, assume features were done when they weren't, or skip entire sections.
4. **Harness engineering** (early 2026) — stepped one layer above. Instead of stretching a single context window, loop the agent with fresh context per iteration under strict task rules.

## Why Context Engineering Breaks Down

When an agent works on a 12-hour task, the context window fills up. The agent summarizes to shrink it. But summarization is lossy. The agent:
- Assumes tasks are finished when they're not
- Oversimplifies remaining work
- Produces half-completed features

The elastic self-managing context window gives the appearance of long-range capability but isn't reliable.

## The Harness Pattern

The fix is simple architecturally:

1. Generate a large requirements document (PRD)
2. Outline it into a structured task list (often JSON)
3. Loop: pick one task, execute it with a fresh context window, test, document
4. Repeat until all tasks are complete

Each iteration gets a fresh prompt and fresh context. No summarization drift.

## Key Points

- Harness engineering doesn't replace prompt or context engineering. It builds on top of both. Prompt engineering still drives the agent's persona/system prompt. Context engineering still handles tool calling, RAG, etc.
- The RALF loop is cited as the primary example. Its power comes from simplicity: the repos are tiny.
- Anthropic has their own simple harness demonstration repo, same idea: lightweight environment, loop-based execution.
- Many coding agents (Cursor, etc.) have already adopted harness layers internally.

## Difference from Cole's Video

Cole's video focuses more on the AI layer components (rules, skills, hooks, MCPs) and the mindset shift ("every mistake becomes a rule"). Caleb's video is more focused on the historical evolution and why the loop architecture solves the context summarization problem. Complementary perspectives on the same concept.

---

*Sponsor segment: Cursor (cloud agents, Slack integration, autonomous scheduling). Skipped in summary.*
