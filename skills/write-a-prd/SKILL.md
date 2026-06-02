---
name: write-a-prd
description: |
  Create a PRD through user interview, codebase exploration, and module design,
  then submit as a GitHub issue. Use when user wants to write a PRD, create a
  product requirements document, or plan a new feature.
license: MIT
compatibility: marvin
metadata:
  marvin-category: development
  user-invocable: true
  slash-command: /write-a-prd
  model: default
  proactive: false
---

# Write a PRD

Create a structured PRD with testable acceptance criteria, submitted as a
GitHub issue. Every step is required. No steps may be skipped.

## When to Use

- User wants to plan a new feature or significant change
- User says "write a PRD", "plan this feature", "I need a spec"
- After `/extract-specs` has produced a requirements brief

## Process

### Step 1: Gather Context

1. Ask the user which project this is for. Look up the repo and path in `state/projects.md`. This is required regardless of whether a brief exists.

**If a requirements brief exists** (from `/extract-specs`):
2. Ask the user which brief to use, or check for recent briefs in the
   project's folder
3. Read the brief. Use it as the starting point. Do not re-interview
   on topics already covered.
4. Identify gaps and open questions from the brief that still need answers.

**If no brief exists:**
2. Ask the user for a detailed description of the problem they want to solve
   and any ideas for solutions

### Step 2: Explore the Codebase

1. Read the project's CLAUDE.md if it exists
2. Identify modules, patterns, and architecture relevant to the feature
3. Check for existing implementations that overlap with the proposed feature
4. Verify the user's assertions about current behavior by reading the code

Do not take the user's description of the codebase at face value. Read it.

### Step 3: Interview

Interview the user about every aspect of this plan until reaching shared
understanding. Walk down each branch of the design tree, resolving
dependencies between decisions one by one.

**Present one question at a time. Wait for the answer before asking the next.**

Use this checklist as a reference for areas to cover. Do NOT blast through
them all at once. Ask one question, wait for the answer, then decide what
to ask next based on the response. Skip areas the requirements brief
already resolved.

**Areas to cover:**
1. **Problem clarity:** What problem does this solve? Who has this problem?
2. **Scope:** What's in scope? What's explicitly out of scope?
3. **User behavior:** Happy path and failure cases, step by step.
4. **Constraints:** Technical limitations, timeline, dependencies.
5. **Edge cases:** Unexpected inputs, empty states, errors.
6. **Integration:** How does this interact with existing features?

If a question can be answered by exploring the codebase, explore the
codebase instead of asking the user.

### Step 4: Design Modules

1. Sketch out the major modules to build or modify
2. For each module, define:
   - Its public interface (what it exposes)
   - Its responsibility (what it owns)
   - Its depth (complex implementation behind a simple interface is good)
3. Look for opportunities to extract deep modules that can be tested in
   isolation
4. Present the module design to the user. Get approval.

### Step 5: Write User Stories with Acceptance Criteria

For each user story:

```markdown
### US-<number>: <short title>

**As a** <actor>, **I want** <feature>, **so that** <reason>.

**Acceptance criteria:**
- [ ] <testable criterion — describes observable behavior>
- [ ] <testable criterion — describes observable behavior>
- [ ] <testable criterion — describes observable behavior>
```

**Rules for acceptance criteria:**
- Every criterion must be testable. "Works correctly" is not testable.
  "Returns a 200 with the user's name in the response body" is testable.
- Every criterion must describe behavior from the outside, not
  implementation. "Uses a hashmap internally" is implementation.
  "Lookups return in under 100ms" is behavior.
- If you can't write a testable criterion, the user story is too vague.
  Go back to the interview and clarify.
- Fewer precise criteria beat many vague ones. Aim for 2-5 per story.

### Step 6: Write the PRD

Assemble the full PRD using this template:

```markdown
## Problem Statement

<The problem from the user's perspective. What's broken or missing.
Why it matters.>

## Solution

<The solution from the user's perspective. What changes and how it
helps. Not implementation details.>

## User Stories

<All user stories from Step 5, with acceptance criteria>

## Module Design

<Modules from Step 4: interfaces, responsibilities, dependencies.
No file paths or code snippets — these go stale.>

## Implementation Decisions

<Decisions made during the interview:>
- <Architectural choices and why>
- <Schema changes>
- <API contracts>
- <Integration approach>
- <What was explicitly ruled out and why>

## Testing Strategy

<For each module the user wants tested:>
- <Module name>: <what behaviors to test, referencing which user
  stories/criteria they verify>
- <Prior art>: <existing tests in the codebase that follow similar
  patterns>

## Out of Scope

<What was discussed but explicitly deferred. Include WHY it's deferred
so future readers don't re-litigate it.>

## Open Questions

<Anything unresolved. If this section is not empty, the PRD is not
ready for implementation until these are answered.>
```

### Step 7: Verify Before Submitting

Before submitting the PRD as a GitHub issue, check:

- [ ] Every user story has testable acceptance criteria
- [ ] Every acceptance criterion describes observable behavior, not implementation
- [ ] The testing strategy references specific user stories
- [ ] Implementation decisions are consistent with the module design
- [ ] Out of scope items have a reason
- [ ] Open questions section is empty (if not, resolve them with the user first)
- [ ] The problem statement and solution are consistent with the user stories
- [ ] No assertions about the codebase that weren't verified by reading the code

If any check fails, fix it before proceeding.

### Step 8: Save and Submit

1. Save a local copy of the PRD to the project folder:
   `<project-path>/prd-<YYYY-MM-DD>.md`
2. Confirm with the user: "Ready to submit this PRD as a GitHub issue?"
3. Create the issue: `gh issue create --repo <repo> --title "PRD: <title>" --body <prd>`
4. Report the issue number and URL

## What This Skill Does NOT Do

- Skip steps
- Create implementation issues (that's `/prd-to-issues`)
- Make unverified claims about the codebase
- Submit a PRD with open questions unresolved
- Write acceptance criteria that can't be tested

---

*Skill created: 2026-01-22*
*Rewritten: 2026-05-28 — added testable acceptance criteria per user story,
removed skip permission, added verification pass, integrated with /extract-specs*
