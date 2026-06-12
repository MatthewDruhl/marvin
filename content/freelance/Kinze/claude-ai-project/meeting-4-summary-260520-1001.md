# Meeting Summary: Kinze North Liberty Software Team - AI Tools & Workflows

**Date:** May 20, 2026, 10:01 AM
**Duration:** ~1 hour 40 minutes
**Location:** On-site at Kinze (North Liberty facility)

**Attendees:**
- **Matt (Speaker 1)** -- External AI consultant/freelancer (Pearson background, Claude Code, Python, AWS)
- **Michael Ayler (Speaker 2)** -- North Liberty team lead (8 years at Kinze, CS background, previously at Intermec doing embedded/hardware, then Trapeze doing control systems for buses)
- **Jason (Speaker 3)** -- Software team lead, embedded and cloud connected teams (16 years at Intermec, 11 years at Kinze, built systems from scratch)
- **Jordan (Speaker 5)** -- Software developer, front-end Android app (10 years at Kinze)
- **Matt H. (Speaker 6)** -- Software engineer, embedded team under Jason (previously at Intermec)
- **Ryan (Speaker 7)** -- Leads UI and automated test teams (11 years at Kinze, previously at Intermec)
- **Gary (Speaker 8)** -- AI role, previously product management and mechanical side (11 years at Kinze)

Other names referenced: Doug (Williamsburg IT), Zach (marketing, agent builder), Brad, Jeff, Stacy

---

## Key Topics Discussed

### 1. Matt's Background & Current Projects

Matt shared his background: software developer since 1997, started at ACT, then 25 years at Pearson (ERP systems, server management, AWS since 2015, hybrid cloud solutions). Currently freelancing:
- **YPS (St. Louis)** -- Automating email responses for a parts sourcing company. Set up draft-and-approve workflow, training AI on company voice/tone. Building database backend and follow-up email/text automation.
- **DND project** -- Personal AI dungeon master game with Python mechanics (character sheets, dice engine, inventory validation), AI running campaigns, 500+ tests, running on AWS Lambda/serverless.
- Connected with Kinze through Dr. Beach (optometrist), who mentioned AI work to Matt's wife Emily.

### 2. AI Evaluation & Adoption (Pearson Experience)

Matt described Pearson's AI rollout process:
- Started with a small pilot group evaluating multiple tools
- Some testers ran two AI tools simultaneously for comparison
- Weekly feedback sessions on usability and setup experience
- Evaluated across multiple IDEs (VS Code, JetBrains, etc.)
- Chose Copilot (at the time, mostly code completion, not agentic)
- Measured usefulness by developer perception, not lines of code generated
- Key insight: usefulness is subjective and varies by developer skill level

### 3. Token Management & Efficiency Metrics

Extended discussion on measuring AI effectiveness:
- Token usage is not a flat metric. Different skill levels consume differently.
- A beginner might spend $2000 in tokens to do what an experienced developer can prompt in $20
- Senior developers use AI to go higher, not to replace existing skills
- The human is the bottleneck, not the AI. Code review and PR approval still require human judgment.
- Quality vs. speed tradeoff: generating code fast burns tokens but may reduce quality
- Matt's approach: work 1-2 issues per PR, review each diff, rather than batch 25 issues into one massive PR

### 4. North Liberty's Development Process

Ryan and Jason described their mature CI/CD pipeline:
- Features come in as multi-year roadmap items, broken into 2-20 hour Jira tasks
- Commits go through Gerrit code review system
- Automated analyzers validate code before human review (build verification, coding standards)
- Continuous integration with overnight builds
- ~2000 automated tests running on simulated planters
- Defects generate new Jira issues automatically
- Bi-weekly releases to field test teams, annual customer releases
- Built entirely from scratch by the current team (no inherited code, no inherited processes)
- Team philosophy: "agile in the true meaning. Do what helps, get rid of the rest."

### 5. Current AI Usage at North Liberty

The team is using Copilot with Claude (Sonnet primarily, Opus for harder problems) through VS Code and Android Studio:
- **Code generation** -- Agent mode primarily, some use Ask mode for exploratory questions
- **Debugging** -- Feeding subsystem context and symptoms, AI sometimes pinpoints bugs immediately
- **Localization** -- First big AI win. 7 languages (English + 6). Previously outsourced to translation houses at high cost with 6-month turnaround. Now done at development time with AI, verified by dealers. Error rate dropped from ~60% to ~5%.
- **Documentation** -- Light usage. Generated a Wiki page from code analysis. Team is lean on documentation by design.
- **Embedded/kernel code** -- Less useful. Custom hardware and Linux kernel modifications still mostly manual.
- Code generated vs. hand-typed: shifting, but production code that's fully AI-generated is still "fairly low." Hand typing is declining.
- Jason burned his monthly Opus token allotment by the 19th. Jordan burned through 15X tokens in 2 days.

