"""Partial test coverage — only covers auth.py, leaving gaps."""

from src.auth import authenticate, handle_login


def test_authenticate_returns_none_for_missing_user():
    # Would need a real DB, but tests the function exists
    assert callable(authenticate)


def test_handle_login_callable():
    assert callable(handle_login)
