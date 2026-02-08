# AWS Recipe Book App

Last updated: 2026-02-07

---

## Overview
Recipe CRUD app with image uploads, search, favorites, and AI recipe extraction from photos.

## Status
Phase 1 API COMPLETE (worked with Claude Code on Feb 3)

## Tech Stack
- **Local:** Python FastAPI + React + SQLite
- **AWS:** Serverless (Lambda, DynamoDB, S3, Bedrock)
- **Cost:** $0/month for 5 users (free tier), AI extraction ~$0.003/image
- **AI Feature:** Extract recipes from photos using AWS Bedrock (Claude 3.5 Sonnet vision)
- **Approach:** Build locally first, deploy to AWS when ready

## Documentation
- `content/recipe-app/Recipe-Book-Master-Spec.md` - Complete spec (982 lines, includes SAM template, pyproject.toml, all routes, DynamoDB/S3/Bedrock services, JWT auth)
- Note: Design docs referenced in older sessions may have been in other workspaces

## Next Steps
Continue implementation phases beyond Phase 1 API
