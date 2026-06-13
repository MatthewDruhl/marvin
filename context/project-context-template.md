# CONTEXT.md Template

Per-project context manifest (marvin#284). One per active project, stored at the project's content root (e.g. `content/freelance/<Client>/CONTEXT.md`). Purpose: any AI or human dropped into the marvin workspace can orient on a project in one read, and a second AI doing cross-review knows where to look without reading everything.

Maintenance: update at `/end` when the project materially changed; the manifest is a map, not a log. Keep it under ~80 lines; details live in the linked files. Live data boundaries still apply (PRIVACY.md): no rates, secrets, or personal data in tracked manifests.

---

```markdown
# <Project> — Context Manifest

Last updated: YYYY-MM-DD

## What This Is
<One paragraph: what the project is, for whom, and the core business problem.>

## Stakeholders
- **<Name>** — <role, what they own, how they matter to decisions>

## Key Decisions
- **<Decision>** (<date>) — <why; link to decisions.md row or session log>

## Current Status
<2-5 bullets: where things stand, what's in flight, what's blocked.>

## Open Questions
- <Question> (owner: <who>)

## Where to Find Details
- <file/path> — <what it contains>
- Session logs: <relevant dates>

## Reviews
- <What was reviewed, by whom/what, when, verdict> 
```
