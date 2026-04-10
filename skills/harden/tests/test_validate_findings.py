"""Tests for validate_findings.py — required field checks, severity validation, blocking type."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from validate_findings import validate

VALID_FINDING = {
    "id": "SEC-1",
    "title": "Hardcoded key",
    "scope": "Security",
    "severity": "High",
    "blocking": True,
    "where": "config.py:10",
    "what": "Key in plaintext",
    "fix": "Use env var",
    "batch": 1,
}


class TestValidate:
    def test_valid_finding_no_errors(self):
        assert validate([VALID_FINDING]) == []

    def test_empty_list_no_errors(self):
        assert validate([]) == []

    def test_missing_required_field_id(self):
        bad = {k: v for k, v in VALID_FINDING.items() if k != "id"}
        errors = validate([bad])
        assert any("id" in e for e in errors)

    def test_missing_required_field_fix(self):
        bad = {k: v for k, v in VALID_FINDING.items() if k != "fix"}
        errors = validate([bad])
        assert any("fix" in e for e in errors)

    def test_missing_required_field_batch(self):
        bad = {k: v for k, v in VALID_FINDING.items() if k != "batch"}
        errors = validate([bad])
        assert any("batch" in e for e in errors)

    def test_invalid_severity_value(self):
        bad = {**VALID_FINDING, "severity": "urgent"}
        errors = validate([bad])
        assert any("invalid severity" in e for e in errors)

    def test_valid_severity_values(self):
        for sev in ("Critical", "High", "Medium", "Low"):
            finding = {**VALID_FINDING, "severity": sev}
            assert validate([finding]) == [], f"Expected {sev} to be valid"

    def test_blocking_non_boolean_flagged(self):
        bad = {**VALID_FINDING, "blocking": "yes"}
        errors = validate([bad])
        assert any("blocking" in e for e in errors)

    def test_blocking_integer_flagged(self):
        bad = {**VALID_FINDING, "blocking": 1}
        errors = validate([bad])
        assert any("blocking" in e for e in errors)

    def test_multiple_findings_multiple_errors(self):
        bad1 = {k: v for k, v in VALID_FINDING.items() if k != "id"}
        bad2 = {**VALID_FINDING, "severity": "unknown"}
        errors = validate([bad1, bad2])
        assert len(errors) >= 2

    def test_error_includes_scope_label(self):
        bad = {k: v for k, v in VALID_FINDING.items() if k != "fix"}
        errors = validate([bad])
        assert any("Security" in e for e in errors)
