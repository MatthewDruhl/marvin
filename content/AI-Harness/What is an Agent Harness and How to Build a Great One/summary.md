# What is an Agent Harness? and How to Build a Great One!

**Source:** https://youtu.be/nWzXyjXCoCE?si=xS0BY0jNSrK3ViR-
**Creator:** (unnamed, technical YouTube channel)
**Length:** ~15 minutes
**Date transcribed:** 2026-05-27

---

## Core Definition

A harness is a fixed architecture that turns a model into an agent. Models are one-shot text generators. The harness gives a model the ability to take action, see consequences, and keep going until the problem is solved. Model = engine, harness = car.

## Harness vs. Framework

This video draws a clear distinction the others don't:

- **Framework** (LangChain, LangGraph, AutoGen, CrewAI): gives you abstractions (state graphs, chains, memory, retrievers). You, the human, wire them together.
- **Harness**: ships a working agent. No assembly step. A while loop with a tool registry and permission layer. You provide the goal, the harness handles the rest.

A framework is built for a human to assemble an agent. A harness is built for the agent itself to do a task.

## The Nine Components

### 1. While Loop (Iteration Loop)
The foundation. Model reads system prompt, decides which tool to call, runs it, feeds result back into context, loops again. Exits when the model produces a text-only response or hits max iterations.

### 2. Context Management
The context tree grows every turn. The harness decides what to keep verbatim, what to summarize, what to throw away. Claude Code triggers compaction around 80-90% of the context budget. Design decision: bring in full tool call traces or just input/output.

### 3. Skills and Tools
Tools are primitives (read file, edit file, run bash, search code). Skills are organizational knowledge encoded in markdown files, layered on top. Tools are universal. Skills are specific to your team and workflow. A registry tracks what's available, what permissions each needs, and how calls get dispatched.

### 4. Sub-Agent Management
When a task is too big or too parallel for one thread, the harness spawns sub-agents. Each gets its own session, restricted tool set, and focused system prompt. Pattern: spawn, restrict, collect.

### 5. Built-In Skills
Non-negotiable primitives every coding harness must ship: file operations, shell execution, code navigation. Beyond primitives: higher-level skills like git commit, open PR, run tests. Must use pure standard libraries (no framework dependencies).

### 6. Session Persistence / Memory
Append-only JSON (or markdown) files. Every message, tool result, and compaction event gets one line, flushed immediately. If the process crashes, the file survives. Replay reconstructs the full session. Two runs can share the same log without conflicts.

### 7. System Prompt Assembly
The system prompt is not a static string. It's a pipeline that walks ancestor directories looking for instruction files (claude.md, agents.md). Important: keep the static part first, dynamic content second, or you break prefix caching.

### 8. Lifecycle Hooks
Pre-tool hooks fire before execution. They receive tool name + input and can allow, deny, or modify the call. Post-tool hooks fire after and can inspect results for auditing/logging/observability. They cannot block.

### 9. Permissions and Safety
Each tool declares minimum permission: read, workspace, or full. The harness enforces this at dispatch time before the tool runs. For bash, the harness classifies commands dynamically (ls = read-only, rm = full access). Interactive approvals let the agent pause and ask before destructive operations.

## What Sets This Video Apart

Most structured of the four. Provides a clear taxonomy (nine named components) and a reference implementation in Python for each. The harness-vs-framework distinction is unique to this video and useful for understanding where tools like LangChain fit (or don't). Less about philosophy/mindset, more about architecture and implementation patterns.

## Mapping to MARVIN / Claude Code

| Component | MARVIN/Claude Code equivalent |
|-----------|-------------------------------|
| While loop | Claude Code's agent loop |
| Context management | Auto-compaction (200K → 1M budget) |
| Skills and tools | `skills/*.md` + built-in tools (Read, Edit, Bash, etc.) |
| Sub-agents | Agent tool with worktree isolation |
| Built-in skills | Read, Write, Edit, Grep, Glob, Bash |
| Session persistence | `sessions/*.md`, memory system |
| System prompt assembly | CLAUDE.md hierarchy (global → project → local) |
| Lifecycle hooks | `.claude/hooks/` (pre/post tool) |
| Permissions | Permission modes (read-only, workspace, full, auto) |
