# MARVIN Instruction Ownership

This file defines where MARVIN instructions belong so Claude, Codex, and future runtimes share the same behavior without copying workflow procedures into multiple places.

## Ownership Rules

- `skills/*/SKILL.md` owns workflow procedures, numbered steps, mode behavior, scoring rules, templates, and tool-specific execution details.
- `context/*` owns runtime-neutral MARVIN rules, user profile context, privacy boundaries, and shared operating assumptions.
- `CLAUDE.md` owns the Claude-facing workspace overview: what MARVIN is, the workspace layout, high-level capabilities, and links to canonical context.
- `AGENTS.md` owns the Codex adapter: Codex startup path, command-to-skill routing, and Codex-specific constraints.
- `.claude/commands/*` owns Claude slash-command registration and routing only. Command files may include frontmatter, usage examples, argument parsing hints, and a pointer to the canonical skill, but not copied workflow procedures.
- Runtime hooks own hard safety enforcement only when a violation would cause damage and should be blocked mechanically.

## Workflow Change Order

When MARVIN behavior changes, update files in this order:

1. Update the canonical `skills/*/SKILL.md` file for procedural changes.
2. Update `context/*` if the change is runtime-neutral policy, safety, or shared operating context.
3. Update runtime adapters only if routing, invocation syntax, or runtime-specific startup behavior changed:
   - Claude: `.claude/commands/*`
   - Codex: `AGENTS.md`
   - Claude workspace overview: `CLAUDE.md`
4. Run the instruction drift check:
   ```bash
   python3 scripts/check_instruction_drift.py
   ```
5. Add a session log note when the behavior change is material to future MARVIN sessions.

## Adapter Checklist

Before changing `CLAUDE.md`, `AGENTS.md`, or `.claude/commands/*`, confirm:

- The canonical skill already contains the full workflow.
- The adapter points to the skill instead of restating its steps.
- The adapter contains only runtime-specific routing, usage, or constraints.
- Existing slash command files remain present; deleting a `.claude/commands/*.md` file removes that Claude command registration.
- Any duplicated procedure removed from an adapter was preserved in the matching skill first.

## Drift Review

Use `scripts/check_instruction_drift.py` to catch mapped command wrappers that likely copied procedure content from a skill. The script is intentionally lightweight: it discovers command-to-skill mappings from skill frontmatter `metadata.slash-command`, then checks for missing skill references, oversized wrappers, and procedural headings inside `.claude/commands/*`.

Unmapped command wrappers should be reviewed manually. If an unmapped command grows into a reusable workflow, create or update a canonical skill first and set its `metadata.slash-command` value.
