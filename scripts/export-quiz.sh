#!/usr/bin/env bash
# Export quiz files for uploading to Claude.ai Project
# Usage: bash ~/marvin/scripts/export-quiz.sh

set -euo pipefail

MARVIN_DIR="$HOME/marvin"
EXPORT_DIR="$MARVIN_DIR/tmp/quiz-export"

# Files to export
FILES=(
    "skills/quiz/question-bank.md"
    "skills/quiz/teach-back-checklists.md"
    "state/learning.md"
)

# Create export directory
mkdir -p "$EXPORT_DIR"

# Copy files
echo "Exporting quiz files to $EXPORT_DIR ..."
for file in "${FILES[@]}"; do
    cp "$MARVIN_DIR/$file" "$EXPORT_DIR/"
    echo "  Copied $(basename "$file")"
done

echo ""
echo "Next steps:"
echo "  1. Go to claude.ai -> Projects -> DSA Quiz"
echo "  2. Upload these 3 files as project knowledge:"
echo "     - question-bank.md"
echo "     - teach-back-checklists.md"
echo "     - learning.md"
echo "  3. Start quizzing from any device!"
