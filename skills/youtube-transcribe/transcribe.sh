#!/usr/bin/env bash
# youtube-transcribe: download auto-generated subtitles and strip SRT formatting
# Usage: ./transcribe.sh <youtube-url>

set -euo pipefail

if [[ $# -eq 0 ]]; then
    echo "Usage: $0 <youtube-url>" >&2
    exit 1
fi

URL="$1"

# SEC-1: Validate URL is a YouTube link
if [[ ! "$URL" =~ ^https://(www\.youtube\.com/|youtu\.be/) ]]; then
    echo "Error: URL must be a YouTube link (https://www.youtube.com/... or https://youtu.be/...)" >&2
    exit 1
fi

# SEC-3: Ensure yt-dlp is installed
if ! command -v yt-dlp &>/dev/null; then
    echo "yt-dlp not found. Install: brew install yt-dlp" >&2
    exit 1
fi

# DEC-1: Output to dedicated directory instead of CWD
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
OUTPUT_DIR="$REPO_ROOT/content/transcripts"
mkdir -p "$OUTPUT_DIR"

# SEC-2: Derive unique filename from video ID to avoid overwrites
if [[ "$URL" =~ [\?\&]v=([a-zA-Z0-9_-]+) ]]; then
    VIDEO_ID="${BASH_REMATCH[1]}"
elif [[ "$URL" =~ youtu\.be/([a-zA-Z0-9_-]+) ]]; then
    VIDEO_ID="${BASH_REMATCH[1]}"
else
    VIDEO_ID="$(date +%Y%m%d_%H%M%S)"
fi

echo "Downloading transcript for: $URL"
yt-dlp --write-auto-sub --sub-format srt --sub-lang en --skip-download --output "$OUTPUT_DIR/transcript_${VIDEO_ID}" "$URL"

# CQ-1: Find the actual SRT file (name may vary)
SRT_FILE=$(ls "$OUTPUT_DIR"/transcript_${VIDEO_ID}*.srt 2>/dev/null | head -1)
if [[ -z "$SRT_FILE" ]]; then
    echo "No subtitle file found. The video may not have English subtitles." >&2
    exit 1
fi

OUTPUT_FILE="$OUTPUT_DIR/transcript_${VIDEO_ID}.txt"
echo "Cleaning SRT formatting..."
sed '/^[0-9]*$/d; /^[0-9:,]* --> /d; /^$/d' "$SRT_FILE" > "$OUTPUT_FILE"

echo "Done. Transcript saved to: $OUTPUT_FILE"
