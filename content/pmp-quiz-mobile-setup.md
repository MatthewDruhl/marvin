# PMP Quiz Mobile Setup — Claude Code Channels

## Overview

Use Claude Code Channels to run `/pmp-quiz` from your phone via Telegram or Discord.

## How It Works

```
Phone (Telegram/Discord) → Bot API → Claude Code (Mac) → reads/writes local files → replies back
```

## Option 1: Telegram

- **Mobile install:** Telegram app (free)
- **Setup:** Create a bot via @BotFather in Telegram
- **Access:** DM the bot directly
- **Pros:** Simpler setup
- **Cons:** Single user — would need separate bots for Matt and Emily

## Option 2: Discord (Recommended)

- **Mobile install:** Discord app (free)
- **Setup:** Create a Discord server + Bot via Discord Developer Portal
- **Access:** Each person can DM the bot or use dedicated channels
- **Pros:** Both Matt and Emily can quiz independently
- **Cons:** Slightly more setup steps

## Requirements

- Claude Code v2.1.80+ (updated to 2.1.83 on 2026-03-25)
- Channels is a research preview feature (syntax may change)
- Mac must be running Claude Code session for the bot to work

## Setup Steps (TODO)

### Discord Setup
1. Create a Discord server (e.g., "PMP Study")
2. Go to Discord Developer Portal → create a Bot application
3. Get bot token
4. Configure Claude Code Channels MCP server for Discord
5. Invite bot to server
6. Test `/pmp-quiz matt` and `/pmp-quiz emily` from phone
7. Invite Emily to the server

---

*Created: 2026-03-25*
