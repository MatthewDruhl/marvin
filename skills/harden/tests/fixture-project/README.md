# Harden Test Fixture Project

Intentionally vulnerable dummy project for testing `/harden` improvements.

Every file contains **deliberate bad patterns** that the recon scanner and
AI agent should catch. Do NOT fix these — they exist to exercise the audit.

## What's covered

| File | Patterns exercised |
|------|--------------------|
| `src/auth.py` | Hardcoded secrets, missing input validation, SQL injection |
| `src/api.py` | Shell injection, bare excepts, hardcoded IP/port |
| `src/ai_agent.py` | Prompt injection, unsafe deserialization, late imports |
| `src/utils.py` | Large file (>300 lines), no test coverage |
| `src/config.py` | Hardcoded values, environment-specific config |
| `tests/test_auth.py` | Partial coverage (only covers auth.py) |

## Usage

```bash
# Run recon scanner
uv run python skills/harden/harden-recon.py skills/harden/tests/fixture-project --json

# Run full /harden audit
/harden skills/harden/tests/fixture-project

# Test incremental mode (after first audit creates harden-state.json)
# 1. Edit a file in src/
# 2. Re-run /harden — should detect changes and scope to modified files
```
