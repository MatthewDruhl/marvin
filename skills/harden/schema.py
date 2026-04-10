"""Shared schema definitions for the harden audit pipeline."""

VALID_SEVERITIES: frozenset[str] = frozenset({"critical", "high", "medium", "low"})

# Superset of all fields required by the full pipeline (validate → score → issues).
# Both validate_findings.py and harden-issues.py import from here so they stay in sync.
REQUIRED_FIELDS: frozenset[str] = frozenset(
    {"id", "title", "scope", "severity", "blocking", "where", "what", "fix", "batch"}
)
