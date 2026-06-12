# MARVIN Dashboard Concept

**Status:** Parked — revisit after PMP exam (post-June 2026)
**Source:** [YouTube - Do You Need a Claude Code-Powered Agentic OS?](https://www.youtube.com/watch?v=pfPi04pIfaw)
**Transcript:** `content/transcripts/transcript_pfPi04pIfaw.txt`
**Screenshots:** `content/diagrams/cc-dashboard/`

---

## Concept

A local dashboard that makes MARVIN's current operating state glanceable without reading multiple state files. The dashboard should reflect live MARVIN data from the repo at render time; mock values are acceptable only as examples in design notes, tests, or empty-state fixtures.

## The Three Gaps It Solves

1. **Memory** — Persistent context across sessions (Obsidian, state files, RAG)
2. **Consistency** — Skills organized by domain, producing repeatable outcomes every time
3. **Visibility** — Compact view of priorities, open loops, stale commitments, habits, learning, and recent sessions

## Architecture (from video)

```
MARVIN
├── Memory Layer (Obsidian / state files)
├── State files
│   ├── current.md
│   ├── commitments.json
│   ├── goals.md
│   ├── habits.md
│   └── projects.md
├── Session logs
└── Dashboard (web UI)
    ├── Priorities
    ├── Open loops
    ├── Needs-attention alerts
    ├── Job search / TWC
    ├── Learning / habits
    └── Recent sessions
```

## How This Maps to Matt's Projects

| Video Concept | Matt Already Has | Gap |
|---------------|------------------|-----|
| Memory layer | MARVIN state files, Obsidian vault | No RAG, but state files work fine |
| Domain skills | MARVIN skills and slash-command workflows | Already built |
| Automations | Session startup, state refresh, and local scripts | Working |
| Dashboard | None | **This is the build** |
| Primary user | Matt | Needs a local operating-state view |

## Build Considerations

- **Frontend:** React or simple HTML + Tailwind (keep it light)
- **Backend:** Python server or generated static HTML
- **State:** Read MARVIN state files for display; do not hardcode current priorities, commitments, counts, or session summaries in the dashboard implementation
- **Auth:** Simple passphrase (like DandD) or local-only
- **Deployment:** Local first (Mac Mini for always-on), remote later

## Dynamic Data Contract

- Use `state/commitments.json` as the source of truth for open loops and commitment health.
- Use `state/current.md`, `state/goals.md`, `state/habits.md`, and `state/projects.md` as display/context inputs.
- Use `sessions/` to derive recent-session summaries and project activity.
- Treat static sample values in wireframes as illustrative only.
- Preserve read-only behavior for the MVP.

## Screenshots to Capture

Add to `content/diagrams/cc-dashboard/`:
- [ ] Dashboard main view
- [ ] MARVIN state-source diagram
- [ ] Open-loop and staleness view
- [ ] Recent-session view

---

*Created: 2026-04-24 — Updated: 2026-04-26 — Revisit after PMP exam*
