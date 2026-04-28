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

# Only check commands that look like git commit
if ! echo "$CMD" | grep -qE 'git\s+commit'; then
  exit 0
fi

# Get current branch
BRANCH=$(git rev-parse --abbrev-ref HEAD 2>/dev/null)

if [ "$BRANCH" = "main" ] || [ "$BRANCH" = "master" ]; then
  echo "BLOCKED: Cannot commit directly to $BRANCH. Create a feature branch first (e.g., git checkout -b fix/description)." >&2
  exit 2
fi

exit 0
