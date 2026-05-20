# Meeting Summary: Kinze Vibe Coding Governance & IT Strategy

**Date:** May 18, 2026, 10:04 AM
**Duration:** ~1 hour 45 minutes
**Location:** On-site at Kinze

**Attendees:**
- **Doug** -- IT/Development lead at Kinze (30+ years dev experience, C#/.NET/Azure DevOps, currently vibe coding a parts manual lookup app with PDF ingestion and RAG)
- **Matt** -- External consultant/freelancer (uses Claude Code, Python, AWS serverless)
- **Steve** -- Security/infrastructure person at Kinze (handles vulnerability analysis, references North Liberty environment)
- **Gary** -- IT management at Kinze (focuses on business case, ROI, risk, governance; references an "AI council")

Other names referenced: Ryan, Stacy, J, Elliot

---

## Key Topics Discussed

### 1. Vibe Coding Governance and Hardening Process

The most pressing concern: how to allow "vibe coding" (non-developers using AI to build apps) at speed while keeping things secure, integrated, and supportable.

- Vibe coded projects should be treated as proof of concepts requiring a hardening process before production
- Non-developer vibe coders should become stakeholders once a project enters the IT portfolio, not ongoing developers

### 2. Security and Data Protection

- Proprietary secrets must not be fed into AI tools (risk of data leaking through LLMs)
- Use scrubbed/dummy databases for development rather than giving vibe coders production data access
- Kinze already has good protections: users have read-only access to most databases, no direct write access except through applications. Financial data further restricted.
- MCP (Model Context Protocol) proposed as a layer for permissions and role-based access for AI-assisted development
- Discussion of whether AI can replace a $13,000 static vulnerability code analysis tool. Consensus: ask multiple AIs, but security spending is justified given breach costs.

### 3. Token Management and Cost Control

- Controlling which AI model users hit (Opus vs. Sonnet) directly affects token costs
- Suggestion: give users the $20 plan with built-in limits, letting natural constraints teach efficient prompting
- Non-developers will use more tokens than developers due to less efficient prompting
- Education and prompt engineering training as the primary token management strategy

### 4. Tech Stack Standardization

- **Current stack:** C#, .NET, Azure DevOps. North Liberty facility uses C++ with local Git.
- **Transitioning to:** PostgreSQL (licensing reasons), Angular/Node.js for front-end, .NET Core for back-end
- Need to define and communicate a standard tech stack so vibe-coded apps can be supported by IT
- Docker containers proposed for deployment standardization
- VS Code preferred over Cursor due to cost and model flexibility

### 5. CI/CD and Code Review Process

- Implement GitHub Actions for linting, code review, and security checks on PRs (not individual commits)
- Automated CI checks should block merging when security issues are found
- Human review only when a vibe coder presents a functional POC
- Keep PRs small. Educate vibe coders on commit/branch/PR workflow.
- CLAUDE.md files can encode project-specific rules that AI follows during development

### 6. Workflow and Development Environments

- Kinze has dev/test environments but users rarely test there. Need to revive staging/test workflows.
- Consider a separate GitHub repository for vibe coding activity (separate from Azure DevOps)
- "Start small, let it grow" approach rather than denying everything

### 7. Tools and Platform Discussion

- Tools in use or under evaluation: Claude Code, Perplexity, Kodex (OpenAI), Copilot (North Liberty), VS Code
- Claude Code CLI preferred over in-editor chat for better context management
- Obsidian used for knowledge management/visualization linked to AI assistant workspace
- Matt demonstrated his Marvin AI assistant setup with stacked CLAUDE.md files, memory management, and Obsidian vault integration

---

## Decisions Made

1. **Tech stack needs to be formally defined and communicated** to vibe coders before they start building. Already on the AI council agenda.
2. **Request/proposal process** will be created for vibe coding projects (business case required before token spend).
3. **MCP approach** endorsed for controlling database access. Two endpoints: one for development (scrubbed data), one for production.
4. **CI pipeline with automated checks** will be implemented in the vibe coding repository.
5. **$20 plan** as the baseline for general vibe coders. IT core team may get higher-tier access.
6. **No IT review of vibe code projects** until they reach a functional POC stage with passing tests.

---

## Action Items / Next Steps

1. **AI Council meeting** later in the week to discuss tech stack decisions (already on agenda)
2. **Define the approved tech stack** and communicate to vibe coders (PostgreSQL, Angular/Node.js, .NET Core, Docker)
3. **Set up a GitHub repository** with GitHub Actions CI/CD for vibe coding projects, separate from Azure DevOps
4. **Develop the MCP layer** for controlled database access with role-based permissions and scrubbed data
5. **Create onboarding/education materials** for vibe coders: Git workflow, prompting best practices, tech stack requirements, security rules
6. **Doug:** Revisit PDF ingestion/RAG testing. Start smaller, build up incrementally, consider asking Claude for alternative architectures.
7. **Matt:** Continue working with Ryan. Plans to test Codex. Iterate on the harden skill.

---

## Important Context

- Kinze is a manufacturing company with facilities in at least two locations (main site and North Liberty)
- The company has an **AI council** that governs AI tool adoption
- Strong emphasis on **not being a roadblock** to innovation while managing risk. IT explicitly wants to enable ideas, not block them.
- Business continuity concern: if a vibe coder leaves, IT inherits an unsupported app. Standardizing the tech stack and requiring proper documentation/testing mitigates this.
- A "levels" concept was referenced multiple times (e.g., "level 4"), suggesting a maturity model for vibe coding governance discussed previously.
