"""Tests for line/page estimation functions in resume_builder.py."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))

from resume_builder import (
    CHARS_PER_LINE,
    HEADER_LINES,
    estimate_lines,
    estimate_pages,
    estimate_total_lines,
)

# ---------------------------------------------------------------------------
# estimate_lines
# ---------------------------------------------------------------------------

class TestEstimateLines:
    """Tests for single-paragraph line estimation."""

    def test_empty_string(self):
        """Empty text should count as 1 line (blank paragraph)."""
        assert estimate_lines("") == 1

    def test_short_text(self):
        """Text shorter than one line should be 1 line."""
        assert estimate_lines("Short bullet.") == 1

    def test_exactly_one_line(self):
        """Text exactly CHARS_PER_LINE long should be 1 line."""
        text = "A" * CHARS_PER_LINE
        assert estimate_lines(text) == 1

    def test_wraps_to_two_lines(self):
        """Text just over one line should wrap to 2."""
        text = "A" * (CHARS_PER_LINE + 1)
        assert estimate_lines(text) == 2

    def test_long_bullet(self):
        """A typical long bullet (~200 chars) should estimate correctly."""
        text = "A" * 200
        expected = -(-200 // CHARS_PER_LINE)  # ceiling division
        assert estimate_lines(text) == expected

    def test_very_long_text(self):
        """Very long text should scale linearly."""
        text = "A" * 500
        expected = -(-500 // CHARS_PER_LINE)
        assert estimate_lines(text) == expected


# ---------------------------------------------------------------------------
# estimate_total_lines
# ---------------------------------------------------------------------------

def _minimal_tailoring(**overrides):
    """Build a minimal tailoring dict with sensible defaults."""
    base = {
        "summary": "Experienced engineer with 25 years of platform and infrastructure experience.",
        "keywords": ["Python", "SQL", "Linux"],
        "skills": ["Python", "SQL", "Linux", "Docker"],
        "certifications": ["PMP, PMI (PMI), 2026"],
        "experience": [{
            "company": "ACME",
            "location": "Remote",
            "roles": [{
                "title": "Senior Engineer",
                "dates": "2020 - 2025",
                "bullets": [
                    "Built infrastructure automation with Terraform.",
                    "Managed Kubernetes clusters serving 2M daily users.",
                ],
            }],
        }],
        "education": [{
            "degree": "AS",
            "field": "Computer Science",
            "school": "Tech College",
            "location": "Somewhere, USA",
            "years": "1995 - 1997",
        }],
    }
    base.update(overrides)
    return base


class TestEstimateTotalLines:
    """Tests for full resume line estimation."""

    def test_minimal_tailoring_positive(self):
        """A minimal tailoring should produce a positive line count."""
        tailoring = _minimal_tailoring()
        total = estimate_total_lines(tailoring)
        assert total > 0

    def test_header_lines_included(self):
        """Total should be at least HEADER_LINES."""
        tailoring = _minimal_tailoring()
        total = estimate_total_lines(tailoring)
        assert total >= HEADER_LINES

    def test_more_bullets_more_lines(self):
        """Adding bullets should increase line count."""
        tailoring_short = _minimal_tailoring()
        tailoring_long = _minimal_tailoring(experience=[{
            "company": "ACME",
            "location": "Remote",
            "roles": [{
                "title": "Senior Engineer",
                "dates": "2020 - 2025",
                "bullets": [
                    "Bullet 1",
                    "Bullet 2",
                    "Bullet 3",
                    "Bullet 4",
                    "Bullet 5",
                    "Bullet 6",
                ],
            }],
        }])
        assert estimate_total_lines(tailoring_long) > estimate_total_lines(tailoring_short)

    def test_compact_mode_fewer_lines(self):
        """Compact mode should produce fewer lines than default."""
        tailoring_normal = _minimal_tailoring()
        tailoring_compact = _minimal_tailoring(compact=True)
        assert estimate_total_lines(tailoring_compact) < estimate_total_lines(tailoring_normal)

    def test_military_section_counted(self):
        """Military section should add lines when present."""
        tailoring_no_mil = _minimal_tailoring()
        tailoring_with_mil = _minimal_tailoring(military={
            "branch": "ARMY",
            "location": "Iowa City, IA",
            "role": "Medic",
            "start": "1993",
            "end": "2004",
            "bullets": ["Served as combat medic."],
        })
        assert estimate_total_lines(tailoring_with_mil) > estimate_total_lines(tailoring_no_mil)

    def test_empty_tailoring(self):
        """Empty tailoring should still return header lines."""
        total = estimate_total_lines({})
        assert total >= HEADER_LINES - 1  # compact could subtract 1

    def test_additional_experience_counted(self):
        """Additional experience section should add lines."""
        tailoring_base = _minimal_tailoring()
        tailoring_extra = _minimal_tailoring(additional_experience=[{
            "company": "OldCo",
            "location": "Somewhere",
            "roles": [{
                "title": "Jr Dev",
                "dates": "2010 - 2015",
                "bullets": ["Did things."],
            }],
        }])
        assert estimate_total_lines(tailoring_extra) > estimate_total_lines(tailoring_base)


# ---------------------------------------------------------------------------
# estimate_pages
# ---------------------------------------------------------------------------

class TestEstimatePages:
    """Tests for page count estimation."""

    def test_minimal_is_one_page(self):
        """A minimal tailoring should fit on 1 page."""
        tailoring = _minimal_tailoring()
        assert estimate_pages(tailoring) >= 1

    def test_many_bullets_exceeds_one_page(self):
        """Enough bullets should push to 2+ pages."""
        big_bullets = [f"Bullet {i} with enough text to take up space on the resume." for i in range(30)]
        tailoring = _minimal_tailoring(experience=[{
            "company": "ACME",
            "location": "Remote",
            "roles": [{
                "title": "Senior Engineer",
                "dates": "2020 - 2025",
                "bullets": big_bullets,
            }],
        }])
        assert estimate_pages(tailoring) >= 2

    def test_empty_is_one_page(self):
        """Empty tailoring (just header) should be 1 page."""
        assert estimate_pages({}) == 1