### 6. Williamsburg AI Usage (Gary's Report)

Gary described broader company AI adoption:
- **Doug** -- Building business applications (quoting tool, parts manual lookup with RAG/PDF ingestion)
- **Zach (Marketing)** -- ~10-15 ChatGPT agents. Lead validation using public government subsidy data cross-referenced with social media leads. Knowledge base agent ("ZackGPT") for marketing ideation. Image generation for advertisements (80% AI, 20% finishing). Brand name stress testing across languages (e.g., "Kinze" sounds like "kinza" = cilantro in Russian).
- **Accounting** -- Using AI for Excel formula creation, troubleshooting, Power Query self-teaching. Had data privacy concerns about putting financial data in chat.
- **Service** -- Planning a customer-facing knowledge base agent. Two data pools: operator/user manuals + historical service call resolutions. Goal: deflect basic support calls before they reach the service team.
- **Design Engineering & Manufacturing** -- Using AI for document review and revision comparison (e.g., harness revision A vs. B, checking for unintended changes). Active tool in development.

### 7. Shared Knowledge Base & Cross-Team Context

Major discussion on breaking out of individual AI silos:
- Matt H. asked: can we share AI context across team members so one person can ask "why did Jordan make that change?"
- Matt explained: sessions are individual, but you can publish learned knowledge to a shared wiki/database
- Jason noted: they already have rich data (Jira links in commits, git blame, Gerrit history). AI could consume all of it.
- The team wants AI to have access to Jira, wiki, and code review history without requiring an extra publishing step
- Jira has an API. Jason noted they've already written scripts to interact with it. No need to pay for Jira's built-in AI.
- Consensus: the data is already structured and available. Low-hanging fruit to connect AI to it.

### 8. Tool Consolidation & SSO

Matt H. asked about unifying the AI experience across Kinze accounts:
- Currently: separate GitHub Copilot, Office 365 Copilot, ChatGPT Pro accounts
- Gary: no plan to consolidate to one tool. Different tools are better at different things (ChatGPT for images, Claude for code).
- SSO federation with AI tools is possible but complex. Pearson took years. Kinze IT hasn't federated Jira yet.
- Key concern: user-based permissions through LLMs (e.g., accounting data shouldn't be accessible to engineering through the LLM)
- Guardrails will focus on data security and system continuity, not restricting usage

### 9. CLI vs. IDE AI Usage

Matt advocated for Claude Code CLI over VS Code integration:
- Different persona/behavior in CLI vs. IDE
- Larger context window in CLI (less overhead)
- Persistent assistant with session memory across weeks
- CLAUDE.md files for project-specific instructions
- Team hasn't tried CLI approach yet. Jason noted VS Code/Android Studio integration has been "good enough" so far.

### 10. Practical Tips Shared

- Keep CLAUDE.md files around 300 lines max
- Check for duplicate/conflicting information across memory, CLAUDE.md, and other config files
- Use voice input for documenting processes (talk through workflows, AI transcribes and structures)
- Back up agents to version control (Zach's ChatGPT agents are in his personal account, not company-owned GitHub)
- API keys in chat: AI will display them. Need education on .env files and secret management.
- Code review pricing changes coming mid-June (Claude in GitHub will use API tokens, not subscription)

---

## Decisions Made

1. **No major process changes needed** -- North Liberty's existing CI/CD pipeline is solid. Focus on incremental AI improvements.
2. **Shared knowledge base is low-hanging fruit** -- Team already has structured data in Jira, Gerrit, and wikis. Connecting AI to these systems is the next logical step.
3. **Multiple AI tools will continue** -- No plan to consolidate to a single tool. Right tool for the right job.
4. **Guardrails coming** -- Data security and supported language requirements, not usage restrictions.

---

## Action Items / Next Steps

1. **Explore shared knowledge base** -- Connect AI tools to existing Jira, wiki, and Gerrit data so team members can query cross-team context
2. **Evaluate Gerrit AI code review plugin** -- Jason noted plugins now available. Consider cost/benefit (token usage vs. value of automated review step)
3. **Gary:** Meet with accounting team (scheduled for tomorrow) to understand their AI usage and concerns
4. **Service agent development** -- Continue building the customer-facing knowledge base combining operator manuals + service call history
5. **Zach's agents** -- Get his ChatGPT agents backed up into company-owned GitHub
6. **Matt:** Continue consulting. Consider demonstrating CLI workflow to team in future session.
7. **Token management** -- Monitor Opus usage. Team members hitting monthly limits. Consider adjusting model selection strategy (Sonnet for code, Opus for architecture/debugging only).
