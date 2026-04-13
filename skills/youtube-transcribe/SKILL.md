---
name: youtube-transcribe
description: |
  Download and clean a YouTube video transcript using auto-generated subtitles.
  Strips SRT timing/sequence formatting and outputs plain readable text.
license: MIT
compatibility: marvin
metadata:
  marvin-category: utility
  user-invocable: true
  slash-command: youtube-transcribe
  model: default
  proactive: false
---

# YouTube Transcribe

Downloads auto-generated subtitles from a YouTube video and strips SRT formatting to produce a clean plain-text transcript.

## When to Use

- User provides a YouTube URL and wants a transcript
- User says "transcribe", "get transcript", "download subtitles", etc.

## Process

### Step 1: Run the shell script

Execute with the URL the user provided:

```bash
bash skills/youtube-transcribe/transcribe.sh "<url>"
```

This runs two commands:
1. `yt-dlp` downloads the auto-generated subtitles to `content/transcripts/`
2. `sed` strips sequence numbers, timestamps, and blank lines → `transcript_VIDEO_ID.txt`

### Step 2: Confirm output

Tell the user:
- Where the transcript was saved (path printed by the script, under `content/transcripts/`)
- Offer to display the contents or summarize the video

## Output

Files are written to `content/transcripts/` with video-ID-based filenames:
- `transcript_VIDEO_ID.en.srt` — raw subtitle file (intermediate, can discard)
- `transcript_VIDEO_ID.txt` — clean plain-text transcript

## Notes

- Requires `yt-dlp` installed (`brew install yt-dlp`)
- Only works if the video has auto-generated or manual subtitles
- If the video has no English subtitles, `yt-dlp` will report no subtitles found — inform the user

---

*Skill created: 2026-04-10*
