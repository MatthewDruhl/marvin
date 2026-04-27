"""Tests for harden-recon.py — static Pass 1 candidate scanner."""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path

# ---------------------------------------------------------------------------
# Import harden-recon module (hyphenated name requires importlib)
# ---------------------------------------------------------------------------

_RECON_PATH = Path(__file__).parent.parent / "harden-recon.py"
_spec = importlib.util.spec_from_file_location("harden_recon", _RECON_PATH)
_mod = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_mod)

run_recon = _mod.run_recon
format_markdown = _mod.format_markdown
format_json = _mod.format_json
main = _mod.main


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _write(tmp_path: Path, name: str, content: str) -> Path:
    p = tmp_path / name
    p.write_text(content, encoding="utf-8")
    return p


def _candidates(result, category: str):
    return [c for c in result.candidates if c.category == category]


# ---------------------------------------------------------------------------
# Secret detection
# ---------------------------------------------------------------------------

class TestSecretDetection:
    def test_detects_hardcoded_api_key(self, tmp_path):
        _write(tmp_path, "config.py", 'api_key = "sk-abc123"\n')
        result = run_recon(tmp_path)
        hits = _candidates(result, "secrets")
        assert len(hits) == 1
        assert hits[0].line == 1
        assert "api_key" in hits[0].detail

    def test_detects_hardcoded_password(self, tmp_path):
        _write(tmp_path, "db.py", "password = 'hunter2'\n")
        result = run_recon(tmp_path)
        hits = _candidates(result, "secrets")
        assert any("password" in h.detail for h in hits)

    def test_does_not_flag_env_lookup(self, tmp_path):
        _write(tmp_path, "config.py", "api_key = os.environ.get('API_KEY')\n")
        result = run_recon(tmp_path)
        hits = _candidates(result, "secrets")
        assert len(hits) == 0

    def test_does_not_flag_config_dict_lookup(self, tmp_path):
        _write(tmp_path, "config.py", 'api_key = config["API_KEY"]\n')
        result = run_recon(tmp_path)
        hits = _candidates(result, "secrets")
        assert len(hits) == 0

    def test_does_not_flag_variable_name_alone(self, tmp_path):
        # Just a variable name reference, not an assignment with a literal
        _write(tmp_path, "util.py", "def get_token(token):\n    return token\n")
        result = run_recon(tmp_path)
        hits = _candidates(result, "secrets")
        assert len(hits) == 0

    def test_detects_token_assignment(self, tmp_path):
        _write(tmp_path, "auth.py", 'auth_token = "Bearer xyz"\n')
        result = run_recon(tmp_path)
        hits = _candidates(result, "secrets")
        assert len(hits) == 1

    def test_records_correct_line_number(self, tmp_path):
        content = "# comment\n# another\napi_key = 'secret-value'\n"
        _write(tmp_path, "app.py", content)
        result = run_recon(tmp_path)
        hits = _candidates(result, "secrets")
        assert hits[0].line == 3


# ---------------------------------------------------------------------------
# Bare except detection
# ---------------------------------------------------------------------------

class TestBareExceptDetection:
    def test_detects_bare_except(self, tmp_path):
        code = "try:\n    x = 1\nexcept:\n    pass\n"
        _write(tmp_path, "app.py", code)
        result = run_recon(tmp_path)
        hits = _candidates(result, "bare_excepts")
        assert len(hits) == 1

    def test_detects_except_exception(self, tmp_path):
        code = "try:\n    x = 1\nexcept Exception:\n    pass\n"
        _write(tmp_path, "app.py", code)
        result = run_recon(tmp_path)
        hits = _candidates(result, "bare_excepts")
        assert len(hits) == 1

    def test_does_not_flag_except_with_reraise(self, tmp_path):
        code = "try:\n    x = 1\nexcept:\n    raise\n"
        _write(tmp_path, "app.py", code)
        result = run_recon(tmp_path)
        hits = _candidates(result, "bare_excepts")
        assert len(hits) == 0

    def test_does_not_flag_except_with_logging(self, tmp_path):
        code = "try:\n    x = 1\nexcept:\n    logger.error('failed')\n"
        _write(tmp_path, "app.py", code)
        result = run_recon(tmp_path)
        hits = _candidates(result, "bare_excepts")
        assert len(hits) == 0

    def test_does_not_flag_specific_exception(self, tmp_path):
        code = "try:\n    x = 1\nexcept ValueError:\n    pass\n"
        _write(tmp_path, "app.py", code)
        result = run_recon(tmp_path)
        hits = _candidates(result, "bare_excepts")
        assert len(hits) == 0


# ---------------------------------------------------------------------------
# Hardcoded IP detection
# ---------------------------------------------------------------------------

