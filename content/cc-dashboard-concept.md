# CC-DB: Claude Code Dashboard

**Status:** Parked — revisit after PMP exam (post-June 2026)
**Source:** [YouTube - Do You Need a Claude Code-Powered Agentic OS?](https://www.youtube.com/watch?v=pfPi04pIfaw)
**Transcript:** `content/transcripts/transcript_pfPi04pIfaw.txt`
**Screenshots:** `content/diagrams/cc-dashboard/`

---

## Concept

A web dashboard that wraps Claude Code, giving non-technical users button-based access to skills and automations without touching the terminal. Claude Code runs headless in the background.

## The Three Gaps It Solves

1. **Memory** — Persistent context across sessions (Obsidian, state files, RAG)
2. **Consistency** — Skills organized by domain, producing repeatable outcomes every time
3. **Accessibility** — Visual interface so non-technical users can execute skills via buttons

## Architecture (from video)

```
Claude Code (engine)
├── Memory Layer (Obsidian / state files)
├── Domain 1: [e.g., Sales/Email]
│   ├── Skill A → on-demand or automated
│   ├── Skill B → local or remote
│   └── ...
├── Domain 2: [e.g., Research]
│   ├── Skill C
│   └── ...
├── Domain N: [custom]
│   └── ...
└── Dashboard (web UI)
    ├── Buttons → run skills headless
    ├── Status cards → recent runs, usage
    ├── Output viewer → results from Obsidian/state
    └── Vault browser → recent changes
```

## How This Maps to Matt's Projects

| Video Concept | Matt Already Has | Gap |
|---------------|------------------|-----|
| Memory layer | MARVIN state files, Obsidian vault | No RAG, but state files work fine |
| Domain skills | `/gmail-scan`, `/draft`, `/review` (YPS), `/pmp-consume`, `/resume` (MARVIN) | Already built |
| Automations | Background agents, `/loop`, `/schedule` | Working |
| Dashboard | None | **This is the build** |
| Non-technical user | John (YPS) | Handoff guide written, but terminal-dependent |

## Build Considerations

- **Frontend:** React or simple HTML + Tailwind (keep it light)
- **Backend:** Node or Python server that spawns `claude` CLI headless
- **State:** Read MARVIN/YPS state files for display
- **Auth:** Simple passphrase (like DandD) or local-only
- **Deployment:** Local first (Mac Mini for always-on), remote later

## Screenshots to Capture

Add to `content/diagrams/cc-dashboard/`:
- [ ] Dashboard main view (buttons, status cards, usage)
- [ ] Org chart / mental model diagram
- [ ] Skill execution flow (button → headless run → output)
- [ ] Vault/output viewer

## Relationship to YPS Assistant

CC-DB is one of the access layers for the YPS Assistant. See `content/yps-assistant-architecture.md` for the full design. The dashboard would be how John and Kirk interact with their assistant without using the terminal.

---

*Created: 2026-04-24 — Updated: 2026-04-26 — Revisit after PMP exam*
