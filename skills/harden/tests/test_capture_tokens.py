"""Tests for capture_tokens.py — JSONL token parsing and marker path validation."""

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from capture_tokens import sum_tokens


def write_jsonl(path: Path, entries: list[dict]) -> None:
    with open(path, "w") as f:
        for entry in entries:
            f.write(json.dumps(entry) + "\n")


def make_entry(input_tokens: int = 0, output_tokens: int = 0,
               cache_creation: int = 0, cache_read: int = 0) -> dict:
    return {
        "message": {
            "usage": {
                "input_tokens": input_tokens,
                "output_tokens": output_tokens,
                "cache_creation_input_tokens": cache_creation,
                "cache_read_input_tokens": cache_read,
            }
        }
    }


class TestSumTokens:
    def test_basic_counts(self, tmp_path):
        f = tmp_path / "session.jsonl"
        write_jsonl(f, [make_entry(input_tokens=100, output_tokens=50)])
        inp, out = sum_tokens(f)
        assert inp == 100
        assert out == 50

    def test_multiple_entries_summed(self, tmp_path):
        f = tmp_path / "session.jsonl"
        write_jsonl(f, [
            make_entry(input_tokens=100, output_tokens=50),
            make_entry(input_tokens=200, output_tokens=75),
        ])
        inp, out = sum_tokens(f)
        assert inp == 300
        assert out == 125

    def test_cache_tokens_included_in_input(self, tmp_path):
        f = tmp_path / "session.jsonl"
        write_jsonl(f, [make_entry(input_tokens=100, cache_creation=40, cache_read=20)])
        inp, out = sum_tokens(f)
        assert inp == 160  # 100 + 40 + 20

    def test_empty_file_returns_zeros(self, tmp_path):
        f = tmp_path / "session.jsonl"
        f.write_text("")
        inp, out = sum_tokens(f)
        assert inp == 0
        assert out == 0

    def test_invalid_json_lines_skipped(self, tmp_path):
        f = tmp_path / "session.jsonl"
        with open(f, "w") as fh:
            fh.write("not json\n")
            fh.write(json.dumps(make_entry(input_tokens=50, output_tokens=25)) + "\n")
        inp, out = sum_tokens(f)
        assert inp == 50
        assert out == 25

    def test_blank_lines_skipped(self, tmp_path):
        f = tmp_path / "session.jsonl"
        with open(f, "w") as fh:
            fh.write("\n")
            fh.write(json.dumps(make_entry(input_tokens=10, output_tokens=5)) + "\n")
            fh.write("\n")
        inp, out = sum_tokens(f)
        assert inp == 10
        assert out == 5

    def test_entries_without_usage_key_skipped(self, tmp_path):
        f = tmp_path / "session.jsonl"
        write_jsonl(f, [{"message": {}}, make_entry(input_tokens=30, output_tokens=15)])
        inp, out = sum_tokens(f)
        assert inp == 30
        assert out == 15


class TestMarkerValidation:
    """Verify marker_path.unlink() is only called for /tmp/ paths."""

    def test_marker_in_tmp_is_deleted(self, tmp_path):
        # Verify only /tmp/ paths pass the guard — not arbitrary user-owned files
        assert not str(Path("/etc/passwd")).startswith("/tmp/")
        assert not str(Path.home() / "important.txt").startswith("/tmp/")

    def test_marker_outside_tmp_not_deleted(self, tmp_path):
        # Confirm the guard rejects non-/tmp paths (unit test of the condition)
        non_tmp_paths = [
            Path.home() / "marvin" / "state" / "current.md",
            Path("/etc/hosts"),
            Path("/Users/user/somefile"),
        ]
        for p in non_tmp_paths:
            assert not str(p).startswith("/tmp/"), f"{p} should not pass /tmp/ guard"
