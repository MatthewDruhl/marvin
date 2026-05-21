# MARVIN Privacy and Data Boundaries

MARVIN is a personal operations workspace. Treat it as private by default, but keep the git repository limited to reusable instructions, examples, sanitized notes, and non-sensitive project artifacts.

This file is the boundary rulebook for personal data, job-search data, contacts, transcripts, credentials, screenshots, CSVs, and external integrations.

## Storage Rules

| Data class | Allowed in this repo | Keep outside this repo |
| --- | --- | --- |
| Runtime instructions | `CLAUDE.md`, `AGENTS.md` if present, `.claude/commands/`, `skills/*/SKILL.md` | Global runtime preferences that are not project-specific |
| MARVIN state | Example schemas and sanitized fixtures | Live `state/`, `sessions/`, local caches, generated scorecards with private context |
| Job applications | Sanitized examples in `content/jobs/*.example` | Live applications, opportunities, interview prep, company research, salary analysis, match scores |
| Job research | Search strings and generic process notes | `~/Resume/jobs/research/` output, personal evaluation data, job-specific scoring |
| Contacts | Sanitized examples only | Live contacts, recruiter notes, networking history, private follow-ups |
| TWC records | Scripts, tests, README files | Generated weekly CSVs, submitted PDFs, exports containing application history |
| Transcripts | Redacted excerpts when needed for documentation | Raw meeting transcripts, voice transcriptions, call notes, client recordings |
| Freelance/client files | Sanitized summaries or public portfolio artifacts | NDAs, source spreadsheets, client data, meeting notes, private deliverables |
| Credentials | `.env.example`, setup docs with placeholder values | `.env`, OAuth client secrets, token stores, MCP credentials, cookies, API keys |
| Screenshots/images | Redacted screenshots that do not expose private data | Screenshots containing inboxes, calendars, contacts, job records, credentials, client data |

## Job-Search Boundaries

Use `~/Resume/jobs/` for live job-search data:

- `~/Resume/jobs/applications.md` - active applications and statuses.
- `~/Resume/jobs/opportunities.md` - roles to research or apply for.
- `~/Resume/jobs/interview-prep/` - interview prep, company notes, mock sessions.
- `~/Resume/jobs/research/` - job posting analysis, match scorecards, salary context, and search-session summaries.

Use `content/jobs/` only for reusable or sanitized repo material:

- `content/jobs/*.example` - examples safe to commit.
- `content/jobs/search-strings.md` - generic search strings.
- `content/jobs/TWC/` - tracker scripts, tests, and documentation.

Do not commit live job records, personal fit evaluations, salary notes, recruiter conversations, or weekly TWC CSV/PDF exports.

## Contacts and Transcripts

Contacts, meeting transcripts, call notes, and voice transcriptions often include private names, phone numbers, email addresses, business context, client decisions, or confidential project details.

Rules:

- Keep live contacts outside the repo unless they are intentionally sanitized examples.
- Keep raw transcripts outside the repo.
- Commit only summaries that are redacted enough to stand alone in public.
- Remove names, email addresses, phone numbers, addresses, account IDs, meeting links, and client-confidential details unless there is an explicit reason to preserve them.
- When a transcript is useful for future work, store a sanitized summary and link to the private source path without copying the source text.

## Credentials and Integrations

Credential material must stay out of git:

- `.env`
- OAuth client secrets
- OAuth token stores such as `.google-workspace-credentials/`
- Slack bot tokens
- MCP credential files
- cookies, session stores, exported browser auth, and service-account keys

Integration docs may include placeholder values and setup commands, but not real IDs, secrets, tokens, refresh tokens, or account-specific credential JSON.

For external integrations:

1. Confirm whether the integration can read private data, write external state, or notify other people.
2. Store credentials in ignored local files only.
3. Prefer least-privilege scopes.
4. Document destructive or externally visible actions.
5. Require human confirmation before sending emails, posting messages, modifying calendars, deleting records, or uploading private files.

## Redaction Rules

Before committing examples, screenshots, CSVs, or exported artifacts:

- Replace personal names with role labels such as `Candidate`, `Recruiter`, or `Client`.
- Replace companies with generic names unless the company is already public and intentionally relevant.
- Replace emails, phone numbers, URLs with private tokens, addresses, IDs, and account numbers with placeholders.
- Remove calendar details, meeting links, attendee lists, inbox previews, and message snippets.
- Remove salary expectations, personal evaluations, negotiation notes, and application outcomes unless explicitly sanitized.
- For CSVs, keep only fake rows or aggregate counts.
- For screenshots, crop or blur private fields before adding them to the repo.

If a file cannot be safely redacted quickly, do not commit it.

## Privacy Preflight Checklist

Run this checklist before adding a new integration, importing content, or committing generated artifacts:

- Is this reusable repo material, or live personal/client data?
- Does it include credentials, tokens, OAuth data, cookies, or service-account JSON?
- Does it include names, emails, phone numbers, addresses, meeting links, or account IDs?
- Does it include job-search evaluations, recruiter notes, salary data, TWC records, or application history?
- Does it include raw transcripts, voice recordings, client spreadsheets, NDAs, or private deliverables?
- Is the file covered by `.gitignore` if it should remain local?
- If it is an example, are all rows and screenshots synthetic or redacted?
- Would it be acceptable if this exact file were pushed to GitHub?

Stop and move the file outside the repo, or redact it, if any answer is uncertain.

## Gitignore Coverage

`.gitignore` should block local state, sessions, credentials, generated TWC exports, live job files, raw transcripts, and private import folders. Gitignore does not protect files already tracked by git, so tracked private files require an explicit migration or removal plan before they are safe.

Use `git status --short` before committing and inspect all untracked files. Treat unfamiliar untracked files as private until proven otherwise.
