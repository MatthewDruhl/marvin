#!/usr/bin/env bash
# youtube-transcribe: download auto-generated subtitles and strip SRT formatting
# Usage: ./transcribe.sh <youtube-url>

set -euo pipefail

if [[ $# -eq 0 ]]; then
    echo "Usage: $0 <youtube-url>" >&2
    exit 1
fi

URL="$1"

echo "Downloading transcript for: $URL"
yt-dlp --write-auto-sub --sub-format srt --skip-download --output "transcript" "$URL"

echo "Cleaning SRT formatting..."
sed '/^[0-9]*$/d; /^[0-9:,]* --> /d; /^$/d' transcript.en.srt > transcript.txt

echo "Done. Transcript saved to: transcript.txt"
