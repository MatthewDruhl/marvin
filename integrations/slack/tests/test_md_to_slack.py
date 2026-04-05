"""Tests for md_to_slack conversion in the Slack bot.

We import md_to_slack by loading only the function source, since bot.py
has runtime dependencies (slack_bolt, dotenv) that may not be available
in the test environment.
"""

import importlib.util
import sys
import types
from pathlib import Path

# Load only the md_to_slack function from bot.py without executing module-level code
_bot_path = Path(__file__).parent.parent / "bot.py"
_source = _bot_path.read_text()

# Extract the function and its imports
_module = types.ModuleType("_bot_extract")
_module.__dict__["re"] = __import__("re")
exec(compile(
    "import re\n" + _source[_source.index("def md_to_slack"):_source.index("\napp = ")],
    str(_bot_path),
    "exec",
), _module.__dict__)
md_to_slack = _module.md_to_slack


class TestMdToSlack:
    """Tests for GitHub-flavored Markdown to Slack mrkdwn conversion."""

    def test_header_conversion(self):
        """## Header should become *Header*."""
        assert md_to_slack("## My Header") == "*My Header*"

    def test_h1_conversion(self):
        """# H1 should also convert."""
        assert md_to_slack("# Title") == "*Title*"

    def test_bold_conversion(self):
        """**bold** should become *bold*."""
        assert md_to_slack("This is **bold** text") == "This is *bold* text"

    def test_strikethrough_conversion(self):
        """~~strike~~ should become ~strike~."""
        assert md_to_slack("This is ~~deleted~~ text") == "This is ~deleted~ text"

    def test_link_conversion(self):
        """[text](url) should become <url|text>."""
        result = md_to_slack("[Click here](https://example.com)")
        assert result == "<https://example.com|Click here>"

    def test_horizontal_rule(self):
        """--- should become a unicode line."""
        result = md_to_slack("---")
        assert "\u2500" in result  # box drawing character

    def test_code_block_passthrough(self):
        """Content inside code blocks should not be converted."""
        md = "```\n## Not a header\n**Not bold**\n```"
        result = md_to_slack(md)
        assert "## Not a header" in result
        assert "**Not bold**" in result

    def test_table_separator_removed(self):
        """|---|---| separator rows should be removed."""
        md = "| Name | Value |\n|------|-------|\n| foo  | bar   |"
        result = md_to_slack(md)
        assert "---" not in result

    def test_table_rows_converted(self):
        """Table rows should become space-separated values."""
        md = "| Name | Value |"
        result = md_to_slack(md)
        assert "Name" in result
        assert "Value" in result
        assert "|" not in result

    def test_plain_text_unchanged(self):
        """Plain text without markdown should pass through unchanged."""
        text = "This is plain text with no formatting."
        assert md_to_slack(text) == text

    def test_multiple_conversions_in_one_line(self):
        """Multiple markdown elements in one line should all convert."""
        result = md_to_slack("**Bold** and ~~struck~~ and [link](https://x.com)")
        assert "*Bold*" in result
        assert "~struck~" in result
        assert "<https://x.com|link>" in result

    def test_multiline_preserves_newlines(self):
        """Newlines between paragraphs should be preserved."""
        md = "Line 1\n\nLine 2\n\nLine 3"
        result = md_to_slack(md)
        assert "Line 1" in result
        assert "Line 3" in result
        assert result.count("\n") >= 2

    def test_empty_string(self):
        """Empty string should return empty string."""
        assert md_to_slack("") == ""
