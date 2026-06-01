---
name: extract-specs
description: |
  Extract structured requirements from raw inputs (meeting transcripts, client docs,
  emails, notes). Produces a requirements brief that feeds into /write-a-prd.
  Use when user has raw source material and needs to pull out what was agreed on.
license: MIT
compatibility: marvin
metadata:
  marvin-category: development
  user-invocable: true
  slash-command: /extract-specs
  model: default
  proactive: false
---

# Extract Specs

Turn raw, unstructured inputs into structured requirements.

## When to Use

- User has meeting transcripts, client docs, emails, or notes
- User wants to pull requirements from source material before writing a PRD
- User says "extract specs from..." or "what did we agree on in that meeting"

## Inputs

User provides one or more of:
- Meeting transcript files (text, markdown)
- Client documents (PDFs, docs, markdown)
- Email threads (via Gmail MCP or pasted)
- Handwritten notes or summaries
- Prior session logs

If the user doesn't specify files, ask: "What source material should I work from?"

## Process

### Step 1: Identify Project and Ingest Source Material

1. Ask the user which project this is for. Look it up in `state/projects.md` to get the repo and path. If the project isn't registered, ask if they want to add it.
2. Read every file the user provides. Do not skim. Do not summarize before analyzing.
2. For each source, note:
   - Who said what (attribute statements to people)
   - What was the date/context of the source
   - What type of source it is (meeting, email, doc)

### Step 2: Extract Raw Requirements

Pull out everything that looks like a requirement, request, decision, or constraint.
For each item, capture:

- **What:** the requirement or request in plain language
- **Who:** who asked for it or agreed to it
- **Source:** which document, which section or timestamp
- **Type:** one of: feature, constraint, integration, workflow, UI/UX, data, security
- **Confidence:** explicit (directly stated) or inferred (implied but not said)

**Rules:**
- Quote the source material when attributing. Do not paraphrase away specificity.
- If two sources contradict each other, flag the conflict. Do not resolve it silently.
- If something is ambiguous, mark it as ambiguous. Do not interpret.
- Separate what was AGREED from what was DISCUSSED. Discussion is not a decision.

### Step 3: Identify Gaps

After extraction, list what's missing:
- Requirements mentioned but not detailed
- Decisions deferred or unresolved
- Questions that were asked but not answered
- Areas where no requirements exist but probably should (auth, error handling, etc.)

### Step 4: Present the Requirements Brief

Show the user the extracted requirements grouped by type:

```markdown
# Requirements Brief

**Sources analyzed:**
- <file> (<type>, <date>)
- <file> (<type>, <date>)

## Agreed Requirements
| # | Requirement | Who | Source | Type | Confidence |
|---|-------------|-----|--------|------|------------|
| 1 | <what>      | <who> | <source:section> | feature | explicit |
| 2 | <what>      | <who> | <source:section> | constraint | inferred |

## Conflicts
- <source A> says X, but <source B> says Y. Needs resolution.

## Gaps
- No discussion of <topic>. Needs input.
- <person> asked about <thing> but no answer was recorded.

## Open Questions
1. <question that needs answering before PRD>
```

### Step 5: Iterate with User

Ask the user:
1. Are any of these wrong? (misheard, misattributed, taken out of context)
2. Can you resolve any of the conflicts?
3. Can you fill any of the gaps?
4. Are there requirements you know about that aren't in the source material?

Update the brief based on answers. Repeat until the user says it's complete.

### Step 6: Save and Handoff

1. Save the final requirements brief to the project's folder (from `state/projects.md`):
   `<project-path>/requirements-brief-<YYYY-MM-DD>.md`
2. Tell the user: "Requirements brief saved. Run `/write-a-prd` to turn this
   into a structured PRD. The brief will be used as input."

## What This Skill Does NOT Do

- Write the PRD (that's `/write-a-prd`)
- Make design decisions (that's the user + `/grill-me`)
- Create issues (that's `/prd-to-issues`)
- Resolve ambiguity silently (it flags and asks)

---

*Skill created: 2026-05-28*
