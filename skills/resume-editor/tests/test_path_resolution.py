"""Tests for resume_builder.py path resolution (Issue #118 / TEST-2).

Verifies that DATA_FILE, RESUME_PATH, and _RESUME_DIR behave correctly
when RESUME_DATA_DIR / RESUME_DOCX_PATH are set to nonexistent paths,
paths with spaces and special characters, or are unset.
"""

import importlib
import json
import sys
from pathlib import Path
from unittest.mock import patch

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))


# ---------------------------------------------------------------------------
# Helpers — reimport the module with patched env vars
# ---------------------------------------------------------------------------

def _reimport_builder(env_overrides: dict[str, str]):
    """Reimport resume_builder with custom env vars and return the module."""
    with patch.dict("os.environ", env_overrides, clear=False):
        # Remove cached module so it re-evaluates module-level constants
        sys.modules.pop("resume_builder", None)
        import resume_builder
        importlib.reload(resume_builder)
        return resume_builder


# ---------------------------------------------------------------------------
# RESUME_DATA_DIR set to nonexistent path
# ---------------------------------------------------------------------------

class TestNonexistentDataDir:
    """RESUME_DATA_DIR pointing to a path that does not exist."""

    def test_data_file_derived_from_nonexistent_dir(self, tmp_path):
        """DATA_FILE should be derived from the env var even if the dir doesn't exist."""
        fake_dir = str(tmp_path / "does_not_exist")
        mod = _reimport_builder({"RESUME_DATA_DIR": fake_dir})
        assert str(mod.DATA_FILE) == str(Path(fake_dir) / "data" / "resume-data.json")
        assert not mod.DATA_FILE.exists()

    def test_load_data_exits_for_nonexistent_dir(self, tmp_path):
        """load_data should exit(1) when DATA_FILE doesn't exist."""
        fake_dir = str(tmp_path / "does_not_exist")
        mod = _reimport_builder({"RESUME_DATA_DIR": fake_dir})
        with pytest.raises(SystemExit) as exc_info:
            mod.load_data()
        assert exc_info.value.code == 1


# ---------------------------------------------------------------------------
# RESUME_DOCX_PATH set to nonexistent path
# ---------------------------------------------------------------------------

class TestNonexistentDocxPath:
    """RESUME_DOCX_PATH pointing to a file that does not exist."""

    def test_resume_path_reflects_env_var(self, tmp_path):
        """RESUME_PATH should use the env var value directly."""
        fake_docx = str(tmp_path / "nonexistent" / "Resume.docx")
        mod = _reimport_builder({"RESUME_DOCX_PATH": fake_docx})
        assert str(mod.RESUME_PATH) == fake_docx
        assert not mod.RESUME_PATH.exists()

    def test_cmd_build_exits_for_nonexistent_docx(self, tmp_path):
        """cmd_build should exit(1) when the base resume docx is missing."""
        import argparse

        fake_docx = str(tmp_path / "nonexistent.docx")
        mod = _reimport_builder({"RESUME_DOCX_PATH": fake_docx})

        # Create a valid tailoring file so we get past that check
        tailoring_file = tmp_path / "tailoring.json"
        tailoring_file.write_text(json.dumps({
            "experience": [{"company": "Test", "roles": []}],
        }))
        output_dir = tmp_path / "output"
        output_dir.mkdir()

        args = argparse.Namespace(
            tailoring_file=str(tailoring_file),
            output_dir=str(output_dir),
        )
        with pytest.raises(SystemExit) as exc_info:
            mod.cmd_build(args)
        assert exc_info.value.code == 1


# ---------------------------------------------------------------------------
# Paths with spaces and special characters
# ---------------------------------------------------------------------------

