"""Tests for update_resume.py — unit tests for path construction, backup naming,
data loading, section parsing, and error paths.

Does NOT require ~/Resume/MatthewDruhl.docx to exist — all tests use tmp_path
fixtures or mocks.
"""

import sys
from datetime import datetime
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))

from update_resume import (
    BACKUP_DIR,
    CERTS_DIR,
    KNOWN_SECTION_HEADERS,
    RESUME_PATH,
    TEMPLATE_PATH,
    _parse_cert_date,
    cmd_backup,
    cmd_scan_certs,
    cmd_show_certs,
    cmd_show_skills,
    safe_save,
)

# ---------------------------------------------------------------------------
# Path constants
# ---------------------------------------------------------------------------

class TestPathConstants:
    """Verify path construction is consistent."""

    def test_resume_path_under_home(self):
        """RESUME_PATH should be under ~/Resume/."""
        assert RESUME_PATH.parent == Path.home() / "Resume"

    def test_template_path_under_home(self):
        """TEMPLATE_PATH should be under ~/Resume/original/."""
        assert TEMPLATE_PATH.parent == Path.home() / "Resume" / "original"

    def test_backup_dir_under_home(self):
        """BACKUP_DIR should be under ~/Resume/backup/."""
        assert BACKUP_DIR == Path.home() / "Resume" / "backup"

    def test_certs_dir_under_home(self):
        """CERTS_DIR should be under ~/Resume/certs/."""
        assert CERTS_DIR == Path.home() / "Resume" / "certs"


# ---------------------------------------------------------------------------
# _parse_cert_date
# ---------------------------------------------------------------------------

class TestParseCertDate:
    """Tests for the cert date parser used in sorting."""

    def test_valid_date(self):
        """'Feb 2026' should parse to Feb 2026."""
        result = _parse_cert_date("Feb 2026")
        assert result.year == 2026
        assert result.month == 2

    def test_valid_date_with_whitespace(self):
        """Leading/trailing whitespace should be stripped."""
        result = _parse_cert_date("  Mar 2025  ")
        assert result.year == 2025
        assert result.month == 3

    def test_invalid_date_returns_min(self):
        """Invalid date strings should return datetime.min (sorts last)."""
        result = _parse_cert_date("not-a-date")
        assert result == datetime.min

    def test_empty_string_returns_min(self):
        """Empty string should return datetime.min."""
        result = _parse_cert_date("")
        assert result == datetime.min


# ---------------------------------------------------------------------------
# safe_save
# ---------------------------------------------------------------------------

class TestSafeSave:
    """Tests for safe_save — handles read-only files."""

    def test_save_to_writable_file(self, tmp_path):
        """Should save normally when file is writable."""
        output = tmp_path / "test.docx"
        doc = MagicMock()
        safe_save(doc, output)
        doc.save.assert_called_once_with(str(output))

    def test_save_to_readonly_file(self, tmp_path):
        """Should temporarily make file writable, save, then restore readonly."""
        output = tmp_path / "test.docx"
        output.write_text("placeholder")
        # Make read-only
        output.chmod(0o444)

        doc = MagicMock()
        safe_save(doc, output)
        doc.save.assert_called_once_with(str(output))

        # Verify file is read-only again
        import stat
        mode = output.stat().st_mode
        assert not (mode & stat.S_IWUSR)

        # Cleanup: make writable so tmp_path cleanup works
        output.chmod(0o644)

    def test_save_to_nonexistent_file(self, tmp_path):
        """Should save even when file doesn't exist yet."""
        output = tmp_path / "new_file.docx"
        doc = MagicMock()
        safe_save(doc, output)
        doc.save.assert_called_once_with(str(output))


# ---------------------------------------------------------------------------
# KNOWN_SECTION_HEADERS
# ---------------------------------------------------------------------------

class TestKnownSectionHeaders:
    """Verify the expected section headers are defined."""

    def test_required_sections_present(self):
        """All standard resume sections should be in the known set."""
        required = {
            "technical skills",
            "certifications",
            "professional experience",
            "education",
        }
        assert required.issubset(KNOWN_SECTION_HEADERS)

    def test_all_lowercase(self):
        """All entries should be lowercase for case-insensitive matching."""
        for header in KNOWN_SECTION_HEADERS:
            assert header == header.lower()


# ---------------------------------------------------------------------------
# cmd_backup
# ---------------------------------------------------------------------------

class TestCmdBackup:
    """Tests for the backup command."""

    def test_backup_missing_resume_exits(self, tmp_path, capsys):
        """Should exit when resume file doesn't exist."""
        fake_resume = tmp_path / "nonexistent.docx"
        with patch("update_resume.RESUME_PATH", fake_resume):
            with pytest.raises(SystemExit) as exc_info:
                cmd_backup(MagicMock())
            assert exc_info.value.code == 1

    def test_backup_creates_file(self, tmp_path):
        """Should create a timestamped backup copy."""
        fake_resume = tmp_path / "TestResume.docx"
        fake_resume.write_text("fake docx content")
        backup_dir = tmp_path / "backup"

        with patch("update_resume.RESUME_PATH", fake_resume), \
             patch("update_resume.BACKUP_DIR", backup_dir):
            cmd_backup(MagicMock())

        backups = list(backup_dir.glob("*.docx"))
        assert len(backups) == 1
        assert "MatthewDruhl_" in backups[0].name


# ---------------------------------------------------------------------------
# cmd_scan_certs
# ---------------------------------------------------------------------------

class TestCmdScanCerts:
    """Tests for the scan-certs command."""

    def test_no_pdfs_prints_message(self, tmp_path, capsys):
        """Should print 'No PDF files found' when certs directory is empty."""
        empty_certs = tmp_path / "certs"
        empty_certs.mkdir()
        with patch("update_resume.CERTS_DIR", empty_certs):
            cmd_scan_certs(MagicMock())
        captured = capsys.readouterr()
        assert "No PDF files found" in captured.out


# ---------------------------------------------------------------------------
# cmd_show_certs / cmd_show_skills
# ---------------------------------------------------------------------------

class TestCmdShowCerts:
    """Tests for the show-certs command."""

    def test_missing_resume_exits(self, tmp_path):
        """Should exit when resume file doesn't exist."""
        fake_resume = tmp_path / "nonexistent.docx"
        with patch("update_resume.RESUME_PATH", fake_resume):
            with pytest.raises(SystemExit) as exc_info:
                cmd_show_certs(MagicMock())
            assert exc_info.value.code == 1


class TestCmdShowSkills:
    """Tests for the show-skills command."""

    def test_missing_resume_exits(self, tmp_path):
        """Should exit when resume file doesn't exist."""
        fake_resume = tmp_path / "nonexistent.docx"
        with patch("update_resume.RESUME_PATH", fake_resume):
            with pytest.raises(SystemExit) as exc_info:
                cmd_show_skills(MagicMock())
            assert exc_info.value.code == 1
