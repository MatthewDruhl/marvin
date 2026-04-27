"""Config module — intentionally vulnerable for harden testing."""

# --- Hardcoded values that should be env vars ---
DATABASE_URL = "postgresql://admin:password123@10.0.0.5:5432/prod"
REDIS_HOST = "172.16.0.10"
port = 6379
API_ENDPOINT = "https://api.production.internal/v2"

# --- Environment-specific config committed as universal ---
DEBUG = True
LOG_LEVEL = "DEBUG"
ALLOWED_HOSTS = ["localhost", "127.0.0.1"]
