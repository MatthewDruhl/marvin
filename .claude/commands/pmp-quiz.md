---
description: PMP quiz - usage /pmp-quiz <name> [exam|revision|refresher] (Matt or Emily)
---

# /pmp-quiz - PMP Certification Quiz

Launch a PMP quiz session for a specific person.

## Usage

`/pmp-quiz <name> [mode] [count]` — where name is `Matt` or `Emily` (case-insensitive)

### Examples
- `/pmp-quiz Matt exam` — Exam Mode (60 questions, no feedback until end)
- `/pmp-quiz Matt revision` — Revision Mode (feedback after each answer)
- `/pmp-quiz Matt refresher` — Refresher Mode (recently consumed content, default 15 questions)
- `/pmp-quiz Matt refresher 10` — Refresher Mode capped at 10 questions
- `/pmp-quiz Emily refresher` — works for Emily too
- `/pmp-quiz Matt` — ask which mode before starting

## Instructions

Parse `$ARGUMENTS` for `name`, `mode`, and optional refresher count, then follow the canonical quiz workflow in `skills/pmp-quiz/SKILL.md`.
