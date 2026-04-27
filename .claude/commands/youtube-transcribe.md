---
description: Download and clean a YouTube transcript from a video URL
---

The user has provided a YouTube URL: `$ARGUMENTS`

**Run this as a background agent.** Use the Agent tool with `run_in_background: true` to spawn an agent that:

1. Runs the transcribe script:
```bash
bash skills/youtube-transcribe/transcribe.sh "$ARGUMENTS"
```

2. Follows `skills/youtube-transcribe/SKILL.md` for post-processing steps (size check, summarization offer).

3. Reports back what was downloaded and where it was saved.

Tell the user the transcript is downloading in the background and continue with other work.
