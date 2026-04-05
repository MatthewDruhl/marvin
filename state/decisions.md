# Decisions Log

Track key decisions with context so future sessions understand *why*, not just *what*.

| Date | Decision | Context |
|------|----------|---------|
| 2026-04-05 | Slack bot uses `--resume` for session continuity | `--session-id` only names new sessions, doesn't load history. `--resume <id>` actually continues conversations. |
| 2026-04-05 | Resume skill: word-boundary keyword matching | Substring matching caused false positives (SQL/MySQL, Java/JavaScript). Now uses `re.search(\b...\b)`. |
| 2026-04-05 | Resume skill: single shared line estimation function | `cmd_build` and `estimate_total_lines` had parallel implementations that could drift. Extracted `_estimate_pre_experience_lines()`. |
| 2026-04-05 | Resume data lives at ~/Resume/, not in marvin repo | Personal content (resume-data.json, base docx, role deep dives) stays outside git. Skill code stays in marvin. |
| 2026-04-05 | Voice samples extracted to ~/Resume/data/ | Direct interview quotes are personal data, not skill logic. SKILL.md references the file instead. |
| 2026-04-05 | Generic resume skill design — tabled | Need onboarding, template generation, voice discovery, configurable paths before open-sourcing. Revisit when ready. |
| 2026-04-03 | DnD project stays private, not portfolio material | AI-generated code, not demonstrable skill. Open-source MARVIN fork is the portfolio project instead. |
| 2026-04-03 | Open-source MARVIN fork is leading double-duty project | Researched 20+ AI Chief of Staff tools. MARVIN is among the most feature-complete with unique differentiators. |
| 2026-04-02 | No SRE roles in job search | Not the right fit. Target: platform eng, DevOps, app support, TPM, integration. |

---

*Updated by MARVIN at session end. Add entries when making non-obvious choices.*
