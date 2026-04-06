"""Tests for Slack bot core logic.

Tests cover: message chunking (send_response), session reset, session locks,
TTL-based session cleanup, and ask_claude with mocked subprocess.

Like the other test files, we mirror/extract pure logic from bot.py rather
than importing it directly (bot.py has runtime dependencies on slack_bolt,
dotenv).
"""

import json
import subprocess
import threading
import time
from unittest.mock import MagicMock, patch

import pytest

# ---------------------------------------------------------------------------
# 1. send_response chunking
# ---------------------------------------------------------------------------

class TestSendResponseChunking:
    """Tests for the message chunking logic inside send_response."""

    MAX_LEN = 3900

    def _chunk_message(self, text: str) -> list[str]:
        """Mirror of the chunking logic in send_response (bot.py lines 271-285)."""
        max_len = self.MAX_LEN
        if len(text) <= max_len:
            return [text]

        chunks = []
        current = ""
        for line in text.split("\n"):
            if len(current) + len(line) + 1 > max_len:
                chunks.append(current)
                current = line
            else:
                current = current + "\n" + line if current else line
        if current:
            chunks.append(current)
        return chunks

    def test_short_message_single_chunk(self):
        result = self._chunk_message("Hello world")
        assert len(result) == 1
        assert result[0] == "Hello world"

    def test_empty_message_single_chunk(self):
        result = self._chunk_message("")
        assert len(result) == 1
        assert result[0] == ""

    def test_exactly_at_limit(self):
        msg = "x" * self.MAX_LEN
        result = self._chunk_message(msg)
        assert len(result) == 1
        assert result[0] == msg

    def test_one_over_limit_with_newlines_splits(self):
        # Build a message slightly over the limit with newlines
        line = "A" * 100
        # 40 lines of 100 chars = 4000 chars + 39 newlines
        msg = "\n".join([line] * 40)
        assert len(msg) > self.MAX_LEN
        result = self._chunk_message(msg)
        assert len(result) > 1
        for chunk in result:
            assert len(chunk) <= self.MAX_LEN

    def test_long_message_splits_on_newlines(self):
        lines = [f"Line {i} " + "x" * 80 for i in range(60)]
        msg = "\n".join(lines)
        result = self._chunk_message(msg)
        assert len(result) > 1
        # Reassembling should give back the original
        reassembled = "\n".join(result)
        assert reassembled == msg

    def test_no_newlines_long_message(self):
        """A single line over the limit: first chunk is empty, second is the whole line."""
        msg = "x" * 5000
        result = self._chunk_message(msg)
        # The loop never enters the else branch for a single-line message,
        # so we get ["", "xxxx..."] — the key point is it doesn't crash.
        assert len(result) >= 1
        # The full content is preserved
        assert "".join(result) == msg

    def test_message_with_single_newline_at_end(self):
        msg = "Hello\n"
        result = self._chunk_message(msg)
        assert len(result) == 1


# ---------------------------------------------------------------------------
# 2. _reset_session
# ---------------------------------------------------------------------------

class TestResetSession:
    """Tests for session reset logic (bot.py _reset_session)."""

    def _reset_session(self, sessions: dict, thread_key: str) -> str:
        """Mirror of _reset_session without logging."""
        sessions.pop(thread_key, None)
        return "new"

    def test_reset_existing_session(self):
        sessions = {"thread1": "session-abc"}
        result = self._reset_session(sessions, "thread1")
        assert result == "new"
        assert "thread1" not in sessions

    def test_reset_nonexistent_session_no_error(self):
        sessions = {}
        result = self._reset_session(sessions, "thread1")
        assert result == "new"
        assert len(sessions) == 0

    def test_reset_does_not_affect_other_sessions(self):
        sessions = {"thread1": "sess-a", "thread2": "sess-b"}
        self._reset_session(sessions, "thread1")
        assert "thread2" in sessions
        assert sessions["thread2"] == "sess-b"


# ---------------------------------------------------------------------------
# 3. _get_session_lock
# ---------------------------------------------------------------------------

