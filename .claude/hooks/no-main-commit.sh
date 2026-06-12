#!/usr/bin/env bash
# Hook: Block git commit on main/master branch
# Type: PreToolUse (Bash)
# Exit 0 = pass through, Exit 2 = block

if ! command -v jq &>/dev/null; then
  exit 0
fi

INPUT=$(cat)
CMD=$(echo "$INPUT" | jq -r '.tool_input.command // empty')

if [ -z "$CMD" ]; then
  exit 0
fi

# Only check commands where git commit appears in command position
# (start of command or after a separator), not anywhere in the string.
# Prevents false positives when quoted text merely mentions committing
# (e.g. an issue body passed to gh issue create).
if ! echo "$CMD" | grep -qE '(^|[;&|]\(?)\s*(command\s+)?git\s+(-[A-Za-z]+\s+\S+\s+)*commit'; then
  exit 0
fi

# Extract target directory from cd command if present
TARGET_DIR=$(echo "$CMD" | grep -oE 'cd\s+[^ ;&|]+' | head -1 | sed 's/^cd\s*//')
if [ -n "$TARGET_DIR" ]; then
  # Expand ~ to home directory
  TARGET_DIR=$(eval echo "$TARGET_DIR")
  BRANCH=$(git -C "$TARGET_DIR" rev-parse --abbrev-ref HEAD 2>/dev/null)
else
  BRANCH=$(git rev-parse --abbrev-ref HEAD 2>/dev/null)
fi

if [ "$BRANCH" = "main" ] || [ "$BRANCH" = "master" ]; then
  echo "BLOCKED: Cannot commit directly to $BRANCH. Create a feature branch first (e.g., git checkout -b fix/description)." >&2
  exit 2
fi

exit 0
