---
name: spec-dev
description: |
  Spec-driven development workflow. Reads a GitHub issue spec, plans the approach,
  gets user approval, then runs TDD + implementation in the background.
  Use when user types /spec-dev or wants to implement a GitHub issue.
license: MIT
compatibility: marvin
metadata:
  marvin-category: development
  user-invocable: true
  slash-command: /spec-dev
  model: default
  proactive: false
---

# Spec-Driven Development

Implement a GitHub issue through a structured spec-to-PR workflow.
Interactive for planning, background for execution.

## When to Use

- User types `/spec-dev <issue-number>`
- User wants to implement a feature or fix from a GitHub issue
- User wants structured, verifiable development

## Requirements

- A GitHub issue number with acceptance criteria
- If no issue exists, refuse and direct user to `/write-a-prd` or manual issue creation
- The issue MUST have acceptance criteria. If missing, stop and ask the user to add them

## Process

### Phase 1: Interactive (requires user)

#### Step 1: Read the Spec

1. If user didn't specify a repo, ask which project this issue belongs to
2. Look up the project in `state/projects.md` to get the repo and path
3. Fetch the issue: `gh issue view <number> --repo <owner/repo> --comments`
4. Read the full issue body and any comments
5. Verify acceptance criteria exist. If missing or vague, stop:
   "This issue needs acceptance criteria before I can build it. Add them to
   the issue or tell me what 'done' looks like."

#### Step 2: Explore the Codebase

1. `cd` to the project path from `state/projects.md`
2. Read the project's CLAUDE.md if it exists
3. Identify the files and modules that will be affected
4. Check for existing tests and test patterns in the project
5. Understand current architecture before proposing changes

#### Step 3: Plan

Present the plan to the user:

```
**Issue:** #<number> - <title>
**Repo:** <owner/repo>
**Branch:** <type>/<short-description>

**Acceptance Criteria:**
- [ ] <criterion 1>
- [ ] <criterion 2>
- [ ] <criterion 3>

**Approach:**
1. <what will be changed and why>
2. <what will be changed and why>

**Tests to write:**
1. <test description> (verifies: criterion X)
2. <test description> (verifies: criterion Y)

**Files affected:**
- <file> — <what changes>

Approve this plan?
```

**Rules for the plan:**
- Every acceptance criterion must map to at least one test
- Every test must trace back to an acceptance criterion
- If a criterion can't be tested, flag it and ask the user

**Wait for explicit user approval before proceeding.**

### Phase 2: Background (no user needed)

After user approves the plan, spawn a background agent with worktree
isolation to execute the build.

#### Agent Instructions

Pass the following to the background agent:

1. **Setup**
   - You are implementing issue #<number> for <repo>
   - Create branch: `<type>/<short-description>`
   - Here is the approved plan: <full plan from Step 3>
   - Here is the spec: <full issue body>
   - Read the project's CLAUDE.md before writing any code

2. **TDD Loop** (follow `/tdd` skill philosophy)
   - Write tests one at a time against the acceptance criteria
   - Each test must verify behavior through public interfaces
   - Vertical slices only: one test, then implementation, then next test
   - Never write all tests first (horizontal slicing)
   - Run tests after each implementation to confirm GREEN

3. **Implement**
   - Write minimal code to pass each test
   - Follow existing patterns in the codebase
   - Keep code clean, clear, and concise
   - No speculative features or over-engineering

4. **Verify Against Spec**
   - Re-read the original issue (fetch it again, do not rely on memory)
   - Walk through each acceptance criterion:
     - Is there a test that verifies it?
     - Does the test pass?
     - Does the implementation actually satisfy the criterion?
   - If any criterion is NOT met, go back and fix it before proceeding
   - Do NOT claim a criterion is met without verifying. Read the code.

5. **Commit and PR**
   - Commit with clear messages (follow project's commit conventions)
   - Push the branch
   - Create a PR with:
     ```
     ## Summary
     <what was built and why>

     ## Spec
     Closes #<issue-number>

     ## Acceptance Criteria Verification
     - [x] <criterion 1> — verified by <test name>
     - [x] <criterion 2> — verified by <test name>

     ## Test Plan
     - [ ] All tests pass locally
     - [ ] Review code changes
     - [ ] Verify against original issue

     🤖 Generated with [Claude Code](https://claude.com/claude-code)
     ```
   - Do NOT merge the PR. Do NOT close the issue.

6. **Report Back**
   - Notify with: PR URL, test results, any concerns or decisions made

#### Spawning the Agent

```
Agent(
  description: "spec-dev: <repo>#<issue-number>",
  isolation: "worktree",
  run_in_background: true,
  prompt: <agent instructions above with all context>
)
```

Always use worktree isolation. Background agents sharing a working tree
fight over git checkout.

## Error Handling

- **Tests won't pass:** Agent makes 3 distinct attempts (different approach
  each time, not rerunning the same failing code), then stops and reports
  what failed, what was tried, and why. Does not force tests to pass.
- **Spec is ambiguous:** Agent stops and reports which criterion is unclear.
  Does not guess or interpret ambiguous requirements.
- **Missing dependencies:** Agent stops and reports what's needed.
  Does not install packages without project context.

## What This Skill Does NOT Do

- Create issues (use `/write-a-prd` + `/prd-to-issues`)
- Merge PRs (Matt's job)
- Auto-close issues (PR linkage handles this on merge)
- Skip the plan approval checkpoint

---

*Skill created: 2026-05-28*
