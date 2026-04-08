# MARVIN - First-Time Setup

**Check if setup is needed:**
- Does `state/current.md` contain placeholders like "[Add your priorities here]"?
- Is there NO user profile in `~/.claude/CLAUDE.md`?

**If setup is needed:** Read `.marvin/onboarding.md` and follow that guide instead of the normal `/marvin` flow.

## After Cloning

Run these once per clone:

```bash
# 1. Activate pre-commit linter (ruff)
git config core.hooksPath .hooks

# 2. Symlink global skills so they're available in all projects
for skill in skills/grill-me skills/harden skills/improve-codebase-architecture skills/prd-to-issues skills/tdd skills/write-a-prd; do
  ln -sf "$PWD/$skill" "$HOME/.claude/skills/$(basename $skill)"
done
```
