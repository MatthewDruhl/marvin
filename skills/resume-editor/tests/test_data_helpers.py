"""Tests for data loading/saving helpers in resume_builder.py."""

import json
import sys
from pathlib import Path
from unittest.mock import patch

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))

from resume_builder import load_data, load_tailoring, save_data


class TestLoadData:
    """Tests for the master resume data loader."""

    def test_missing_file_exits(self, tmp_path):
        """Should sys.exit(1) when data file doesn't exist."""
        fake_path = tmp_path / "nonexistent.json"
        with patch("resume_builder.DATA_FILE", fake_path):
            with pytest.raises(SystemExit) as exc_info:
                load_data()
            assert exc_info.value.code == 1

    def test_valid_json_loads(self, tmp_path):
        """Should load and return valid JSON data."""
        data = {"header": {"name": "Test"}, "skills": []}
        data_file = tmp_path / "resume-data.json"
        data_file.write_text(json.dumps(data))
        with patch("resume_builder.DATA_FILE", data_file):
            result = load_data()
        assert result == data

    def test_malformed_json_raises(self, tmp_path):
        """Malformed JSON should raise an error."""
        data_file = tmp_path / "resume-data.json"
        data_file.write_text("{broken json")
        with patch("resume_builder.DATA_FILE", data_file):
            with pytest.raises(json.JSONDecodeError):
                load_data()


class TestLoadTailoring:
    """Tests for the tailoring file loader."""

    def test_missing_file_exits(self, tmp_path):
        """Should sys.exit(1) when tailoring file doesn't exist."""
        with pytest.raises(SystemExit) as exc_info:
            load_tailoring(str(tmp_path / "nonexistent.json"))
        assert exc_info.value.code == 1

    def test_valid_file_loads(self, tmp_path):
        """Should load and return valid tailoring JSON."""
        data = {"title": "Test Engineer", "summary": "Test summary"}
        f = tmp_path / "tailoring.json"
        f.write_text(json.dumps(data))
        result = load_tailoring(str(f))
        assert result == data


class TestSaveData:
    """Tests for the data saver."""

    def test_round_trip(self, tmp_path):
        """Save then load should return identical data."""
        data = {
            "header": {"name": "Matt"},
            "skills": [{"name": "Python", "categories": ["language"]}],
        }
        data_file = tmp_path / "resume-data.json"
        with patch("resume_builder.DATA_FILE", data_file):
            save_data(data)
            result = load_data()
        assert result == data

    def test_unicode_preserved(self, tmp_path):
        """Unicode characters should survive save/load."""
        data = {"header": {"name": "Matt"}, "notes": "2020 \u2013 2025"}
        data_file = tmp_path / "resume-data.json"
        with patch("resume_builder.DATA_FILE", data_file):
            save_data(data)
            result = load_data()
        assert result["notes"] == "2020 \u2013 2025"

    def test_file_ends_with_newline(self, tmp_path):
        """Saved file should end with a newline (clean git diffs)."""
        data = {"header": {"name": "Matt"}}
        data_file = tmp_path / "resume-data.json"
        with patch("resume_builder.DATA_FILE", data_file):
            save_data(data)
        content = data_file.read_text()
        assert content.endswith("\n")