class TestHardcodedIPDetection:
    def test_detects_hardcoded_ip(self, tmp_path):
        _write(tmp_path, "config.py", 'HOST = "192.168.1.1"\n')
        result = run_recon(tmp_path)
        hits = _candidates(result, "hardcoded_values")
        ip_hits = [h for h in hits if "192.168.1.1" in h.detail]
        assert len(ip_hits) == 1

    def test_detects_public_ip(self, tmp_path):
        _write(tmp_path, "settings.py", "server = '10.0.0.1'\n")
        result = run_recon(tmp_path)
        hits = _candidates(result, "hardcoded_values")
        assert any("10.0.0.1" in h.detail for h in hits)

    def test_does_not_flag_invalid_ip(self, tmp_path):
        # 999.999.999.999 is not a valid IP
        _write(tmp_path, "app.py", "x = '999.999.999.999'\n")
        result = run_recon(tmp_path)
        hits = _candidates(result, "hardcoded_values")
        ip_hits = [h for h in hits if "999.999.999.999" in h.detail]
        assert len(ip_hits) == 0

    def test_records_correct_line(self, tmp_path):
        content = "# header\nHOST = '127.0.0.1'\n"
        _write(tmp_path, "cfg.py", content)
        result = run_recon(tmp_path)
        hits = _candidates(result, "hardcoded_values")
        ip_hits = [h for h in hits if "127.0.0.1" in h.detail]
        assert ip_hits[0].line == 2


# ---------------------------------------------------------------------------
# Test gap detection
# ---------------------------------------------------------------------------

class TestTestGapDetection:
    def test_flags_src_file_without_test(self, tmp_path):
        src = tmp_path / "src"
        src.mkdir()
        _write(src, "module.py", "def foo(): pass\n")
        result = run_recon(tmp_path)
        hits = _candidates(result, "test_gaps")
        assert any("module.py" in h.file for h in hits)

    def test_does_not_flag_file_with_test(self, tmp_path):
        src = tmp_path / "src"
        src.mkdir()
        _write(src, "module.py", "def foo(): pass\n")
        tests = tmp_path / "tests"
        tests.mkdir()
        _write(tests, "test_module.py", "def test_foo(): pass\n")
        result = run_recon(tmp_path)
        hits = _candidates(result, "test_gaps")
        assert not any("module.py" in h.file and "src" in h.file for h in hits)

    def test_does_not_flag_test_files_themselves(self, tmp_path):
        tests = tmp_path / "tests"
        tests.mkdir()
        _write(tests, "test_something.py", "def test_it(): pass\n")
        result = run_recon(tmp_path)
        hits = _candidates(result, "test_gaps")
        assert not any("test_something.py" in h.file for h in hits)

    def test_flags_root_level_py_without_test(self, tmp_path):
        _write(tmp_path, "script.py", "def run(): pass\n")
        result = run_recon(tmp_path)
        hits = _candidates(result, "test_gaps")
        assert any("script.py" in h.file for h in hits)


# ---------------------------------------------------------------------------
# Large file detection
# ---------------------------------------------------------------------------

class TestLargeFileDetection:
    def test_flags_large_file_without_test(self, tmp_path):
        # Write a file with 301 lines
        content = "\n".join(f"x_{i} = {i}" for i in range(301)) + "\n"
        _write(tmp_path, "big_module.py", content)
        result = run_recon(tmp_path)
        hits = _candidates(result, "large_files")
        assert any("big_module.py" in h.file for h in hits)

    def test_does_not_flag_small_file(self, tmp_path):
        content = "\n".join(f"x_{i} = {i}" for i in range(100)) + "\n"
        _write(tmp_path, "small.py", content)
        result = run_recon(tmp_path)
        hits = _candidates(result, "large_files")
        assert not any("small.py" in h.file for h in hits)

    def test_does_not_flag_large_file_with_test(self, tmp_path):
        content = "\n".join(f"x_{i} = {i}" for i in range(301)) + "\n"
        _write(tmp_path, "big_module.py", content)
        tests = tmp_path / "tests"
        tests.mkdir()
        _write(tests, "test_big_module.py", "def test_placeholder(): pass\n")
        result = run_recon(tmp_path)
        hits = _candidates(result, "large_files")
        assert not any("big_module.py" in h.file for h in hits)

    def test_detail_contains_line_count(self, tmp_path):
        content = "\n".join(f"x_{i} = {i}" for i in range(350)) + "\n"
        _write(tmp_path, "fat.py", content)
        result = run_recon(tmp_path)
        hits = _candidates(result, "large_files")
        fat_hits = [h for h in hits if "fat.py" in h.file]
        assert fat_hits
        assert "lines" in fat_hits[0].detail


# ---------------------------------------------------------------------------
# JSON output
# ---------------------------------------------------------------------------

