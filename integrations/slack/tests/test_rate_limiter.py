"""Tests for per-user rate limiting.

Mirrors the rate-limiter logic from bot.py to avoid importing it directly
(bot.py has runtime dependencies on slack_bolt, dotenv).
"""

import threading
import time

# ---------------------------------------------------------------------------
# Mirror of rate-limiter logic from bot.py
# ---------------------------------------------------------------------------

RATE_LIMIT_MAX = 30
RATE_LIMIT_WINDOW = 3600  # 1 hour in seconds

_rate_limits: dict[str, list[float]] = {}
_rate_lock = threading.Lock()


def _check_rate_limit(user_id: str) -> bool:
    """Return True if within limits, False if exceeded."""
    now = time.time()
    cutoff = now - RATE_LIMIT_WINDOW
    with _rate_lock:
        timestamps = _rate_limits.get(user_id, [])
        timestamps = [t for t in timestamps if t > cutoff]
        if len(timestamps) >= RATE_LIMIT_MAX:
            _rate_limits[user_id] = timestamps
            return False
        timestamps.append(now)
        _rate_limits[user_id] = timestamps
        return True


def _cleanup_rate_limits() -> None:
    """Remove entries for users with no recent activity."""
    now = time.time()
    cutoff = now - RATE_LIMIT_WINDOW
    with _rate_lock:
        stale = [uid for uid, ts in _rate_limits.items() if all(t <= cutoff for t in ts)]
        for uid in stale:
            del _rate_limits[uid]


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------


class TestCheckRateLimit:
    """Tests for _check_rate_limit sliding-window logic."""

    def setup_method(self):
        _rate_limits.clear()

    def test_first_call_allowed(self):
        assert _check_rate_limit("U001") is True

    def test_under_limit_allowed(self):
        for _ in range(29):
            assert _check_rate_limit("U001") is True
        # 29 calls, still under 30
        assert _check_rate_limit("U001") is True

    def test_at_limit_denied(self):
        for _ in range(30):
            _check_rate_limit("U001")
        # 31st call should be denied
        assert _check_rate_limit("U001") is False

    def test_different_users_independent(self):
        for _ in range(30):
            _check_rate_limit("U001")
        # U001 is at limit
        assert _check_rate_limit("U001") is False
        # U002 should still be allowed
        assert _check_rate_limit("U002") is True

    def test_old_entries_expire(self):
        """Entries older than the window should be pruned, freeing capacity."""
        # Manually inject 30 timestamps that are already expired
        old_time = time.time() - RATE_LIMIT_WINDOW - 1
        with _rate_lock:
            _rate_limits["U001"] = [old_time] * 30
        # All 30 are stale, so the next call should succeed
        assert _check_rate_limit("U001") is True

    def test_mixed_old_and_new_entries(self):
        """Only recent entries count toward the limit."""
        now = time.time()
        old_time = now - RATE_LIMIT_WINDOW - 1
        with _rate_lock:
            # 20 old (expired) + 10 recent = only 10 count
            _rate_limits["U001"] = [old_time] * 20 + [now] * 10
        # Should still have 20 remaining in the window
        assert _check_rate_limit("U001") is True

    def test_denied_message_does_not_add_entry(self):
        """When rate-limited, the denied call should not add a new timestamp."""
        for _ in range(30):
            _check_rate_limit("U001")
        count_before = len(_rate_limits["U001"])
        _check_rate_limit("U001")  # denied
        count_after = len(_rate_limits["U001"])
        assert count_after == count_before


class TestCleanupRateLimits:
    """Tests for _cleanup_rate_limits."""

    def setup_method(self):
        _rate_limits.clear()

    def test_stale_user_removed(self):
        old_time = time.time() - RATE_LIMIT_WINDOW - 1
        with _rate_lock:
            _rate_limits["U001"] = [old_time]
        _cleanup_rate_limits()
        assert "U001" not in _rate_limits

    def test_recent_user_kept(self):
        _check_rate_limit("U001")
        _cleanup_rate_limits()
        assert "U001" in _rate_limits

    def test_empty_dict_no_error(self):
        _cleanup_rate_limits()
        assert len(_rate_limits) == 0

    def test_mixed_users(self):
        old_time = time.time() - RATE_LIMIT_WINDOW - 1
        with _rate_lock:
            _rate_limits["stale"] = [old_time]
        _check_rate_limit("fresh")
        _cleanup_rate_limits()
        assert "stale" not in _rate_limits
        assert "fresh" in _rate_limits


class TestRateLimiterThreadSafety:
    """Verify the rate limiter doesn't crash under concurrent access."""

    def setup_method(self):
        _rate_limits.clear()

    def test_concurrent_calls_no_crash(self):
        errors: list[Exception] = []

        def call_limiter():
            try:
                for _ in range(50):
                    _check_rate_limit("U001")
            except Exception as e:
                errors.append(e)

        threads = [threading.Thread(target=call_limiter) for _ in range(5)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        assert len(errors) == 0