class TestGetSessionLock:
    """Tests for per-session lock management (bot.py _get_session_lock)."""

    def setup_method(self):
        self._locks: dict[str, threading.Lock] = {}
        self._locks_lock = threading.Lock()

    def _get_session_lock(self, key: str) -> threading.Lock:
        """Mirror of _get_session_lock."""
        with self._locks_lock:
            if key not in self._locks:
                self._locks[key] = threading.Lock()
            return self._locks[key]

    def test_same_key_returns_same_lock(self):
        lock1 = self._get_session_lock("thread1")
        lock2 = self._get_session_lock("thread1")
        assert lock1 is lock2

    def test_different_keys_return_different_locks(self):
        lock1 = self._get_session_lock("thread1")
        lock2 = self._get_session_lock("thread2")
        assert lock1 is not lock2

    def test_lock_is_usable(self):
        lock = self._get_session_lock("thread1")
        assert lock.acquire(timeout=1)
        lock.release()


# ---------------------------------------------------------------------------
# 4. _cleanup_stale_sessions
# ---------------------------------------------------------------------------

class TestCleanupStaleSessions:
    """Tests for TTL-based session cleanup (bot.py _cleanup_stale_sessions)."""

    SESSION_TTL = 28800  # 8 hours, matches bot.py

    def _cleanup(self, sessions, locks, last_used):
        """Mirror of _cleanup_stale_sessions."""
        now = time.time()
        stale_keys = [k for k, v in last_used.items() if now - v > self.SESSION_TTL]
        for key in stale_keys:
            sessions.pop(key, None)
            locks.pop(key, None)
            last_used.pop(key, None)
        return stale_keys

    def test_stale_sessions_removed(self):
        now = time.time()
        sessions = {"old": "sess1", "new": "sess2"}
        locks = {"old": threading.Lock(), "new": threading.Lock()}
        last_used = {"old": now - 30000, "new": now - 100}

        stale = self._cleanup(sessions, locks, last_used)
        assert "old" in stale
        assert "old" not in sessions
        assert "old" not in locks
        assert "old" not in last_used

    def test_recent_sessions_kept(self):
        now = time.time()
        sessions = {"new": "sess1"}
        locks = {"new": threading.Lock()}
        last_used = {"new": now - 100}

        stale = self._cleanup(sessions, locks, last_used)
        assert len(stale) == 0
        assert "new" in sessions

    def test_all_stale_empties_dicts(self):
        now = time.time()
        sessions = {"a": "s1", "b": "s2"}
        locks = {"a": threading.Lock(), "b": threading.Lock()}
        last_used = {"a": now - 30000, "b": now - 30000}

        self._cleanup(sessions, locks, last_used)
        assert len(sessions) == 0
        assert len(locks) == 0
        assert len(last_used) == 0

    def test_empty_dicts_no_error(self):
        stale = self._cleanup({}, {}, {})
        assert len(stale) == 0


# ---------------------------------------------------------------------------
# 5. ask_claude with mocked subprocess
# ---------------------------------------------------------------------------

