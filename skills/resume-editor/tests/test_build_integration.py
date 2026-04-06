"""Integration tests for build and auto-trim commands.

These tests require:
- ~/Resume/MatthewDruhl.docx (base resume)
- ~/Resume/data/resume-data.json (master data)

Tests are skipped if these files don't exist.
"""

import argparse
import json
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))

from resume_builder import DATA_FILE, RESUME_PATH, cmd_auto_trim, cmd_build

# Skip all tests in this module if required files are missing
pytestmark = pytest.mark.skipif(
    not RESUME_PATH.exists() or not DATA_FILE.exists(),
    reason=f"Requires {RESUME_PATH} and {DATA_FILE}",
)


@pytest.fixture
def minimal_tailoring(tmp_path):
    """Create a minimal tailoring file for testing builds."""
    tailoring = {
        "title": "Test Engineer",
        "tagline": "Testing the resume builder",
        "summary": "Experienced engineer with platform and infrastructure expertise.",
        "keywords": ["Python", "SQL", "Linux"],
        "skills": ["Python", "SQL", "Linux", "Docker"],
        "skills_columns": 4,
        "certifications": ["Test Cert, TestOrg (TestPlatform), 2026"],
        "experience": [{
            "company": "TESTCORP",
            "location": "Remote",
            "roles": [{
                "title": "Senior Engineer",
                "type": "Remote",
                "dates": "2020 - 2025",
                "bullets": [
                    "Built infrastructure automation with Terraform.",
                    "Managed Kubernetes clusters serving 2M daily users.",
                ],
            }],
        }],
        "military": {
            "branch": "ARMY NATIONAL GUARD",
            "location": "Iowa City, IA",
            "role": "Medical Specialist",
            "start": "Nov 1993",
            "end": "Nov 2004",
            "bullets": ["Served as combat medic in field operations."],
        },
        "education": [{
            "degree": "Associate of Science (AS)",
            "field": "Computer Science",
            "school": "Test College",
            "location": "Somewhere, USA",
            "years": "1995 - 1997",
        }],
    }
    tailoring_file = tmp_path / "tailoring-test.json"
    tailoring_file.write_text(json.dumps(tailoring, indent=2))
    return tailoring_file, tailoring


class TestBuildMissingFiles:
    """Tests for error handling when required files are missing."""

    def test_missing_base_resume_exits(self, tmp_path):
        """Should sys.exit(1) with clear message when base resume is missing."""
        from unittest.mock import patch

        tailoring_file = tmp_path / "tailoring.json"
        tailoring_file.write_text(json.dumps({"experience": [{"company": "Test", "roles": []}]}))
        output_dir = tmp_path / "output"
        output_dir.mkdir()

        fake_resume = tmp_path / "nonexistent.docx"
        args = argparse.Namespace(
            tailoring_file=str(tailoring_file),
            output_dir=str(output_dir),
        )
        with patch("resume_builder.RESUME_PATH", fake_resume):
            with pytest.raises(SystemExit) as exc_info:
                cmd_build(args)
            assert exc_info.value.code == 1


class TestBuildCommand:
    """Integration tests for the build command."""

    def test_build_produces_docx(self, minimal_tailoring, tmp_path):
        """Build should create a .docx file in the output directory."""
        tailoring_file, _ = minimal_tailoring
        output_dir = tmp_path / "output"
        output_dir.mkdir()

        args = argparse.Namespace(
            tailoring_file=str(tailoring_file),
            output_dir=str(output_dir),
        )
        cmd_build(args)

        docx_files = list(output_dir.glob("Resume-*.docx"))
        assert len(docx_files) == 1, f"Expected 1 docx, got {len(docx_files)}"

    def test_build_filename_contains_company(self, minimal_tailoring, tmp_path):
        """Output filename should contain the company name."""
        tailoring_file, _ = minimal_tailoring
        output_dir = tmp_path / "output"
        output_dir.mkdir()

        args = argparse.Namespace(
            tailoring_file=str(tailoring_file),
            output_dir=str(output_dir),
        )
        cmd_build(args)

        docx_files = list(output_dir.glob("*.docx"))
        assert any("TESTCORP" in f.name for f in docx_files)

    def test_build_docx_not_empty(self, minimal_tailoring, tmp_path):
        """Built docx should have nonzero size."""
        tailoring_file, _ = minimal_tailoring
        output_dir = tmp_path / "output"
        output_dir.mkdir()

        args = argparse.Namespace(
            tailoring_file=str(tailoring_file),
            output_dir=str(output_dir),
        )
        cmd_build(args)

        docx_files = list(output_dir.glob("*.docx"))
        assert docx_files[0].stat().st_size > 1000  # at least 1KB


