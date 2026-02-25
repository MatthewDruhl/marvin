---
name: learning-journal
description: |
  Capture coding learnings, patterns, and insights during sessions. Creates a
  searchable knowledge base with concepts, code snippets, sources, and tags.
  Syncs to Obsidian Learning/ folder.
license: MIT
compatibility: marvin
metadata:
  marvin-category: learning
  user-invocable: false
  slash-command: null
  model: default
  proactive: true
---

# Code Learning Journal

Capture and organize what you learn during coding sessions.

## When to Use

- User says "TIL..." or "Today I learned..."
- User says "learned that..." or "note this pattern..."
- User says "add to journal: ..."
- User asks "what did I learn about [topic]?"
- User says "search journal for [keyword]"

## Process

### Step 1: Capture Entry
Extract from user's message:
- **Concept:** What was learned (brief title)
- **Details:** Explanation of the concept
- **Code snippet:** If applicable
- **Source:** Where it came from (project, tutorial, docs, etc.)
- **Tags:** Relevant tags (python, dsa, fastapi, docker, sql, etc.)
- **Date:** Today's date

### Step 2: Format Entry
```markdown
### [Concept Title]
**Date:** YYYY-MM-DD | **Tags:** #tag1 #tag2 | **Source:** [source]

[Details/explanation]

```[language]
[code snippet if applicable]
```

---
```

### Step 3: Add to Journal
Append the entry to `content/learning-journal.md` under "## Entries".

### Step 4: Update Tags Index
Add any new tags to the Tags Index section at the bottom.

### Step 5: Confirm
```
📝 Logged: [Concept Title]
Tags: #tag1 #tag2
```

## Search Process

When user searches:
1. Read `content/learning-journal.md`
2. Search for keyword in titles, details, tags, and code
3. Return matching entries
4. If no matches, suggest related tags

## Notes
- Entries are appended chronologically
- Tags use # prefix for Obsidian compatibility
- Code snippets include language for syntax highlighting
- Journal syncs to Obsidian Learning/ folder as individual notes
- Keep entries concise — focus on the key insight

---

*Skill created: 2026-02-08*
