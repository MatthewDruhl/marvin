# Meeting Summary: Kinze AI Consulting Session #2

**Date:** May 18, 2026, 1:15 PM
**Attendees:** Matt (external AI consultant), Zach (Kinze marketing), Gary (engineering/product leader)
**Company:** Kinze Manufacturing (agricultural equipment: planters, row units, hydraulic doors)

---

## Key Topics Discussed

### 1. Zach's Current AI Usage (ChatGPT Custom GPTs)

Zach walked through his library of custom GPT agents built within ChatGPT Enterprise:

- **Kinsey Insights** -- Core knowledge agent trained on operator manuals and marketing literature. Mimics brand voice. Used for copywriting, social media (planned 3 months of posts), and web copy. A simplified version is being deployed on Copilot for new sales managers.
- **Zach GPT** -- Personal AI assistant that helps write and refine prompts.
- **Kinsey Web Troubleshooter** -- Helps manage WordPress site (Bluehost, custom CSS). Used during a server migration and a Bluehost cyber attack.
- **Marketing Strategist** -- Campaign planning and ad tactics.
- **HubSpot Operations Advisor** -- New agent, backfilling for retiring colleague (Scott) who managed HubSpot.
- **Other agents:** VR Specialist, Event Planner, Ag Market Analyst, Dealer Due Diligence (BBB/bankruptcy/arrest checks via Deep Research), Vendor Due Diligence (evaluated Market Pilot software), Operator Support Assistants (trained on operator manuals, parts lookup planned), Video Production Assistant ("Quinton GPTino"), Lead Vetting Data Intelligence, Hydraulic Door Specialist.

### 2. Lead Vetting with Python Scripts (EWG & UCC Data Matching)

A major discussion topic. Zach built Python scripts (run in Google Colab) that:

- Export leads from HubSpot CRM as Excel
- Match against EWG (Environmental Working Group) subsidy data (~80,000+ rows, 2022-2025) to determine if leads are real farmers and estimate acreage
- Match against UCC (Uniform Commercial Code) financial data (from AEM) to see if leads have financed planters, what brand, new vs. used
- Uses fuzzy matching (handles Dan vs. Daniel, etc.)
- Previously took weeks manually. The script does it in ~13 minutes.
- Jamie handles scraping/downloading the government subsidy data.

### 3. Digital Advertising Strategy

- Meta (Facebook/Instagram) is their primary lead generation channel
- Carousels on Meta drive many leads
- Hydraulic door ad campaign: initially targeted corn belt (Iowa, Illinois) but saw ad fatigue. Shifted to West/Alaska/Florida with strong results.
- Kinsey Insights handles much of the ad copywriting
- Ad creation is mostly manual (Zach writing copy + Adobe Express templates)

### 4. Interactive 3D Row Unit on Website

Zach built an interactive 3D model viewer embedded on WordPress:
- SolidWorks engineering file -> Cinema 4D -> GLB export
- Used Google's Model Viewer as base, customized with ChatGPT
- Added interactive hotspots for key features
- Tech stack: HTML5, CSS, JavaScript in WordPress

---

## Decisions Made

No major formal decisions. This was primarily a consulting/advisory session with Matt reviewing Zach's current AI setup and providing recommendations.

---

## Action Items / Next Steps

1. **Back up custom GPT agents** -- Matt strongly recommended backing up all ChatGPT custom GPTs (system prompts, knowledge files, configs). None are currently backed up. Suggested weekly backups, potentially in GitHub.

2. **Use competing AIs for agent improvement** -- Take each custom GPT and have a different AI (Claude or fresh ChatGPT) review and suggest improvements. Evaluate suggestions critically.

3. **AI-powered ad performance analysis** -- Have AI analyze ad performance data (Meta, Google Search Console) weekly to generate start-of-week reports. Could begin with manual copy-paste rather than direct HubSpot integration.

4. **Google AI Overview / Search Console analysis** -- Zach wants to better analyze presence in Google's AI Overviews for Kinze planter model searches.

5. **Automate lead vetting pipeline (agentic AI)** -- Long-term goal: leads enter HubSpot, automatically run through Python matching scripts, results populate back into HubSpot. Blocker: approval from "Steve" (IT/security) for AI access to HubSpot. Interim solutions discussed:
   - Weekly HubSpot data export via script, matching in sandboxed environment
   - Docker container to isolate Python scripts
   - MCP (Model Context Protocol) layer in front of the data
   - Simple NoSQL database instead of spreadsheets

6. **Evaluate Claude access** -- Zach doesn't have Claude yet. Plan: get access and compare with ChatGPT over 1-2 months. Claude may outperform in non-visual areas; ChatGPT likely better for photo/video.

7. **Video/audio sync automation** -- Zach's 4K raw file syncing with audio is time-consuming. Matt advised Claude isn't the right tool. Recommended dedicated software (PluralEyes, ~$100/year). Buy rather than build.

8. **Connect agents into agentic workflow** -- Zach's vision: chain Zach GPT -> Marketing Strategist -> Kinsey Insights -> auto-build ads and schedule posts. Aspirational, not yet implemented.

---

## Important Context

- **Team size:** Marketing team is 3, going down to 2 (Scott retiring). AI is filling gaps from departed copywriters and designers.
- **Security concerns:** Internal roadblocks from IT/security about letting AI access HubSpot directly. ChatGPT Enterprise agreement says data isn't shared, but trust gap remains.
- **AI Summit takeaways:** Zach attended an AI summit. Key topics: multimodal AI, agentic AI. Saw software solutions but felt they could build their own.
- **AI platform landscape:** OpenAI/ChatGPT and Anthropic/Claude viewed as dominant. Copilot adequate for code assist only. Adobe AI rated worse than ChatGPT for imaging. Grok and Gemini dismissed for serious work.
- **Hydraulic doors** are a newer business line being actively marketed to aviation and large-door markets nationally.