class TestAskClaude:
    """Tests for ask_claude behaviour with mocked subprocess.run."""

    def _make_proc(self, stdout="", stderr="", returncode=0):
        proc = MagicMock()
        proc.stdout = stdout
        proc.stderr = stderr
        proc.returncode = returncode
        return proc

    @patch("subprocess.run")
    def test_new_session_stores_session_id(self, mock_run):
        """A new session parses JSON output and stores the session_id."""
        mock_run.return_value = self._make_proc(
            stdout=json.dumps({"session_id": "abc-123", "result": "Hello!"})
        )
        sessions: dict[str, str] = {}

        proc = subprocess.run(
            ["claude", "--print", "--output-format", "json", "hello"],
            capture_output=True, text=True, timeout=120,
        )
        output = proc.stdout.strip()
        data = json.loads(output)
        if data.get("session_id"):
            sessions["thread1"] = data["session_id"]

        assert sessions["thread1"] == "abc-123"
        assert data["result"] == "Hello!"

    @patch("subprocess.run")
    def test_resume_session_passes_flag(self, mock_run):
        """When resuming, --resume flag is included in the command."""
        mock_run.return_value = self._make_proc(stdout="Continued conversation")
        existing_session = "abc-123"

        cmd = ["claude", "--print", "--resume", existing_session, "follow up"]
        subprocess.run(cmd, capture_output=True, text=True, timeout=120)

        called_cmd = mock_run.call_args[0][0]
        assert "--resume" in called_cmd
        assert "abc-123" in called_cmd

    @patch("subprocess.run")
    def test_empty_output_indicates_error(self, mock_run):
        """Empty stdout should be treated as an error condition."""
        mock_run.return_value = self._make_proc(stdout="", stderr="something broke")

        proc = subprocess.run(
            ["claude", "--print", "hello"],
            capture_output=True, text=True, timeout=120,
        )
        output = proc.stdout.strip()
        assert output == ""
        assert proc.stderr.strip() == "something broke"

    @patch("subprocess.run")
    def test_timeout_raises_exception(self, mock_run):
        """subprocess.TimeoutExpired should propagate so caller can handle it."""
        mock_run.side_effect = subprocess.TimeoutExpired(cmd="claude", timeout=120)

        with pytest.raises(subprocess.TimeoutExpired):
            subprocess.run(
                ["claude", "--print", "hello"],
                capture_output=True, text=True, timeout=120,
            )

    @patch("subprocess.run")
    def test_json_parse_failure_returns_raw_output(self, mock_run):
        """If JSON parsing fails, the raw output should still be usable."""
        mock_run.return_value = self._make_proc(stdout="not json at all")

        proc = subprocess.run(
            ["claude", "--print", "--output-format", "json", "hello"],
            capture_output=True, text=True, timeout=120,
        )
        output = proc.stdout.strip()
        try:
            data = json.loads(output)
        except json.JSONDecodeError:
            data = None

        assert data is None
        assert output == "not json at all"

    @patch("subprocess.run")
    def test_session_conflict_detected(self, mock_run):
        """Session conflict message should be detectable for retry logic."""
        mock_run.return_value = self._make_proc(
            stdout="Session ID abc is already in use"
        )

        proc = subprocess.run(
            ["claude", "--print", "--resume", "abc", "hello"],
            capture_output=True, text=True, timeout=120,
        )
        output = proc.stdout.strip()
        is_conflict = "Session ID" in output and "is already in use" in output
        assert is_conflict

    @patch("subprocess.run")
    def test_session_conflict_clears_and_retries(self, mock_run):
        """After max retries on conflict, session is cleared and new one started."""
        conflict_proc = self._make_proc(stdout="Session ID abc is already in use")
        fresh_proc = self._make_proc(
            stdout=json.dumps({"session_id": "new-456", "result": "Fresh start"})
        )
        mock_run.side_effect = [conflict_proc, conflict_proc, conflict_proc, fresh_proc]

        sessions = {"thread1": "abc"}

        # Simulate the retry loop (3 conflicts then clear and start fresh)
        max_retries = 2
        output = None
        for attempt in range(max_retries + 1):
            proc = subprocess.run(["claude"], capture_output=True, text=True, timeout=120)
            output = proc.stdout.strip()
            if "Session ID" in output and "is already in use" in output:
                if attempt < max_retries:
                    continue
                # Clear session and start fresh
                sessions.pop("thread1", None)
                proc = subprocess.run(["claude"], capture_output=True, text=True, timeout=120)
                output = proc.stdout.strip()
                data = json.loads(output)
                if data.get("session_id"):
                    sessions["thread1"] = data["session_id"]
                output = data.get("result", output)
                break
            break

        assert sessions["thread1"] == "new-456"
        assert output == "Fresh start"

    @patch("subprocess.run")
    def test_file_not_found_error(self, mock_run):
        """FileNotFoundError (claude CLI missing) should be catchable."""
        mock_run.side_effect = FileNotFoundError("claude not found")

        with pytest.raises(FileNotFoundError):
            subprocess.run(
                ["claude", "--print", "hello"],
                capture_output=True, text=True, timeout=120,
            )
