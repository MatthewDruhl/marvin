# Google Workspace Integration

Connect MARVIN to your Google account for email and calendar access.

## What It Does

- **Gmail** — Read, search, and send emails
- **Calendar** — View events, check availability, create meetings

Additional tools available (Drive, Docs, Sheets, Slides, Chat, Forms, Contacts, Search) — select during setup.

## How It Works

The integration uses the [workspace-mcp](https://github.com/ergovia-devs/workspace-mcp) package, configured as a project-level MCP server in `.mcp.json`. OAuth credentials are loaded from `.env` via `dotenv-cli`.

### Architecture

```
.mcp.json                          # MCP server definition (checked in)
.env                                # OAuth credentials (gitignored)
.google-workspace-credentials/      # OAuth tokens (gitignored)
.claude/settings.local.json         # Enables the MCP server (gitignored)
```

### What `.mcp.json` looks like

```json
{
  "mcpServers": {
    "google-workspace": {
      "type": "stdio",
      "command": "npx",
      "args": [
        "-y", "dotenv-cli", "-e", ".env", "--",
        "uvx", "workspace-mcp", "--tools", "gmail", "calendar"
      ],
      "env": {}
    }
  }
}
```

Key detail: `dotenv-cli` loads `.env` so OAuth secrets never appear in `.mcp.json`.

### Required `.env` variables

```
GOOGLE_OAUTH_CLIENT_ID=<your-client-id>
GOOGLE_OAUTH_CLIENT_SECRET=<your-client-secret>
GOOGLE_MCP_CREDENTIALS_DIR=.google-workspace-credentials
```

## Setup

### Option A: Interactive setup script

```bash
./integrations/google-workspace/setup.sh
```

The script will:
1. Check prerequisites (uv, Claude Code)
2. Prompt for OAuth Client ID and Secret
3. Let you choose scope (user vs project) and tools
4. Configure the MCP server via `claude mcp add`
5. First Google request opens browser for OAuth login

### Option B: Manual setup

1. Create a Google Cloud project and OAuth 2.0 credentials (Desktop app type)
2. Add the required variables to `.env`
3. Copy the `.mcp.json` example above into your project root
4. Enable the server in `.claude/settings.local.json`:
   ```json
   { "enabledMcpjsonServers": ["google-workspace"] }
   ```
5. Start Claude Code — first Google request triggers OAuth browser flow

## Prerequisites

- **uv** / **uvx** — `curl -LsSf https://astral.sh/uv/install.sh | sh`
- **Node.js / npx** — For `dotenv-cli`
- **Claude Code** — `npm install -g @anthropic-ai/claude-code`
- **Google Cloud OAuth credentials** — Desktop app type, with Gmail and Calendar API enabled

## Known Issues

### Slack-bot / `claude --print` can't find the MCP

The `.mcp.json` approach works in interactive Claude Code sessions but **not** in `claude --print` (non-interactive) mode. The CLI in print mode may skip project-level MCP discovery.

**Fix:** Add `--mcp-config .mcp.json` to the `claude --print` command:
```bash
claude --print --mcp-config .mcp.json "Check my email"
```

### Tasks API bug

The `workspace-mcp` package has a known bug with Google Tasks. The setup script excludes it by default.

## Danger Zone

| Action | Risk Level | Who's Affected |
|--------|------------|----------------|
| Send emails | **High** | Recipients see it immediately |
| Create/modify calendar events | **Medium** | Other attendees are notified |
| Delete emails | **Medium** | May be recoverable from trash |
| Read emails, calendar | Low | No external impact |

**MARVIN will always confirm before sending emails or modifying calendar events.**

## Try It

After setup:
- "What's on my calendar today?"
- "Show me my unread emails"
- "Search Gmail for messages from [company]"
- "What meetings do I have this week?"

---

*Integration by Sterling Chin. README updated 2026-04-07.*
