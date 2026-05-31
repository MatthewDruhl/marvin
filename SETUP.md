# MARVIN - First-Time Setup

**Check if setup is needed:**
- Does `state/current.md` contain placeholders like "[Add your priorities here]"?
- Is there no runtime-specific user profile or adapter context for the AI you are using?

**If setup is needed:** Read `.marvin/onboarding.md` and follow that guide instead of the normal `/marvin` flow.

## After Cloning

Run this once per clone for all runtimes:

```bash
git config core.hooksPath .hooks
```

## Codex Setup

Codex uses `AGENTS.md` as the project adapter. No skill symlinks are required for Codex in this repo.

For "start MARVIN", `/marvin`, or equivalent startup requests:

1. Read `AGENTS.md`.
2. Run from the repo root:

   ```bash
   python3 scripts/marvin_start.py
   ```

3. Use the startup packet as source context.
4. Follow `skills/marvin/SKILL.md`.

Shared runtime-neutral context lives in:

- `context/user-profile.md`
- `context/marvin-operating-rules.md`

Workflow procedures live in `skills/*/SKILL.md`. Codex slash commands are not auto-registered from `.claude/commands/*`; use the command routing table in `AGENTS.md` and read the matching skill directly.

### Codex Limitations

- `.claude/commands/*` files are Claude adapters, not Codex command registrations.
- Project MCP servers from `.mcp.json` may not be available automatically in Codex. If Gmail or calendar tools are unavailable during `/marvin`, report those checks as skipped instead of failing silently.
- Keep external-action safeguards: confirm before sending email, posting Slack messages, changing calendars, publishing, deleting, or overwriting.

## Claude Code Setup

Run these once per clone when using Claude Code:

```bash
# 1. Symlink global skills so they're available in all projects
for skill in skills/grill-me skills/harden skills/improve-codebase-architecture skills/prd-to-issues skills/tdd skills/write-a-prd; do
  ln -sf "$PWD/$skill" "$HOME/.claude/skills/$(basename $skill)"
done

# 2. Install RTK — compresses Bash command output to reduce token usage (60-90% on git, tests, etc.)
brew install rtk
rtk init -g   # adds a hook to ~/.claude/settings.json; restart Claude Code after
```
