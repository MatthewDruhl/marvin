"""Integration tests for the cover-letter command.

No external dependencies required — builds from scratch using python-docx.
"""

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))

from resume_builder import cmd_cover_letter


class TestCoverLetterCommand:
    """Integration tests for cover letter generation."""

    def test_creates_docx(self, tmp_path):
        """Should create a .docx file in the output directory."""
        body_file = tmp_path / "body.txt"
        body_file.write_text(
            "I am writing to express my interest in the Engineer role.\n\n"
            "My experience aligns well with your requirements."
        )
        output_dir = tmp_path / "output"
        output_dir.mkdir()

        args = argparse.Namespace(
            company="TestCorp",
            job_title="Senior Engineer",
            body_file=str(body_file),
            output_dir=str(output_dir),
            date="April 5, 2026",
        )
        cmd_cover_letter(args)

        docx_files = list(output_dir.glob("CoverLetter-*.docx"))
        assert len(docx_files) == 1

    def test_filename_contains_company(self, tmp_path):
        """Output filename should include the company name."""
        body_file = tmp_path / "body.txt"
        body_file.write_text("Test body paragraph.")
        output_dir = tmp_path / "output"
        output_dir.mkdir()

        args = argparse.Namespace(
            company="Acme Inc",
            job_title="Dev",
            body_file=str(body_file),
            output_dir=str(output_dir),
            date="",
        )
        cmd_cover_letter(args)

        docx_files = list(output_dir.glob("*.docx"))
        assert any("AcmeInc" in f.name for f in docx_files)

    def test_missing_body_file_exits(self, tmp_path):
        """Should sys.exit(1) when body file doesn't exist."""
        import pytest

        output_dir = tmp_path / "output"
        output_dir.mkdir()

        args = argparse.Namespace(
            company="TestCorp",
            job_title="Dev",
            body_file=str(tmp_path / "nonexistent.txt"),
            output_dir=str(output_dir),
            date="",
        )
        with pytest.raises(SystemExit) as exc_info:
            cmd_cover_letter(args)
        assert exc_info.value.code == 1

    def test_default_date_used(self, tmp_path):
        """When date is empty, should use today's date (doesn't crash)."""
        body_file = tmp_path / "body.txt"
        body_file.write_text("Test body.")
        output_dir = tmp_path / "output"
        output_dir.mkdir()

        args = argparse.Namespace(
            company="TestCorp",
            job_title="Dev",
            body_file=str(body_file),
            output_dir=str(output_dir),
            date="",  # should default to today
        )
        # Should not raise
        cmd_cover_letter(args)

        docx_files = list(output_dir.glob("*.docx"))
        assert len(docx_files) == 1

    def test_docx_not_empty(self, tmp_path):
        """Generated docx should have reasonable size."""
        body_file = tmp_path / "body.txt"
        body_file.write_text(
            "First paragraph.\n\n"
            "Second paragraph.\n\n"
            "Third paragraph."
        )
        output_dir = tmp_path / "output"
        output_dir.mkdir()

        args = argparse.Namespace(
            company="TestCorp",
            job_title="Dev",
            body_file=str(body_file),
            output_dir=str(output_dir),
            date="April 5, 2026",
        )
        cmd_cover_letter(args)

        docx_files = list(output_dir.glob("*.docx"))
        assert docx_files[0].stat().st_size > 500  # at least 500 bytes
