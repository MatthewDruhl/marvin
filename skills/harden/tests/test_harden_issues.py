"""Tests for harden-issues.py — issue creation, body building, and validation."""

import importlib.util
from pathlib import Path
from unittest.mock import MagicMock, patch

# harden-issues.py has a dash so it can't be imported with a plain import statement.
_spec = importlib.util.spec_from_file_location(
    "harden_issues",
    Path(__file__).parent.parent / "harden-issues.py",
)
_mod = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_mod)
build_body = _mod.build_body
create_issue = _mod.create_issue
validate_findings = _mod.validate_findings

# ---------------------------------------------------------------------------
# build_body
# ---------------------------------------------------------------------------

MINIMAL_FINDING = {
    "id": "SEC-1",
    "title": "Hardcoded API key",
    "scope": "Security",
    "severity": "Critical",
    "blocking": True,
    "where": "config.py:42",
    "what": "API key stored in plaintext",
    "proof": "grep -r 'sk-' shows key at line 42",
    "impact": "Full API access to attacker",
    "fix": "Move to environment variable",
    "batch": 1,
}


class TestBuildBody:
    def test_includes_id_and_title(self):
        body = build_body(MINIMAL_FINDING)
        assert "SEC-1" in body
        assert "Hardcoded API key" in body

    def test_includes_scope_and_severity(self):
        body = build_body(MINIMAL_FINDING)
        assert "Security" in body
        assert "Critical" in body

    def test_blocking_yes_when_true(self):
        body = build_body(MINIMAL_FINDING)
        assert "**Blocking:** Yes" in body

    def test_blocking_no_when_false(self):
        f = {**MINIMAL_FINDING, "blocking": False}
        body = build_body(f)
        assert "**Blocking:** No" in body

    def test_where_in_code_block(self):
        body = build_body(MINIMAL_FINDING)
        assert "`config.py:42`" in body

    def test_fix_included(self):
        body = build_body(MINIMAL_FINDING)
        assert "Move to environment variable" in body

    def test_footer_attribution(self):
        body = build_body(MINIMAL_FINDING)
        assert "Filed by harden-issues.py" in body

    def test_optional_fields_missing_no_keyerror(self):
        sparse = {
            "id": "AI-1",
            "title": "Sparse finding",
            "scope": "AI",
            "severity": "Low",
            "blocking": False,
            "where": "foo.py:1",
            "what": "something",
            "fix": "fix it",
            "batch": 1,
        }
        body = build_body(sparse)  # no proof or impact
        assert "AI-1" in body


# ---------------------------------------------------------------------------
# create_issue — dry run
# ---------------------------------------------------------------------------


class TestCreateIssueDryRun:
    def test_dry_run_does_not_call_subprocess(self, capsys):
        with patch("subprocess.run") as mock_run:
            create_issue(MINIMAL_FINDING, repo="owner/repo", batch=1, dry_run=True)
            mock_run.assert_not_called()

    def test_dry_run_prints_title(self, capsys):
        create_issue(MINIMAL_FINDING, repo="owner/repo", batch=1, dry_run=True)
        out = capsys.readouterr().out
        assert "[dry-run]" in out
        assert "SEC-1" in out

    def test_live_run_builds_correct_gh_cmd(self, capsys):
        mock_result = MagicMock()
        mock_result.returncode = 0
        mock_result.stdout = "https://github.com/owner/repo/issues/1"
        with patch("subprocess.run", return_value=mock_result) as mock_run:
            create_issue(MINIMAL_FINDING, repo="owner/repo", batch=1, dry_run=False)
            args, kwargs = mock_run.call_args
            cmd = args[0]
            assert cmd[0] == "gh"
            assert "issue" in cmd
            assert "create" in cmd
            assert "--repo" in cmd
            assert "owner/repo" in cmd
            assert "--label" in cmd

    def test_live_run_includes_blocking_label(self):
        mock_result = MagicMock()
        mock_result.returncode = 0
        mock_result.stdout = ""
        with patch("subprocess.run", return_value=mock_result) as mock_run:
            create_issue(MINIMAL_FINDING, repo="owner/repo", batch=1, dry_run=False)
            cmd = mock_run.call_args[0][0]
            label_idx = cmd.index("--label") + 1
            labels = cmd[label_idx]
            assert "blocking" in labels
            assert "critical" in labels

    def test_live_run_no_blocking_label_when_false(self):
        mock_result = MagicMock()
        mock_result.returncode = 0
        mock_result.stdout = ""
        f = {**MINIMAL_FINDING, "blocking": False}
        with patch("subprocess.run", return_value=mock_result) as mock_run:
            create_issue(f, repo="owner/repo", batch=1, dry_run=False)
            cmd = mock_run.call_args[0][0]
            label_idx = cmd.index("--label") + 1
            labels = cmd[label_idx]
            assert "blocking" not in labels


# ---------------------------------------------------------------------------
# validate_findings
# ---------------------------------------------------------------------------


class TestValidateFindings:
    def test_valid_finding_no_errors(self):
        errors = validate_findings([MINIMAL_FINDING])
        assert errors == []

    def test_missing_required_field(self):
        bad = {k: v for k, v in MINIMAL_FINDING.items() if k != "fix"}
        errors = validate_findings([bad])
        assert any("fix" in e for e in errors)

    def test_invalid_severity_reported(self):
        bad = {**MINIMAL_FINDING, "severity": "urgent"}
        errors = validate_findings([bad])
        assert any("invalid severity" in e for e in errors)

    def test_multiple_missing_fields(self):
        bad = {"id": "X-1", "title": "x", "scope": "Security"}
        errors = validate_findings([bad])
        # at least severity, blocking, where, what, fix, batch are missing
        assert len(errors) >= 2

    def test_empty_list_no_errors(self):
        assert validate_findings([]) == []
