"""API module — intentionally vulnerable for harden testing."""

import subprocess

# --- Hardcoded values: IP and port ---
SERVER_IP = "192.168.1.100"
port = 8443


def run_deploy(branch_name):
    """Deploy a branch — shell injection risk."""
    # --- Shell injection: subprocess with shell=True ---
    subprocess.run(
        f"git checkout {branch_name} && make deploy",
        shell=True,
    )


def fetch_data(url):
    """Fetch data from external service."""
    try:
        import urllib.request

        return urllib.request.urlopen(url).read()
    except Exception:
        # --- Bare except: silently swallows all errors ---
        pass


def process_webhook(payload):
    """Handle incoming webhook."""
    try:
        data = payload["data"]
        return _handle_event(data)
    except Exception:
        # --- Bare except: no logging or re-raise ---
        return None


def _handle_event(data):
    return {"status": "ok"}
