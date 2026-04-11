---
name: pmp-intake
description: |
  Interactive Q&A interview to gather everything needed for a PMI PMP certification application.
  Asks questions one section at a time, tracks progress toward the month requirement,
  and saves answers directly to the person's profile.md.
  Invoke: /pmp-intake <name> (Matt or Emily)
license: MIT
compatibility: marvin
metadata:
  marvin-category: pmp
  user-invocable: true
  slash-command: /pmp-intake
  model: default
---

# PMP Intake Interview

Gather all data needed for a PMI PMP application through a conversational Q&A session.
Saves answers to `pmp/ApplicationProcess/{person}/profile.md`.

## Invocation

- `/pmp-intake matt` — intake for Matt
- `/pmp-intake emily` — intake for Emily
- `/pmp-intake` (no name) — ask who this is for

Name matching is case-insensitive. Profile files are at:
- `pmp/ApplicationProcess/matt/profile.md`
- `pmp/ApplicationProcess/emily/profile.md`

---

## Behavior

Ask **one question at a time**. Wait for the answer before asking the next.
Do not dump a list of questions at once — this is a conversation, not a form.

After each answer, briefly confirm what you heard before continuing.

Allow the user to say **"skip"** on any question — mark it as `⬜ To fill in` in the profile.
Allow the user to say **"stop"** at any time — save progress and summarize what's left.

---

## Interview Flow

### Step 0 — Load Existing Profile

Before starting, read the person's `profile.md`.
If it already has data, show a summary of what's complete and what's missing.
Ask: "Want to continue where you left off, or start fresh?"

---

### Phase 1 — Education

Ask these in order:

1. **Degree level:** "What is your highest level of education — bachelor's, master's, associate, or high school diploma?"
   - Bachelor's or higher → requirement = **36 months**
   - Associate or HS → requirement = **60 months**
   - Announce: "You'll need to show [X] months of project management experience."

2. **Institution:** "What school did you attend for that degree?"

3. **Field of study:** "What was your field of study or major?"

4. **Graduation year:** "What year did you graduate?"

5. **Degree copy:** "Do you have a digital copy of your degree saved somewhere? (yes/no/not sure)"

---

### Phase 2 — 35 Contact Hours

5. **Certificate status:** "Do you have a 35-hour PMP prep course certificate?"
   - If **yes**: Ask course name, provider, completion date.
   - If **no**: "You'll need to complete a PMI-approved 35-hour course before applying. Have you started one, or are you still looking for one?"
     - Note the status and move on.

---

### Phase 3 — Project Experience

Introduce this phase:
> "Now let's capture your project experience. PMI needs [X] months total. I'll ask about each project and track our running total.
> Tip: Fewer projects with longer durations is simpler. One 3-year project is better than six 6-month ones."

For each project, ask these fields one at a time:

**Project basics:**
1. "What would you call this project? (Give it a short title)"
2. "What company or organization was this for?"
3. "What was your job title at the time?"
4. "Which department or functional area were you in? (e.g., IT, Operations, Marketing, Finance)"
5. "What industry is that company in? (e.g., Technology, Healthcare, Finance, Retail)"
6. "Was this project run using a Traditional (waterfall), Agile, or Hybrid approach?"
7. "How big was the project team? (1–4, 5–10, 11–20, or 20+)"
8. "What was the approximate project budget? (or say 'classified' if you'd rather not share)"
9. "When did this project start? (Month and year)"
10. "When did it end? (Month and year, or 'still in progress')"
11. "Who could verify this project if PMI audits you? (Name and title of a manager or colleague from that org)"

**After basics — show running total:**
> "That adds [N] months. Running total: [X] of [required] months."

If requirement is already met:
> "You've hit your [X]-month requirement! You can add more projects if you want, but you don't need to."

**Description content (for each project):**
> "Now a few questions so we can draft the project description later. These are the 5 sections PMI requires."

12. "In one or two sentences: what was the **objective** of this project? (What problem were you trying to solve or what were you trying to build?)"
13. "In one or two sentences: what was the **outcome**? (What happened when the project was done?)"
14. "Walk me through the **PM work you did** — what did you do to initiate, plan, execute, and close this project? Don't worry about PMBOK language yet, just tell me in plain English what you actually did."
15. "What were the **deliverables** — the tangible things that came out of this project?"

After all 5 description fields are captured, say:
> "Got it. I can generate a draft description for this project when you're ready — it'll translate your answers into PMBOK language (200–400 words). Want me to draft it now or continue gathering projects first?"

**Offer to add another project:**
> "Want to add another project? (You need [remaining] more months)"

Repeat until requirement is met or user says stop.

---

### Phase 4 — Audit Prep

After all projects are captured:

> "Last section — audit prep. About 10% of applicants get audited. Let's make sure you're ready."

1. "Have you given a heads-up to the contact person for each project that they might be asked to sign a verification form? (yes/no/not yet)"
2. "Do you have a digital copy of your degree ready to send? (yes/no)"
3. "Do you have a digital copy of your 35-hour certificate ready to send? (yes/no)"

---

### Phase 5 — PMI Account

1. "Have you created an account at pmi.org yet?"
2. "Are you planning to become a PMI member? (Membership is ~$139/year but saves ~$30 on the exam fee — it's worth it if you're going to take the exam)"

---

## Saving Answers

After each phase completes, update the profile.md immediately — don't wait until the end.

Write to `pmp/ApplicationProcess/{person}/profile.md` using this structure:

- Education table: fill in degree, institution, field, year
- Update experience requirement based on degree level
- Project Inventory table: one row per project
- Description Status table: update status to "⬜ Data collected" once all fields answered
- Audit Prep checklist: check boxes as confirmed
- PMI Account section: fill in what's known

When saving, preserve any existing data in the file. Only overwrite fields that were answered in this session.

---

## Generating Draft Descriptions

When the user asks to draft a description (during or after intake):

1. Read the project's captured data from profile.md
2. Translate the plain-English responsibilities into PMBOK process group language
3. Use this structure (target 300–400 words):

```
**Project Objectives:** [1–2 sentences from objective answer]

**Outcome:** [1–2 sentences from outcome answer]

**Role:** My role was the project manager.

**Responsibilities:** [PMBOK/Agile language based on methodology]
- Traditional: reference charter, WBS, schedule, budget, risk register, stakeholder comms, resource plan, change management, lessons learned, close-out
- Agile: reference product owner, backlog prioritization, sprint planning, daily standups, retrospectives, burn-down charts, servant leadership
- Hybrid: combine both as appropriate

**Deliverables:** [from deliverables answer]
```

Save the draft to: `pmp/ApplicationProcess/{person}/descriptions/project-{N}-{short-name}.md`
Update the Description Status table in profile.md to "✅ Draft ready".

---

## End of Session Summary

When done (or when user says stop), display:

```
## PMP Intake Summary — {Person}

Education:       [degree] from [institution] — [year]
Requirement:     [36 or 60] months
Months captured: [X] of [required]
Projects:        [N] project(s) entered
Descriptions:    [N] drafted, [N] still needed

35-hour cert:    [have it / need it / in progress]
Degree copy:     [ready / not yet]
Contacts notified: [yes / not yet]

Next steps:
- [list any incomplete items]
```

---

## Reference

Full application guide: `pmp/ApplicationProcess/PMP-Application-Plan.md`
