"""Tests for bullet scoring functions in resume_builder.py."""

import sys
from pathlib import Path

# Add scripts dir to path so we can import resume_builder
sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))

from resume_builder import score_bullet, score_tailoring

# ---------------------------------------------------------------------------
# score_bullet
# ---------------------------------------------------------------------------

class TestScoreBullet:
    """Tests for the score_bullet keyword matching function."""

    def test_exact_keyword_match(self):
        """Keywords that appear exactly in the bullet should score."""
        score = score_bullet("Managed Linux servers and wrote Bash scripts", ["Linux", "Bash"])
        assert score == 1.0

    def test_no_match(self):
        """Keywords not in the bullet should score 0."""
        score = score_bullet("Managed Windows servers", ["Linux", "Bash"])
        assert score == 0.0

    def test_partial_match(self):
        """Only matching keywords should count."""
        score = score_bullet("Managed Linux servers", ["Linux", "Bash"])
        assert score == 0.5

    def test_case_insensitive(self):
        """Matching should be case-insensitive."""
        score = score_bullet("Built a PYTHON pipeline", ["python"])
        assert score == 1.0

    def test_empty_keywords(self):
        """Empty keyword list should return 0.5 (neutral)."""
        score = score_bullet("Any bullet text", [])
        assert score == 0.5

    def test_empty_bullet(self):
        """Empty bullet text should score 0 against any keywords."""
        score = score_bullet("", ["Linux", "Python"])
        assert score == 0.0

    # --- Known substring false positives (current behavior) ---
    # These tests document the CURRENT behavior. When we fix the keyword
    # matching to use word boundaries, flip expected values.

    def test_sql_does_not_match_mysql(self):
        """'SQL' should not match inside 'MySQL' (word-boundary matching)."""
        score = score_bullet("Configured MySQL databases", ["SQL"])
        assert score == 0.0

    def test_java_does_not_match_javascript(self):
        """'Java' should not match inside 'JavaScript' (word-boundary matching)."""
        score = score_bullet("Built JavaScript frontends", ["Java"])
        assert score == 0.0

    def test_sql_matches_standalone_sql(self):
        """'SQL' should still match when it appears as a standalone word."""
        score = score_bullet("Wrote complex SQL queries for reporting", ["SQL"])
        assert score == 1.0

    def test_java_matches_standalone_java(self):
        """'Java' should still match when it appears as a standalone word."""
        score = score_bullet("Built Java microservices with Spring Boot", ["Java"])
        assert score == 1.0

    def test_multiple_keywords_partial(self):
        """Score reflects fraction of keywords matched."""
        score = score_bullet(
            "Deployed Docker containers on Kubernetes",
            ["Docker", "Kubernetes", "Terraform", "Ansible"],
        )
        assert score == 0.5  # 2 of 4


# ---------------------------------------------------------------------------
# score_tailoring
# ---------------------------------------------------------------------------

def _make_tailoring(experience=None, additional_experience=None, military=None):
    """Helper to build a minimal tailoring dict for testing."""
    t = {}
    if experience is not None:
        t["experience"] = experience
    if additional_experience is not None:
        t["additional_experience"] = additional_experience
    if military is not None:
        t["military"] = military
    return t


class TestScoreTailoring:
    """Tests for the score_tailoring function."""

    def test_returns_sorted_ascending(self):
        """Results should be sorted by score, lowest first."""
        tailoring = _make_tailoring(experience=[{
            "company": "Acme",
            "roles": [
                {
                    "title": "Dev",
                    "bullets": [
                        "Used Python and SQL daily",
                        "Managed office supplies",
                        "Built Linux automation with Bash and Python",
                    ],
                }
            ],
        }])
        scored = score_tailoring(tailoring, ["Python", "SQL", "Linux", "Bash"])
        scores = [s["score"] for s in scored]
        assert scores == sorted(scores), "Should be sorted ascending"

    def test_includes_all_bullets(self):
        """Every bullet from every section should be scored."""
        tailoring = _make_tailoring(
            experience=[{
                "company": "Acme",
                "roles": [{"title": "Dev", "bullets": ["Bullet 1", "Bullet 2"]}],
            }],
            additional_experience=[{
                "company": "OldCo",
                "roles": [{"title": "Jr Dev", "bullets": ["Old bullet"]}],
            }],
            military={
                "branch": "Army",
                "role": "Medic",
                "bullets": ["Military bullet"],
            },
        )
        scored = score_tailoring(tailoring, ["test"])
        assert len(scored) == 4

    def test_empty_tailoring(self):
        """Empty tailoring should return empty list."""
        scored = score_tailoring({}, ["Python"])
        assert scored == []

    def test_entry_structure(self):
        """Each scored entry should have required fields."""
        tailoring = _make_tailoring(experience=[{
            "company": "Acme",
            "roles": [{"title": "Dev", "bullets": ["Used Python"]}],
        }])
        scored = score_tailoring(tailoring, ["Python"])
        entry = scored[0]
        assert "section" in entry
        assert "company" in entry
        assert "role" in entry
        assert "bullet_index" in entry
        assert "text" in entry
        assert "full_text" in entry
        assert "score" in entry

    def test_long_bullet_text_truncated(self):
        """The 'text' field should be truncated to 80 chars + '...'."""
        long_bullet = "A" * 100
        tailoring = _make_tailoring(experience=[{
            "company": "Acme",
            "roles": [{"title": "Dev", "bullets": [long_bullet]}],
        }])
        scored = score_tailoring(tailoring, ["Python"])
        assert len(scored[0]["text"]) == 83  # 80 + "..."
        assert scored[0]["full_text"] == long_bullet

    def test_military_bullets_scored(self):
        """Military bullets should be included in scoring."""
        tailoring = _make_tailoring(military={
            "branch": "Army",
            "role": "Medic",
            "bullets": ["Managed Linux medical systems"],
        })
        scored = score_tailoring(tailoring, ["Linux"])
        assert len(scored) == 1
        assert scored[0]["section"] == "military"
        assert scored[0]["score"] > 0