class TestAutoTrimCommand:
    """Integration tests for the auto-trim command."""

    def test_auto_trim_produces_output(self, minimal_tailoring, tmp_path):
        """Auto-trim should produce both a docx and a trimmed tailoring file."""
        tailoring_file, _ = minimal_tailoring
        output_dir = tmp_path / "output"
        output_dir.mkdir()

        args = argparse.Namespace(
            tailoring_file=str(tailoring_file),
            output_dir=str(output_dir),
            keywords="Python,SQL,Linux",
            max_pages=2,
            company="",
        )
        cmd_auto_trim(args)

        docx_files = list(output_dir.glob("Resume-*.docx"))
        assert len(docx_files) >= 1

        trimmed = output_dir / "tailoring-trimmed.json"
        assert trimmed.exists()

    def test_auto_trim_saves_valid_json(self, minimal_tailoring, tmp_path):
        """The trimmed tailoring file should be valid JSON."""
        tailoring_file, _ = minimal_tailoring
        output_dir = tmp_path / "output"
        output_dir.mkdir()

        args = argparse.Namespace(
            tailoring_file=str(tailoring_file),
            output_dir=str(output_dir),
            keywords="Python,SQL",
            max_pages=2,
            company="",
        )
        cmd_auto_trim(args)

        trimmed = output_dir / "tailoring-trimmed.json"
        data = json.loads(trimmed.read_text())
        assert "experience" in data

    def test_auto_trim_with_company_rename(self, minimal_tailoring, tmp_path):
        """Auto-trim with --company should rename the output file."""
        tailoring_file, _ = minimal_tailoring
        output_dir = tmp_path / "output"
        output_dir.mkdir()

        args = argparse.Namespace(
            tailoring_file=str(tailoring_file),
            output_dir=str(output_dir),
            keywords="Python",
            max_pages=2,
            company="CustomName",
        )
        cmd_auto_trim(args)

        docx_files = list(output_dir.glob("*.docx"))
        assert any("CUSTOMNAME" in f.name for f in docx_files)

    def test_auto_trim_respects_min_bullets(self, tmp_path):
        """Auto-trim should never leave a role with 0 bullets, even with tight page limit."""
        tailoring = {
            "summary": "Test",
            "keywords": [],
            "skills": ["Python"],
            "certifications": [],
            "experience": [{
                "company": "TESTCORP",
                "location": "Remote",
                "roles": [{
                    "title": "Dev",
                    "dates": "2020 - 2025",
                    "bullets": [
                        "Bullet one about nothing relevant.",
                        "Bullet two about nothing relevant.",
                    ],
                }],
            }],
            "education": [{
                "degree": "AS",
                "field": "CS",
                "school": "Test",
                "location": "USA",
                "years": "1995 - 1997",
            }],
        }
        tailoring_file = tmp_path / "tailoring.json"
        tailoring_file.write_text(json.dumps(tailoring))
        output_dir = tmp_path / "output"
        output_dir.mkdir()

        args = argparse.Namespace(
            tailoring_file=str(tailoring_file),
            output_dir=str(output_dir),
            keywords="Python,SQL,Linux,Terraform,Kubernetes",
            max_pages=1,
            company="",
        )
        cmd_auto_trim(args)

        # Verify the trimmed file still has at least 1 bullet per role
        trimmed = json.loads((output_dir / "tailoring-trimmed.json").read_text())
        for comp in trimmed.get("experience", []):
            for role in comp.get("roles", []):
                assert len(role.get("bullets", [])) >= 1, (
                    f"Role '{role['title']}' at '{comp['company']}' has 0 bullets"
                )