class TestJSONOutput:
    def test_json_flag_produces_valid_json(self, tmp_path):
        _write(tmp_path, "config.py", 'api_key = "hardcoded"\n')
        result = run_recon(tmp_path)
        output = format_json(result)
        parsed = json.loads(output)
        assert isinstance(parsed, dict)
        assert "candidates" in parsed
        assert "file_risk_ranking" in parsed

    def test_json_structure_has_required_fields(self, tmp_path):
        _write(tmp_path, "config.py", 'api_key = "hardcoded"\n')
        result = run_recon(tmp_path)
        output = format_json(result)
        parsed = json.loads(output)
        assert len(parsed["candidates"]) >= 1
        item = parsed["candidates"][0]
        assert "category" in item
        assert "file" in item
        assert "line" in item
        assert "detail" in item

    def test_json_categories_are_lowercase(self, tmp_path):
        _write(tmp_path, "config.py", 'api_key = "hardcoded"\n')
        result = run_recon(tmp_path)
        output = format_json(result)
        parsed = json.loads(output)
        for item in parsed["candidates"]:
            assert item["category"] == item["category"].lower()

    def test_json_line_none_for_file_level_candidates(self, tmp_path):
        src = tmp_path / "src"
        src.mkdir()
        _write(src, "module.py", "def foo(): pass\n")
        result = run_recon(tmp_path)
        output = format_json(result)
        parsed = json.loads(output)
        gap_items = [i for i in parsed["candidates"] if i["category"] == "test_gaps"]
        assert gap_items
        assert gap_items[0]["line"] is None

    def test_json_risk_ranking_present(self, tmp_path):
        _write(tmp_path, "config.py", 'api_key = "hardcoded"\n')
        result = run_recon(tmp_path)
        output = format_json(result)
        parsed = json.loads(output)
        ranking = parsed["file_risk_ranking"]
        assert len(ranking) >= 1
        assert "file" in ranking[0]
        assert "score" in ranking[0]
        assert "match_count" in ranking[0]
        assert "categories" in ranking[0]


# ---------------------------------------------------------------------------
# Empty directory
# ---------------------------------------------------------------------------

class TestEmptyDirectory:
    def test_empty_dir_produces_zero_candidates(self, tmp_path):
        result = run_recon(tmp_path)
        assert len(result.candidates) == 0

    def test_empty_dir_files_scanned_zero(self, tmp_path):
        result = run_recon(tmp_path)
        assert result.files_scanned == 0

    def test_markdown_output_shows_zero_candidates(self, tmp_path):
        result = run_recon(tmp_path)
        md = format_markdown(result)
        assert "Candidates found: 0" in md

    def test_json_output_empty(self, tmp_path):
        result = run_recon(tmp_path)
        output = format_json(result)
        parsed = json.loads(output)
        assert parsed["candidates"] == []
        assert parsed["file_risk_ranking"] == []


# ---------------------------------------------------------------------------
# Exclusions
# ---------------------------------------------------------------------------

class TestExclusions:
    def test_skips_pycache(self, tmp_path):
        pycache = tmp_path / "__pycache__"
        pycache.mkdir()
        _write(pycache, "module.cpython-311.pyc", "")
        # Also write a real py file to ensure scanning happened
        _write(tmp_path, "clean.py", "x = 1\n")
        result = run_recon(tmp_path)
        # No candidates from __pycache__
        assert not any("__pycache__" in c.file for c in result.candidates)

    def test_skips_venv(self, tmp_path):
        venv = tmp_path / ".venv"
        venv.mkdir()
        lib = venv / "lib"
        lib.mkdir()
        _write(lib, "site.py", 'api_key = "exposed"\n')
        result = run_recon(tmp_path)
        hits = _candidates(result, "secrets")
        assert not any(".venv" in h.file for h in hits)


# ---------------------------------------------------------------------------
# Markdown output
# ---------------------------------------------------------------------------

class TestMarkdownOutput:
    def test_markdown_has_header(self, tmp_path):
        result = run_recon(tmp_path)
        md = format_markdown(result)
        assert "# Harden Recon — Candidates" in md

    def test_markdown_has_scanned_line(self, tmp_path):
        result = run_recon(tmp_path)
        md = format_markdown(result)
        assert "Scanned:" in md

    def test_markdown_shows_all_category_sections(self, tmp_path):
        result = run_recon(tmp_path)
        md = format_markdown(result)
        assert "## Secrets" in md
        assert "## Bare Excepts" in md
        assert "## Missing Input Validation" in md
        assert "## Hardcoded Values" in md
        assert "## Test Gaps" in md
        assert "## Large Files" in md

    def test_markdown_formats_file_line_reference(self, tmp_path):
        _write(tmp_path, "config.py", 'api_key = "hardcoded"\n')
        result = run_recon(tmp_path)
        md = format_markdown(result)
        assert "config.py:1" in md


# ---------------------------------------------------------------------------
# CLI integration
# ---------------------------------------------------------------------------

class TestCLI:
    def test_nonexistent_dir_returns_1(self, tmp_path):
        rc = main([str(tmp_path / "does_not_exist")])
        assert rc == 1

    def test_valid_dir_returns_0(self, tmp_path):
        rc = main([str(tmp_path)])
        assert rc == 0

    def test_json_flag_produces_json(self, tmp_path, capsys):
        _write(tmp_path, "cfg.py", 'password = "abc"\n')
        rc = main([str(tmp_path), "--json"])
        assert rc == 0
        out = capsys.readouterr().out
        parsed = json.loads(out)
        assert isinstance(parsed, dict)
        assert "candidates" in parsed

    def test_output_file_written(self, tmp_path):
        out_file = tmp_path / "candidates.md"
        rc = main([str(tmp_path), "--output", str(out_file)])
        assert rc == 0
        assert out_file.exists()
