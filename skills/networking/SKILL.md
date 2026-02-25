---
name: networking
description: |
  Lightweight CRM for managing professional contacts. Track interaction history,
  schedule follow-ups, and maintain relationships. Integrates with daily briefing
  to surface contacts due for follow-up.
license: MIT
compatibility: marvin
metadata:
  marvin-category: career
  user-invocable: false
  slash-command: null
  model: default
  proactive: true
---

# Networking & Contact CRM

Manage professional contacts and follow-up reminders.

## When to Use

- User says "add contact: [name] at [company]"
- User says "log interaction with [name]"
- User says "when should I follow up with [name]?"
- User asks "who should I follow up with?"
- During daily briefing (surface contacts due for follow-up)
- After an interview or networking event

## Process

### Step 1: Identify Action
- **Add contact** → Create new entry in contacts.md
- **Log interaction** → Update interaction history and last interaction date
- **Set follow-up** → Set or update follow-up date
- **Check follow-ups** → List contacts due for follow-up
- **Update relationship** → Change relationship strength level

### Step 2: Read Current State
Read `content/jobs/contacts.md` for current contact data.

### Step 3: Execute Action

For adding a contact:
1. Gather: name, company, email, role, context
2. Set relationship level based on how you met
3. Add interaction history entry
4. Set follow-up date (default: 2 weeks)
5. Add to contacts.md

For logging interaction:
1. Find contact in contacts.md
2. Add entry to Interaction History
3. Update Last Interaction date
4. Adjust relationship strength if appropriate
5. Set next follow-up date

### Step 4: Update File
Write changes to `content/jobs/contacts.md`.

### Step 5: Confirm
```
Updated: [Name] at [Company]
Last interaction: [date]
Next follow-up: [date]
Relationship: [level]
```

## Briefing Integration

When called from daily briefing:
```
**Networking Follow-ups:**
- [Name] at [Company] — follow-up due [date] ([N] days overdue)
- [Name] at [Company] — follow-up due today
```

Only show contacts with follow-up dates that are today or overdue.

## Notes
- Keep interaction history concise but complete
- Relationship strength helps prioritize follow-ups
- Integrate with Gmail for email follow-ups
- After interviews, always prompt to log the interaction

---

*Skill created: 2026-02-08*
