"""Tests for score_audit.py — scorecard grade calculator."""

import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from score_audit import compute_scorecard, points_to_grade

# ---------------------------------------------------------------------------
# points_to_grade
# ---------------------------------------------------------------------------


class TestPointsToGrade:
    def test_a_zero_points_no_critical(self):
        assert points_to_grade(0, False) == "A"

    def test_b_low_points(self):
        assert points_to_grade(1, False) == "B"
        assert points_to_grade(4, False) == "B"

    def test_c_mid_points(self):
        assert points_to_grade(5, False) == "C"
        assert points_to_grade(9, False) == "C"

    def test_d_high_points(self):
        assert points_to_grade(10, False) == "D"
        assert points_to_grade(14, False) == "D"

    def test_f_very_high_points(self):
        assert points_to_grade(15, False) == "F"
        assert points_to_grade(999, False) == "F"

    def test_critical_floor_overrides_a(self):
        assert points_to_grade(0, True) == "D"

    def test_critical_floor_overrides_b(self):
        assert points_to_grade(3, True) == "D"

    def test_critical_floor_overrides_c(self):
        assert points_to_grade(7, True) == "D"

    def test_critical_floor_does_not_override_d(self):
        assert points_to_grade(12, True) == "D"

    def test_critical_floor_does_not_override_f(self):
        assert points_to_grade(15, True) == "F"


# ---------------------------------------------------------------------------
# compute_scorecard
# ---------------------------------------------------------------------------


class TestComputeScorecard:
    def test_empty_findings(self, capsys):
        compute_scorecard([])
        out = capsys.readouterr().out
        assert "No findings" in out
        assert "Grade: A" in out

    def test_single_scope_grade_b(self, capsys):
        findings = [
            {"scope": "Security", "severity": "High", "blocking": True},
        ]
        compute_scorecard(findings)
        out = capsys.readouterr().out
        assert "Security" in out
        assert "| B |" in out
        assert "Overall: B" in out

    def test_single_scope_grade_a(self, capsys):
        compute_scorecard([{"scope": "Tests", "severity": "Low", "blocking": False}])
        out = capsys.readouterr().out
        assert "| B |" in out  # 1 low = 1 pt → B

    def test_critical_floor_in_output(self, capsys):
        findings = [{"scope": "Security", "severity": "Critical", "blocking": True}]
        compute_scorecard(findings)
        out = capsys.readouterr().out
        assert "| D |" in out

    def test_overall_grade_conventional_rounding(self, capsys):
        # A(4) + B(3) + B(3) + F(0) = 10 / 4 = 2.5 → should be B(3), not C(2)
        # Python banker rounding gives round(2.5) = 2 (C) — this verifies the fix.
        findings = [
            {"scope": "AI", "severity": "Low", "blocking": False},           # 1pt → B
            {"scope": "Decoupling", "severity": "Low", "blocking": False},   # 1pt → B
            {"scope": "Security", "severity": "High", "blocking": True},     # 3pt → B
            {"scope": "Tests", "severity": "Critical", "blocking": True},    # 4pt + critical → D
        ]
        compute_scorecard(findings)
        out = capsys.readouterr().out
        # B(3) + B(3) + B(3) + D(1) = 10 / 4 = 2.5 → B with fix, C without
        assert "Overall: B" in out

    def test_missing_severity_no_keyerror(self, capsys):
        findings = [{"scope": "Security", "blocking": True}]  # no severity field
        compute_scorecard(findings)  # must not raise
        out = capsys.readouterr().out
        assert "Security" in out

    def test_blocking_vs_non_blocking_columns(self, capsys):
        findings = [
            {"scope": "Security", "severity": "High", "blocking": True},
            {"scope": "Security", "severity": "Low", "blocking": False},
        ]
        compute_scorecard(findings)
        out = capsys.readouterr().out
        assert "1 high" in out
        assert "1 low" in out

    def test_multiple_scopes_sorted(self, capsys):
        findings = [
            {"scope": "Tests", "severity": "High", "blocking": True},
            {"scope": "AI", "severity": "Low", "blocking": False},
        ]
        compute_scorecard(findings)
        out = capsys.readouterr().out
        lines = out.splitlines()
        scope_lines = [line for line in lines if "AI" in line or "Tests" in line]
        assert scope_lines[0].startswith("| AI")
        assert scope_lines[1].startswith("| Tests")

    def test_f_grade_scope(self, capsys):
        # 4 highs = 12pts → D; 5 highs = 15pts → F
        findings = [
            {"scope": "Code Quality", "severity": "High", "blocking": True},
        ] * 5
        compute_scorecard(findings)
        out = capsys.readouterr().out
        assert "| F |" in out


# ---------------------------------------------------------------------------
# CLI (invalid JSON → exit 1)
# ---------------------------------------------------------------------------


class TestCLI:
    def _run(self, input_data: str) -> subprocess.CompletedProcess:
        script = Path(__file__).parent.parent / "score_audit.py"
        return subprocess.run(
            ["python", str(script)],
            input=input_data,
            capture_output=True,
            text=True,
        )

    def test_invalid_json_exits_1(self):
        result = self._run("not json")
        assert result.returncode == 1
        assert "Error" in result.stderr

    def test_empty_input_exits_0(self):
        result = self._run("")
        assert result.returncode == 0
        assert "Grade: A" in result.stdout

    def test_valid_findings_exits_0(self):
        findings = '[{"scope":"Security","severity":"High","blocking":true}]'
        result = self._run(findings)
        assert result.returncode == 0
        assert "Overall:" in result.stdout
