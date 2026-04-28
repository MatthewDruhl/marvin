#!/usr/bin/env bash
# Hook: Block Write/Edit to .env files
# Type: PreToolUse (Write, Edit)
# Exit 0 = pass through, Exit 2 = block

if ! command -v jq &>/dev/null; then
  exit 0
fi

INPUT=$(cat)
FILE_PATH=$(echo "$INPUT" | jq -r '.tool_input.file_path // empty')

if [ -z "$FILE_PATH" ]; then
  exit 0
fi

# Block .env and .env.* but allow .env.example (safe, tracked in git)
BASENAME=$(basename "$FILE_PATH")
if [ "$BASENAME" = ".env.example" ]; then
  exit 0
fi
if echo "$BASENAME" | grep -qE '^\.(env)($|\.)'; then
  echo "BLOCKED: Cannot modify $BASENAME. .env files must be edited manually. See ~/.claude/CLAUDE.md safety guidelines." >&2
  exit 2
fi

exit 0
