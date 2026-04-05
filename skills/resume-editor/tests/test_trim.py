"""Tests for remove_lowest_bullet in resume_builder.py."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))

from resume_builder import remove_lowest_bullet, score_tailoring


def _make_tailoring(experience=None, military=None):
    """Helper to build tailoring data for trim tests."""
    t = {}
    if experience is not None:
        t["experience"] = experience
    if military is not None:
        t["military"] = military
    return t


class TestRemoveLowestBullet:
    """Tests for the iterative bullet removal function."""

    def test_removes_lowest_scored(self):
        """Should remove the bullet with the lowest keyword score."""
        tailoring = _make_tailoring(experience=[{
            "company": "Acme",
            "roles": [{
                "title": "Dev",
                "bullets": [
                    "Used Python and Linux daily",         # high match
                    "Managed office supplies and catering", # no match
                    "Built SQL pipelines on Linux",         # medium match
                ],
            }],
        }])
        keywords = ["Python", "Linux", "SQL"]
        scored = score_tailoring(tailoring, keywords)
        removed = remove_lowest_bullet(tailoring, scored)

        assert removed is not None
        assert "office supplies" in removed["text"]
        # Verify it was actually removed from tailoring
        remaining = tailoring["experience"][0]["roles"][0]["bullets"]
        assert len(remaining) == 2

    def test_never_removes_last_bullet(self):
        """Should never leave a role with 0 bullets."""
        tailoring = _make_tailoring(experience=[{
            "company": "Acme",
            "roles": [{
                "title": "Dev",
                "bullets": ["Only bullet here"],
            }],
        }])
        keywords = ["Python"]
        scored = score_tailoring(tailoring, keywords)
        removed = remove_lowest_bullet(tailoring, scored)

        assert removed is None
        assert len(tailoring["experience"][0]["roles"][0]["bullets"]) == 1

    def test_returns_none_when_all_roles_at_minimum(self):
        """Returns None when every role has exactly 1 bullet."""
        tailoring = _make_tailoring(experience=[{
            "company": "Acme",
            "roles": [
                {"title": "Dev", "bullets": ["One bullet"]},
                {"title": "Lead", "bullets": ["Another bullet"]},
            ],
        }])
        keywords = ["Python"]
        scored = score_tailoring(tailoring, keywords)
        removed = remove_lowest_bullet(tailoring, scored)
        assert removed is None

    def test_removes_from_role_with_most_bullets_when_tied(self):
        """When scores are equal, should still remove from a role with >1 bullet."""
        tailoring = _make_tailoring(experience=[{
            "company": "Acme",
            "roles": [
                {"title": "Dev", "bullets": ["No match A"]},
                {"title": "Lead", "bullets": ["No match B", "No match C"]},
            ],
        }])
        keywords = ["Python"]
        scored = score_tailoring(tailoring, keywords)
        removed = remove_lowest_bullet(tailoring, scored)

        assert removed is not None
        # Dev has 1 bullet (protected), so removal must come from Lead
        assert removed["role"] == "Lead"
        assert len(tailoring["experience"][0]["roles"][1]["bullets"]) == 1

    def test_military_bullets_can_be_removed(self):
        """Military bullets with >1 should be removable."""
        tailoring = _make_tailoring(military={
            "branch": "Army",
            "role": "Medic",
            "bullets": ["Managed medical supplies", "Led team of 10 medics"],
        })
        keywords = ["Python"]
        scored = score_tailoring(tailoring, keywords)
        removed = remove_lowest_bullet(tailoring, scored)

        assert removed is not None
        assert removed["section"] == "military"
        assert len(tailoring["military"]["bullets"]) == 1

    def test_military_last_bullet_protected(self):
        """Military section with 1 bullet should not be removed."""
        tailoring = _make_tailoring(military={
            "branch": "Army",
            "role": "Medic",
            "bullets": ["Only military bullet"],
        })
        keywords = ["Python"]
        scored = score_tailoring(tailoring, keywords)
        removed = remove_lowest_bullet(tailoring, scored)
        assert removed is None

    def test_multiple_removals_iterative(self):
        """Simulate multiple trim iterations."""
        tailoring = _make_tailoring(experience=[{
            "company": "Acme",
            "roles": [{
                "title": "Dev",
                "bullets": [
                    "Used Python daily",
                    "Managed supplies",
                    "Organized meetings",
                    "Filed reports",
                ],
            }],
        }])
        keywords = ["Python"]
        removed_count = 0
        for _ in range(10):  # try up to 10 removals
            scored = score_tailoring(tailoring, keywords)
            removed = remove_lowest_bullet(tailoring, scored)
            if removed is None:
                break
            removed_count += 1

        # Should have removed 3 (leaving 1 protected)
        assert removed_count == 3
        assert len(tailoring["experience"][0]["roles"][0]["bullets"]) == 1

    def test_empty_tailoring(self):
        """Empty tailoring should return None."""
        removed = remove_lowest_bullet({}, [])
        assert removed is None
