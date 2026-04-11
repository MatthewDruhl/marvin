"""Tests for batch_plan.py — grouping, ordering, rendering, and --assign."""
import json
from pathlib import Path

from batch_plan import assign_batches, batch_description, group_into_batches, render_plan


def make_finding(id_: str, severity: str, blocking: bool, scope: str = "Security") -> dict:
    return {
        "id": id_,
        "title": f"Test finding {id_}",
        "scope": scope,
        "severity": severity,
        "blocking": blocking,
        "where": "test.py:1",
        "what": "x",
        "proof": "x",
        "impact": "x",
        "fix": "x",
    }


class TestGroupIntoBatches:
    def test_blocking_always_in_batch_1(self) -> None:
        findings = [
            make_finding("SEC-1", "High", blocking=True),
            make_finding("CQ-1", "Low", blocking=False, scope="Code Quality"),
        ]
        batches = group_into_batches(findings)
        assert batches[0][0]["id"] == "SEC-1"
        assert batches[0][0]["blocking"] is True

    def test_all_blocking_in_same_batch(self) -> None:
        findings = [
            make_finding("SEC-1", "Critical", blocking=True),
            make_finding("AI-1", "High", blocking=True, scope="AI"),
            make_finding("CQ-1", "Low", blocking=False, scope="Code Quality"),
        ]
        batches = group_into_batches(findings)
        batch_1_ids = {f["id"] for f in batches[0]}
        assert "SEC-1" in batch_1_ids
        assert "AI-1" in batch_1_ids

    def test_non_blocking_not_in_batch_1_when_blocking_exists(self) -> None:
        findings = [
            make_finding("SEC-1", "Critical", blocking=True),
            make_finding("CQ-1", "Low", blocking=False, scope="Code Quality"),
        ]
        batches = group_into_batches(findings)
        batch_1_ids = {f["id"] for f in batches[0]}
        assert "CQ-1" not in batch_1_ids

    def test_no_blocking_findings_starts_with_non_blocking(self) -> None:
        findings = [
            make_finding("CQ-1", "Medium", blocking=False, scope="Code Quality"),
            make_finding("AI-1", "Low", blocking=False, scope="AI"),
        ]
        batches = group_into_batches(findings)
        assert len(batches) >= 1
        assert all(not f["blocking"] for f in batches[0])

    def test_same_scope_grouped_together(self) -> None:
        findings = [
            make_finding("SEC-1", "Medium", blocking=False, scope="Security"),
            make_finding("SEC-2", "Low", blocking=False, scope="Security"),
            make_finding("AI-1", "High", blocking=False, scope="AI"),
        ]
        batches = group_into_batches(findings)
        # AI-1 is highest severity so its scope should be in the first non-blocking batch
        first_batch_ids = {f["id"] for f in batches[0]}
        assert "AI-1" in first_batch_ids
        # SEC-1 and SEC-2 should be in the same batch
        sec_batches = [
            i for i, b in enumerate(batches) if any(f["id"].startswith("SEC") for f in b)
        ]
        assert len(set(sec_batches)) == 1, "SEC findings split across batches"

    def test_blocking_sorted_by_severity_desc(self) -> None:
        findings = [
            make_finding("SEC-1", "Low", blocking=True),
            make_finding("SEC-2", "Critical", blocking=True),
            make_finding("SEC-3", "High", blocking=True),
        ]
        batches = group_into_batches(findings)
        batch_1 = batches[0]
        severities = [f["severity"] for f in batch_1]
        assert severities[0] == "Critical"
        assert severities[1] == "High"
        assert severities[2] == "Low"

    def test_empty_findings_returns_empty(self) -> None:
        assert group_into_batches([]) == []


class TestBatchDescription:
    def test_blocking_batch_description(self) -> None:
        batch = [make_finding("SEC-1", "High", blocking=True)]
        assert "blocking" in batch_description(batch, 1)

    def test_non_blocking_uses_scope(self) -> None:
        batch = [
            make_finding("AI-1", "Medium", blocking=False, scope="AI"),
            make_finding("AI-2", "Low", blocking=False, scope="AI"),
        ]
        desc = batch_description(batch, 2)
        assert "ai" in desc.lower()

    def test_multi_scope_description(self) -> None:
        batch = [
            make_finding("AI-1", "Medium", blocking=False, scope="AI"),
            make_finding("CQ-1", "Low", blocking=False, scope="Code Quality"),
        ]
        desc = batch_description(batch, 2)
        assert "ai" in desc.lower()
        assert "code quality" in desc.lower()


class TestRenderPlan:
    def test_render_includes_batch_headers(self) -> None:
        batches = [[make_finding("SEC-1", "High", blocking=True)]]
        output = render_plan(batches)
        assert "### Batch 1" in output
        assert "SEC-1" in output

    def test_blocking_batch_says_yes(self) -> None:
        batches = [[make_finding("SEC-1", "High", blocking=True)]]
        output = render_plan(batches)
        assert "Yes — must fix before shipping" in output

    def test_non_blocking_batch_says_no(self) -> None:
        batches = [[make_finding("CQ-1", "Low", blocking=False)]]
        output = render_plan(batches)
        assert "No — quality improvement" in output

    def test_batch_1_dependency_is_none(self) -> None:
        batches = [[make_finding("SEC-1", "High", blocking=True)]]
        output = render_plan(batches)
        assert "None — do this first" in output

    def test_subsequent_batch_references_prior(self) -> None:
        batches = [
            [make_finding("SEC-1", "High", blocking=True)],
            [make_finding("CQ-1", "Low", blocking=False)],
        ]
        output = render_plan(batches)
        assert "Batch 1" in output.split("### Batch 2")[1]


class TestAssignBatches:
    def test_writes_batch_numbers(self, tmp_path: Path) -> None:
        findings = [
            make_finding("SEC-1", "High", blocking=True),
            make_finding("CQ-1", "Low", blocking=False, scope="Code Quality"),
        ]
        path = tmp_path / "findings.json"
        path.write_text(json.dumps(findings))

        batches = group_into_batches(findings)
        assign_batches(path, batches)

        result = json.loads(path.read_text())
        id_to_batch = {f["id"]: f["batch"] for f in result}
        assert id_to_batch["SEC-1"] == 1
        assert id_to_batch["CQ-1"] == 2

    def test_blocking_always_gets_batch_1(self, tmp_path: Path) -> None:
        findings = [
            make_finding("SEC-1", "Low", blocking=True),
            make_finding("SEC-2", "Critical", blocking=True),
        ]
        path = tmp_path / "findings.json"
        path.write_text(json.dumps(findings))

        batches = group_into_batches(findings)
        assign_batches(path, batches)

        result = json.loads(path.read_text())
        for f in result:
            if f["blocking"]:
                assert f["batch"] == 1
