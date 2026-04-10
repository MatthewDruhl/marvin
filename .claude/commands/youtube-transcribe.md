---
description: Download and clean a YouTube transcript from a video URL
---

# /youtube-transcribe

Download auto-generated subtitles from a YouTube video and strip SRT formatting to produce a clean plain-text transcript.

## Instructions

The user has provided a YouTube URL: `$ARGUMENTS`

Run the transcribe script:

```bash
bash skills/youtube-transcribe/transcribe.sh "$ARGUMENTS"
```

After it completes:
1. Confirm `transcript.txt` was created
2. Ask if the user wants to view the contents or have the video summarized
