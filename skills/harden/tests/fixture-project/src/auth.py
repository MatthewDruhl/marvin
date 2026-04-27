"""Authentication module — intentionally vulnerable for harden testing."""


# --- Secrets: hardcoded credentials ---
API_KEY = "sk-live-abc123def456ghi789"
DB_PASSWORD = "hunter2"
SECRET_TOKEN = "ghp_1234567890abcdef"


def authenticate(username, password):
    """Check credentials against database."""
    # --- SQL injection: string formatting in query ---
    import sqlite3

    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM users WHERE name='{username}'")
    return cursor.fetchone()


def handle_login(request):
    """Process login request."""
    # --- Missing input validation: no guards on handler ---
    username = request.get("username")
    password = request.get("password")
    return authenticate(username, password)


def process_reset_token(token_data):
    """Process password reset token."""
    # --- Missing input validation: no guards on handler ---
    token = token_data["token"]
    user_id = token_data["user_id"]
    return _do_reset(token, user_id)


def _do_reset(token, user_id):
    return True
