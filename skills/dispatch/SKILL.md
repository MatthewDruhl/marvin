---
name: dispatch
description: |
  Launch a background agent against any registered project with a defined task,
  under the standard agent contract, logged to the run ledger. Use when the user
  types /dispatch or asks to run an agent against a project for work that no
  specialized skill (spec-dev, harden) already covers.
license: MIT
compatibility: marvin
metadata:
  marvin-category: orchestration
  user-invocable: true
  slash-command: /dispatch
  model: default
  proactive: false
---

# Dispatch Skill

Generic orchestration entry point: pick a project, define a task, launch a contracted background agent, log the run.

Specialized skills win: if the task is "implement GitHub issue N", use `/spec-dev`; if it's "audit this project", use `/harden`. Dispatch is for everything else (refactors, research against a codebase, doc generation, migrations, experiments).

## Process

### Step 1: Resolve the Project

1. If the user named a project, look it up in `state/projects.md` for the path, repo, and current branch. If it's not registered, ask whether to add it first.
2. If no project was named, ask which one (list the registered projects).

### Step 2: Define the Task

Confirm with the user before launching:

```
**Project:** <name> (<path>)
**Task:** <one-line description>
**Deliverable:** <PR | report in content/ | files in project | analysis reply>
**Branch:** <type>/<short-description> (omit if read-only task)
**Mode:** <background | inline>

Launch?
```

Rules:
- Every dispatch has a named deliverable. "Look into X" becomes "write findings to `content/<project>-<topic>-<date>.md`".
- Read-only tasks (research, analysis) skip the branch and may use an Explore-type agent.
- Tasks that modify files always get a branch and produce a PR.

### Step 3: Launch

Spawn the agent with:

```
Agent(
  description: "dispatch: <project> — <short task>",
  isolation: "worktree",          // for any task that writes files
  run_in_background: true,
  prompt: <task definition>
        + <full text of context/agent-contract.md>
        + <project path, repo, relevant context from state/projects.md>
        + "Read the project's CLAUDE.md before changing anything."
)
```

The contract is non-negotiable and always included verbatim. Add task-specific instructions on top; never weaken contract rules.

### Step 4: Log the Run

Immediately after spawning, append an entry to `state/agent-runs.json` (schema: `context/agent-runs.example.json`): id `run-YYYY-MM-DD-NNN`, project, skill `dispatch`, task, branch (or null), status `running`, launched date. Update `last_updated`.

### Step 5: On Report-Back

1. Update the ledger entry: status `needs-review`, completed date, output location from the agent's report, notes with test results or concerns.
2. Relay the agent's report to the user: what was produced, where it lives, what needs review.
3. If the deliverable was a report, save or confirm it landed in `content/` with a descriptive name.

## What This Skill Does NOT Do

- Merge PRs or close issues (Matt's job)
- Replace spec-dev or harden for their specialties
- Launch agents without a confirmed task definition and deliverable
- Skip ledger logging

---

*Skill created: 2026-06-12 (marvin#289)*
