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

echo "Downloading transcript for: $URL"
yt-dlp --write-auto-sub --sub-format srt --sub-lang en --skip-download --output "transcript" "$URL"

# CQ-1: Find the actual SRT file (name may vary)
SRT_FILE=$(ls transcript*.srt 2>/dev/null | head -1)
if [[ -z "$SRT_FILE" ]]; then
    echo "No subtitle file found. The video may not have English subtitles." >&2
    exit 1
fi

echo "Cleaning SRT formatting..."
sed '/^[0-9]*$/d; /^[0-9:,]* --> /d; /^$/d' "$SRT_FILE" > transcript.txt

echo "Done. Transcript saved to: transcript.txt"
