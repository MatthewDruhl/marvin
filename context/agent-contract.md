# Agent Contract

The single rules document for every background agent MARVIN launches against a project. Skills that spawn agents (spec-dev, harden, dispatch, future skills) include this contract in the agent prompt instead of restating the rules. Source decisions: `state/decisions.md` 2026-04-26 (worktree isolation), global git workflow hard rules.

## Isolation

- Always spawn with `isolation: "worktree"`. Background agents sharing a working tree fight over git checkout and lose uncommitted changes. No exceptions for "quick" tasks.

## Git

- Never commit to `main` or `master`. Create a feature branch first.
- Branch naming: `<type>/<short-description>` (e.g., `feature/issue-123`, `fix/combat-respawn`).
- One PR per logical change. Push the branch, open a PR, stop.
- Never merge PRs. Never close issues directly (PR linkage closes them on merge). Merging is Matt's job.
- Commit messages follow the project's existing conventions.

## Write Scope

- Only write inside the target project directory (or the assigned worktree).
- Never write to MARVIN state files (`state/*`), memory, or any file outside the assigned scope. If the task seems to require it, stop and report instead.
- Never read or write `.env` files. Never echo secrets, tokens, or credentials in output, commits, or PR bodies.

## PR Format

```
## Summary
<what was built/changed and why>

## Spec
Closes #<issue-number>   (when working from an issue)

## Test Plan
- [x] <what was run and the result>

🤖 Generated with [Claude Code](https://claude.com/claude-code)
```

Skills may extend this (e.g., spec-dev adds Acceptance Criteria Verification) but never drop the Summary or Test Plan sections.

## Verification

- Never claim a criterion is met without checking: read the code, run the tests, paste real output.
- Tests that fail: make at most 3 distinct attempts (different approach each time), then stop and report what failed, what was tried, and why. Do not force tests to pass or skip them.
- Ambiguous requirements: stop and report which part is unclear. Do not guess.

## Report Back

Your final message is the run record. Include:
- What was produced and where it lives (PR URL, file path, or report location)
- Test/verification results (real numbers, not "should work")
- Any concerns, deviations from the plan, or follow-ups needed

The launching session logs your run in `~/marvin/state/agent-runs.json`; your report is what fills the `output` and `notes` fields, so make it precise.
