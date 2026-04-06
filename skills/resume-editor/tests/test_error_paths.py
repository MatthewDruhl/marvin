"""Error path tests for resume_builder.py (Issue #41).

Tests for missing files, malformed JSON, and other failure modes
that the existing happy-path tests don't cover.
"""

import argparse
import json
import sys
from pathlib import Path
from unittest.mock import patch

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))

from resume_builder import (
    cmd_build,
    cmd_cover_letter,
    cmd_update,
    get_filename_prefix,
    get_header,
    load_data,
    load_tailoring,
    save_data,
    score_bullet,
    score_tailoring,
)

# ---------------------------------------------------------------------------
# load_data error paths
# ---------------------------------------------------------------------------

class TestLoadDataErrors:
    """Error paths for load_data."""

    def test_missing_file_exits_with_code_1(self, tmp_path):
        fake = tmp_path / "nonexistent.json"
        with patch("resume_builder.DATA_FILE", fake):
            with pytest.raises(SystemExit) as exc_info:
                load_data()
            assert exc_info.value.code == 1

    def test_malformed_json_raises(self, tmp_path):
        bad_file = tmp_path / "bad.json"
        bad_file.write_text("{this is not valid json!!!")
        with patch("resume_builder.DATA_FILE", bad_file):
            with pytest.raises(json.JSONDecodeError):
                load_data()

    def test_empty_file_raises(self, tmp_path):
        empty_file = tmp_path / "empty.json"
        empty_file.write_text("")
        with patch("resume_builder.DATA_FILE", empty_file):
            with pytest.raises(json.JSONDecodeError):
                load_data()

    def test_permission_error(self, tmp_path):
        """Unreadable file should raise PermissionError."""
        restricted = tmp_path / "restricted.json"
        restricted.write_text('{"test": true}')
        restricted.chmod(0o000)
        try:
            with patch("resume_builder.DATA_FILE", restricted):
                with pytest.raises(PermissionError):
                    load_data()
        finally:
            restricted.chmod(0o644)


# ---------------------------------------------------------------------------
# load_tailoring error paths
# ---------------------------------------------------------------------------

class TestLoadTailoringErrors:
    """Error paths for load_tailoring."""

    def test_missing_file_exits(self, tmp_path):
        with pytest.raises(SystemExit) as exc_info:
            load_tailoring(str(tmp_path / "nonexistent.json"))
        assert exc_info.value.code == 1

    def test_malformed_json_raises(self, tmp_path):
        bad = tmp_path / "bad.json"
        bad.write_text("not json")
        with pytest.raises(json.JSONDecodeError):
            load_tailoring(str(bad))

    def test_empty_file_raises(self, tmp_path):
        empty = tmp_path / "empty.json"
        empty.write_text("")
        with pytest.raises(json.JSONDecodeError):
            load_tailoring(str(empty))


# ---------------------------------------------------------------------------
# save_data error paths
# ---------------------------------------------------------------------------

class TestSaveDataErrors:
    """Error paths for save_data."""

    def test_nonexistent_directory_raises(self, tmp_path):
        """Writing to a path whose parent doesn't exist should raise."""
        bad_path = tmp_path / "nonexistent_dir" / "data.json"
        with patch("resume_builder.DATA_FILE", bad_path):
            with pytest.raises(FileNotFoundError):
                save_data({"header": {"name": "Test"}})

    def test_readonly_directory_raises(self, tmp_path):
        """Writing to a read-only directory should raise."""
        readonly_dir = tmp_path / "readonly"
        readonly_dir.mkdir()
        readonly_dir.chmod(0o555)
        data_file = readonly_dir / "data.json"
        try:
            with patch("resume_builder.DATA_FILE", data_file):
                with pytest.raises(PermissionError):
                    save_data({"header": {"name": "Test"}})
        finally:
            readonly_dir.chmod(0o755)


# ---------------------------------------------------------------------------
# cmd_build error paths
# ---------------------------------------------------------------------------

class TestCmdBuildErrors:
    """Error paths for the build command."""

    def test_missing_base_resume_exits(self, tmp_path):
        """Should exit when base resume .docx doesn't exist."""
        tailoring_file = tmp_path / "tailoring.json"
        tailoring_file.write_text(json.dumps({
            "experience": [{"company": "Test", "roles": []}],
        }))
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

    def test_missing_tailoring_file_exits(self, tmp_path):
        """Should exit when tailoring file doesn't exist."""
        args = argparse.Namespace(
            tailoring_file=str(tmp_path / "nonexistent.json"),
            output_dir=str(tmp_path),
        )
        with pytest.raises(SystemExit) as exc_info:
            cmd_build(args)
        assert exc_info.value.code == 1


