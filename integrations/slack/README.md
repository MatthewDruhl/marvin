# MARVIN Slack Bot

Two-way Slack bot that pipes messages to Claude Code CLI via Socket Mode.

## Setup

1. Copy `.env.example` to `~/marvin/.env` and fill in your Slack tokens.
2. Set `ALLOWED_SLACK_USERS` to a comma-separated list of Slack user IDs.
3. Run: `uv run python bot.py`

## Security Notes

### System Prompt (defense-in-depth)

The `SYSTEM_PROMPT` constant instructs Claude to stay in role, refuse credential
disclosure, and reject prompt-injection attempts.  This is a **defense-in-depth
measure, not a security boundary**.  LLM system prompts can be bypassed by
sufficiently creative inputs.  The bot relies on multiple layers of defense:

- **Access control** (`ALLOWED_SLACK_USERS`) -- only listed users can interact.
- **Input validation** -- message length limits.
- **Output scrubbing** (`_scrub_secrets`) -- known secret patterns are redacted
  before any response reaches Slack.
- **Rate limiting** -- per-user sliding-window limit to prevent abuse.
- **System prompt** -- instructs the model to refuse dangerous requests, but
  should never be the sole control protecting sensitive data.

Do not treat the system prompt as a guarantee.  Always keep secrets out of the
model's reachable context (e.g., never store tokens in files Claude can read).

### Rate Limiting

Each user is limited to 30 requests per hour (sliding window).  This prevents
runaway usage and limits blast radius if an authorized account is compromised.
