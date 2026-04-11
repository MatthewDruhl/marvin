"""Tests for harden_state.py — state read/write, build helpers."""

from datetime import date
from pathlib import Path

from harden_state import (
    batches_from_findings,
    build_initial_state,
    mark_batch_filed,
    read_state,
    update_batch_state,
    write_state,
)

# ---------------------------------------------------------------------------
# Fixtures / helpers
# ---------------------------------------------------------------------------

SAMPLE_STATE = {
    "project": "marvin",
    "target": "/path/to/project",
    "repo": "owner/repo",
    "date": "2026-04-10",
    "grade": "B",
    "token_usage": 12345,
    "findings_file": "/path/to/project/findings.json",
    "batches": {
        "1": {"status": "pending", "description": "Security", "count": 3, "issues": []},
        "2": {"status": "pending", "description": "Code Quality", "count": 2, "issues": []},
    },
}

SAMPLE_FINDINGS = [
    {"id": "SEC-1", "scope": "Security", "batch": 1, "severity": "Critical", "blocking": True},
    {"id": "SEC-2", "scope": "Security", "batch": 1, "severity": "High", "blocking": True},
    {"id": "AI-1", "scope": "AI", "batch": 2, "severity": "Medium", "blocking": False},
    {"id": "QUAL-1", "scope": "Code Quality", "batch": 2, "severity": "Low", "blocking": False},
]


# ---------------------------------------------------------------------------
# write_state / read_state
# ---------------------------------------------------------------------------


class TestWriteAndReadState:
    def test_write_and_read_state(self, tmp_path: Path) -> None:
        state_path = tmp_path / "harden-state.json"
        write_state(state_path, SAMPLE_STATE)
        result = read_state(state_path)
        assert result == SAMPLE_STATE

    def test_write_state_atomic_no_tmp_leftover(self, tmp_path: Path) -> None:
        state_path = tmp_path / "harden-state.json"
        write_state(state_path, SAMPLE_STATE)
        # Only the final file should exist — no temp files left behind
        files = list(tmp_path.iterdir())
        assert len(files) == 1
        assert files[0] == state_path

    def test_read_state_returns_none_when_missing(self, tmp_path: Path) -> None:
        state_path = tmp_path / "nonexistent.json"
        assert read_state(state_path) is None

    def test_write_creates_valid_json(self, tmp_path: Path) -> None:
        state_path = tmp_path / "harden-state.json"
        write_state(state_path, SAMPLE_STATE)
        import json
        raw = json.loads(state_path.read_text())
        assert raw["project"] == "marvin"


# ---------------------------------------------------------------------------
# build_initial_state
# ---------------------------------------------------------------------------


class TestBuildInitialState:
    def test_all_fields_present(self) -> None:
        batches = batches_from_findings(SAMPLE_FINDINGS)
        state = build_initial_state(
            project="myproject",
            target="/some/path",
            repo="owner/repo",
            grade="A",
            token_usage=9999,
            findings_file="/some/path/findings.json",
            batches=batches,
        )
        for field in ("project", "target", "repo", "date", "grade", "token_usage",
                      "findings_file", "batches"):
            assert field in state, f"Missing field: {field}"

    def test_date_is_today(self) -> None:
        state = build_initial_state(
            project="p", target="/t", repo="o/r", grade="B",
            token_usage=0, findings_file="f.json", batches={},
        )
        assert state["date"] == date.today().isoformat()

    def test_batches_keyed_by_string(self) -> None:
        batches = batches_from_findings(SAMPLE_FINDINGS)
        state = build_initial_state(
            project="p", target="/t", repo="o/r", grade="C",
            token_usage=100, findings_file="f.json", batches=batches,
        )
        for key in state["batches"]:
            assert isinstance(key, str), f"Batch key must be str, got {type(key)}"


# ---------------------------------------------------------------------------
# batches_from_findings
# ---------------------------------------------------------------------------


class TestBatchesFromFindings:
    def test_grouping_and_count(self) -> None:
        batches = batches_from_findings(SAMPLE_FINDINGS)
        assert batches["1"]["count"] == 2
        assert batches["2"]["count"] == 2

    def test_status_is_pending(self) -> None:
        batches = batches_from_findings(SAMPLE_FINDINGS)
        for b in batches.values():
            assert b["status"] == "pending"

    def test_issues_list_is_empty(self) -> None:
        batches = batches_from_findings(SAMPLE_FINDINGS)
        for b in batches.values():
            assert b["issues"] == []

    def test_description_from_first_finding_scope(self) -> None:
        batches = batches_from_findings(SAMPLE_FINDINGS)
        assert batches["1"]["description"] == "Security"
        assert batches["2"]["description"] == "AI"

    def test_keys_are_strings(self) -> None:
        batches = batches_from_findings(SAMPLE_FINDINGS)
        for k in batches:
            assert isinstance(k, str)

    def test_empty_findings_returns_empty_dict(self) -> None:
        assert batches_from_findings([]) == {}

    def test_default_batch_when_missing(self) -> None:
        findings = [{"id": "X-1", "scope": "Security"}]  # no "batch" key
        batches = batches_from_findings(findings)
        assert "1" in batches


# ---------------------------------------------------------------------------
# update_batch_state
# ---------------------------------------------------------------------------


class TestUpdateBatchState:
    def test_no_op_when_state_file_missing(self, tmp_path: Path) -> None:
        state_path = tmp_path / "harden-state.json"
        # Should not raise even though file doesn't exist
        update_batch_state(state_path, 1, "SEC-1", "https://github.com/owner/repo/issues/1")

    def test_appends_issue_to_batch(self, tmp_path: Path) -> None:
        state_path = tmp_path / "harden-state.json"
        write_state(state_path, SAMPLE_STATE)
        update_batch_state(state_path, 1, "SEC-1", "https://github.com/owner/repo/issues/1")
        state = read_state(state_path)
        assert state["batches"]["1"]["issues"] == [
            {"id": "SEC-1", "url": "https://github.com/owner/repo/issues/1"}
        ]

    def test_no_op_when_batch_missing(self, tmp_path: Path) -> None:
        state_path = tmp_path / "harden-state.json"
        write_state(state_path, SAMPLE_STATE)
        # Batch 99 doesn't exist — should not raise
        update_batch_state(state_path, 99, "X-1", "https://github.com/x")


# ---------------------------------------------------------------------------
# mark_batch_filed
# ---------------------------------------------------------------------------


class TestMarkBatchFiled:
    def test_no_op_when_state_file_missing(self, tmp_path: Path) -> None:
        state_path = tmp_path / "harden-state.json"
        mark_batch_filed(state_path, 1)  # should not raise

    def test_sets_status_to_filed(self, tmp_path: Path) -> None:
        state_path = tmp_path / "harden-state.json"
        write_state(state_path, SAMPLE_STATE)
        mark_batch_filed(state_path, 1)
        state = read_state(state_path)
        assert state["batches"]["1"]["status"] == "filed"

    def test_other_batches_unchanged(self, tmp_path: Path) -> None:
        state_path = tmp_path / "harden-state.json"
        write_state(state_path, SAMPLE_STATE)
        mark_batch_filed(state_path, 1)
        state = read_state(state_path)
        assert state["batches"]["2"]["status"] == "pending"

    def test_no_op_when_batch_missing(self, tmp_path: Path) -> None:
        state_path = tmp_path / "harden-state.json"
        write_state(state_path, SAMPLE_STATE)
        mark_batch_filed(state_path, 99)  # should not raise