# ---------------------------------------------------------------------------
# cmd_cover_letter error paths
# ---------------------------------------------------------------------------

class TestCmdCoverLetterErrors:
    """Error paths for the cover-letter command."""

    def test_missing_body_file_exits(self, tmp_path):
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


# ---------------------------------------------------------------------------
# cmd_update error paths
# ---------------------------------------------------------------------------

class TestCmdUpdateErrors:
    """Error paths for the update command."""

    def test_add_duplicate_skill_no_save(self, tmp_path, capsys):
        """Adding a skill that already exists should print message, not save."""
        data = {
            "header": {"name": "Test"},
            "skills": [{"name": "Python", "categories": ["language"]}],
        }
        data_file = tmp_path / "data.json"
        data_file.write_text(json.dumps(data))

        args = argparse.Namespace(
            update_command="add-skill",
            name="Python",
            categories="language",
        )
        with patch("resume_builder.DATA_FILE", data_file):
            cmd_update(args)

        captured = capsys.readouterr()
        assert "already exists" in captured.out

    def test_add_bullet_nonexistent_role(self, tmp_path, capsys):
        """Adding a bullet to a nonexistent role should print error."""
        data = {
            "header": {"name": "Test"},
            "skills": [],
            "experience": [{
                "company": "Acme",
                "roles": [{"title": "Dev", "bullets": []}],
            }],
            "additional_experience": [],
        }
        data_file = tmp_path / "data.json"
        data_file.write_text(json.dumps(data))

        args = argparse.Namespace(
            update_command="add-bullet",
            role="NonexistentRole",
            text="A bullet",
            tags="test",
        )
        with patch("resume_builder.DATA_FILE", data_file):
            cmd_update(args)

        captured = capsys.readouterr()
        assert "not found" in captured.out


# ---------------------------------------------------------------------------
# get_header / get_filename_prefix error paths
# ---------------------------------------------------------------------------

class TestGetHeaderErrors:
    """Error paths for header loading."""

    def test_missing_data_file_exits(self, tmp_path):
        with patch("resume_builder.DATA_FILE", tmp_path / "nonexistent.json"):
            with pytest.raises(SystemExit):
                get_header()

    def test_missing_name_uses_default_prefix(self, tmp_path):
        """get_filename_prefix should use 'Resume' when name is missing."""
        data = {"header": {}, "skills": []}
        data_file = tmp_path / "data.json"
        data_file.write_text(json.dumps(data))
        with patch("resume_builder.DATA_FILE", data_file):
            prefix = get_filename_prefix()
        assert prefix == "RESUME"


# ---------------------------------------------------------------------------
# score_bullet edge cases
# ---------------------------------------------------------------------------

class TestScoreBulletEdgeCases:
    """Edge cases for bullet scoring."""

    def test_none_like_empty_bullet(self):
        """Empty bullet text should score 0."""
        assert score_bullet("", ["Python", "SQL"]) == 0.0

    def test_special_regex_chars_in_keywords(self):
        """Keywords with regex-special chars should not crash (re.escape handles them).

        Note: Word-boundary matching with \\b doesn't work well for keywords
        ending in non-word chars like C++ or C#, since \\b requires a word char
        on one side. These keywords score 0 — this documents the current behavior.
        """
        # Should not raise even with regex-special characters
        score = score_bullet("Used C++ and C# daily", ["C++", "C#"])
        assert score == 0.0  # known limitation: \b can't match C++ or C#

    def test_single_keyword_full_match(self):
        """Single keyword that matches should return 1.0."""
        assert score_bullet("Built Python scripts", ["Python"]) == 1.0

    def test_single_keyword_no_match(self):
        """Single keyword that doesn't match should return 0.0."""
        assert score_bullet("Built shell scripts", ["Python"]) == 0.0


# ---------------------------------------------------------------------------
# score_tailoring edge cases
# ---------------------------------------------------------------------------

class TestScoreTailoringEdgeCases:
    """Edge cases for tailoring scoring."""

    def test_empty_tailoring_returns_empty(self):
        assert score_tailoring({}, ["Python"]) == []

    def test_roles_with_no_bullets(self):
        """Roles with empty bullet lists should not crash."""
        tailoring = {
            "experience": [{
                "company": "Acme",
                "roles": [{"title": "Dev", "bullets": []}],
            }],
        }
        scored = score_tailoring(tailoring, ["Python"])
        assert scored == []

    def test_military_with_no_bullets(self):
        """Military section with empty bullets should not crash."""
        tailoring = {
            "military": {"branch": "Army", "role": "Medic", "bullets": []},
        }
        scored = score_tailoring(tailoring, ["Python"])
        assert scored == []
