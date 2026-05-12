#!/usr/bin/env bash
# Hook: Enforce line limits on CLAUDE.md files
# Type: PostToolUse (Write, Edit)
# Global CLAUDE.md: 250 lines max
# Project CLAUDE.md: 400 lines max
# Exit 0 = pass, non-zero message = warning (post-tool, advisory)

if ! command -v jq &>/dev/null; then
  exit 0
fi

INPUT=$(cat)
FILE_PATH=$(echo "$INPUT" | jq -r '.tool_input.file_path // empty')

if [ -z "$FILE_PATH" ]; then
  exit 0
fi

BASENAME=$(basename "$FILE_PATH")
if [ "$BASENAME" != "CLAUDE.md" ]; then
  exit 0
fi

# File must exist to count lines
if [ ! -f "$FILE_PATH" ]; then
  exit 0
fi

LINE_COUNT=$(wc -l < "$FILE_PATH" | tr -d ' ')

# Determine which limit applies
if echo "$FILE_PATH" | grep -q "$HOME/.claude/CLAUDE.md"; then
  MAX=250
  LABEL="Global"
else
  MAX=400
  LABEL="Project"
fi

if [ "$LINE_COUNT" -gt "$MAX" ]; then
  echo "WARNING: $LABEL CLAUDE.md is $LINE_COUNT lines (max $MAX). Trim it or move content to skills/hooks/memory." >&2
  exit 2
fi

exit 0