class TestSpecialCharacterPaths:
    """Paths containing spaces, parentheses, and other special characters."""

    def test_data_dir_with_spaces(self, tmp_path):
        """RESUME_DATA_DIR with spaces should resolve correctly."""
        spaced_dir = tmp_path / "My Resume Data"
        spaced_dir.mkdir()
        mod = _reimport_builder({"RESUME_DATA_DIR": str(spaced_dir)})
        assert mod._RESUME_DIR == spaced_dir
        assert mod.DATA_FILE == spaced_dir / "data" / "resume-data.json"

    def test_data_dir_with_special_chars(self, tmp_path):
        """RESUME_DATA_DIR with parens and ampersands should resolve correctly."""
        special_dir = tmp_path / "Resume (v2) & Backup"
        special_dir.mkdir()
        mod = _reimport_builder({"RESUME_DATA_DIR": str(special_dir)})
        assert mod._RESUME_DIR == special_dir
        assert mod.DATA_FILE == special_dir / "data" / "resume-data.json"

    def test_docx_path_with_spaces(self, tmp_path):
        """RESUME_DOCX_PATH with spaces should resolve correctly."""
        spaced_path = str(tmp_path / "My Documents" / "John Doe Resume.docx")
        mod = _reimport_builder({"RESUME_DOCX_PATH": spaced_path})
        assert str(mod.RESUME_PATH) == spaced_path

    def test_load_data_with_spaced_dir(self, tmp_path):
        """load_data should work when DATA_FILE path has spaces."""
        spaced_dir = tmp_path / "My Resume"
        data_dir = spaced_dir / "data"
        data_dir.mkdir(parents=True)
        data_file = data_dir / "resume-data.json"
        data_file.write_text(json.dumps({"header": {"name": "Test"}, "skills": []}))

        mod = _reimport_builder({"RESUME_DATA_DIR": str(spaced_dir)})
        result = mod.load_data()
        assert result["header"]["name"] == "Test"

    def test_save_data_with_spaced_dir(self, tmp_path):
        """save_data should work when DATA_FILE path has spaces."""
        spaced_dir = tmp_path / "My Resume"
        data_dir = spaced_dir / "data"
        data_dir.mkdir(parents=True)

        mod = _reimport_builder({"RESUME_DATA_DIR": str(spaced_dir)})
        data = {"header": {"name": "Test"}, "skills": []}
        mod.save_data(data)

        loaded = json.loads((data_dir / "resume-data.json").read_text())
        assert loaded == data


# ---------------------------------------------------------------------------
# Graceful error handling
# ---------------------------------------------------------------------------

class TestGracefulErrors:
    """Verify the builder fails gracefully (exits, not crashes) on bad paths."""

    def test_load_data_prints_error_on_missing_file(self, tmp_path, capsys):
        """load_data should print an error message before exiting."""
        fake_dir = str(tmp_path / "gone")
        mod = _reimport_builder({"RESUME_DATA_DIR": fake_dir})
        with pytest.raises(SystemExit):
            mod.load_data()
        captured = capsys.readouterr()
        assert "Error" in captured.out
        assert "not found" in captured.out

    def test_save_data_raises_on_missing_parent(self, tmp_path):
        """save_data should raise FileNotFoundError when parent dir is missing."""
        fake_dir = str(tmp_path / "no" / "such" / "dir")
        mod = _reimport_builder({"RESUME_DATA_DIR": fake_dir})
        with pytest.raises(FileNotFoundError):
            mod.save_data({"header": {"name": "Test"}})

    def test_default_paths_use_home_directory(self):
        """When env vars are unset, paths should default to ~/Resume."""
        # Remove both env vars to test defaults
        env = {"RESUME_DATA_DIR": "", "RESUME_DOCX_PATH": ""}
        with patch.dict("os.environ", env, clear=False):
            # Remove the env vars entirely (empty string != absent)
            import os
            os.environ.pop("RESUME_DATA_DIR", None)
            os.environ.pop("RESUME_DOCX_PATH", None)
            sys.modules.pop("resume_builder", None)
            import resume_builder
            importlib.reload(resume_builder)

        # Should fall back to ~/Resume
        assert str(resume_builder._RESUME_DIR) == str(Path.home() / "Resume")
        assert "Resume" in str(resume_builder.RESUME_PATH)
