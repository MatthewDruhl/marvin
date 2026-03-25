---
description: Show available commands and integrations
---

# /help - MARVIN Help

Show the user what MARVIN can do and what integrations are available.

## Instructions

### 1. Show Available Commands

Display this reference:

```
## Slash Commands

| Command     | What It Does                              |
|-------------|-------------------------------------------|
| /marvin     | Start a session with a briefing           |
| /end        | End session and save everything           |
| /update     | Quick checkpoint (save progress)          |
| /report     | Generate a weekly summary of work         |
| /wkplan     | Weekly planning session (set priorities)  |
| /dashboard  | Project momentum dashboard                |
| /analytics  | Session analytics and trends              |
| /learn-sync | Sync topics-learned.md into learning tracker |
| /commit     | Review and commit git changes             |
| /code       | Open MARVIN in your IDE                   |
| /help       | Show this help guide                      |
| /sync       | Get updates from MARVIN template          |
```

### 2. Show Active Skills

Display the skills MARVIN uses automatically:

```
## Active Skills (automatic)

| Skill | What It Does |
|-------|--------------|
| Daily Briefing | Calendar, tasks, learning reviews, habits, follow-ups |
| Learning Tracker | Spaced repetition for DSA & Data Engineering topics |
| Habit Tracker | Track exercise, DSA practice, coding streaks |
| Learning Journal | Capture TIL moments and coding insights |
| Interview Prep | Practice questions, mock interviews, company research |
| Networking CRM | Contact management and follow-up reminders |

These activate automatically based on what you say. For example:
- "I reviewed recursion" → Learning Tracker
- "Did exercise today" → Habit Tracker
- "TIL about decorators" → Learning Journal
- "Prep for GitHub interview" → Interview Prep
- "Add contact: Sarah at Stripe" → Networking CRM
```

### 3a. Show Current Integrations

Check what MCP servers are configured by running:
```bash
claude mcp list
```

Then display something like:

```
## Your Integrations

These are the tools MARVIN can currently access:

| Integration      | What It Does                                      |
|------------------|---------------------------------------------------|
| Google Workspace | Read/send email, check calendar, access Drive     |
| Atlassian        | View Jira tickets, search Confluence              |

(List only what's actually configured based on the mcp list output)
```

If no integrations are configured, say:
```
## Your Integrations

No integrations configured yet. I can help you set one up, or you can run the setup scripts in `.marvin/integrations/`.
```

### 3b. Show Available Integrations

Read `.marvin/integrations/README.md` to see the full list of available integrations, then display:

```
## Available Integrations

These can be added anytime. Browse `.marvin/integrations/` for details.

| Integration      | Setup Command                                   | What It Does                 |
|------------------|-------------------------------------------------|------------------------------|
| Google Workspace | ./.marvin/integrations/google-workspace/setup.sh | Gmail, Calendar, Drive       |
| Atlassian        | ./.marvin/integrations/atlassian/setup.sh        | Jira, Confluence             |

Want something else? Check `.marvin/integrations/REQUESTS.md` to see what's planned or request a new one!
```

### 4. Offer Next Steps

End with:

```
---

Want me to help you set up an integration, create a new skill, or learn more about what I can do?

Otherwise, hit **Esc** to get back to work.
```

Wait for the user to respond or exit.
