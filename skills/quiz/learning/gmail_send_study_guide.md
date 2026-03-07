# Gmail Send — Study Guide

This guide covers the skills you need for the gmail_send project. Read through each section, try the mini examples, then start the lessons when you feel comfortable.

---

## 1. Environment Variables with python-dotenv

### What it is
Instead of hardcoding secrets (API keys, client IDs) in your code, you store them in a `.env` file and load them at runtime. The `python-dotenv` package reads that file and injects the values into `os.environ` so your code can access them like any other environment variable. This keeps secrets out of version control.

### Syntax
```python
import os
from dotenv import load_dotenv

# Reads .env file and populates os.environ
load_dotenv()

# Now retrieve values — returns None if the key doesn't exist
api_key = os.getenv("API_KEY")

# Or raise an error if missing (useful for required values)
api_key = os.environ["API_KEY"]
```

### Mini example
```python
# .env file contains:
# DATABASE_URL=postgresql://localhost/mydb

import os
from dotenv import load_dotenv

load_dotenv()
db_url = os.getenv("DATABASE_URL")
print(db_url)  # postgresql://localhost/mydb
```

### Common mistake
```python
# WRONG — accessing env var BEFORE calling load_dotenv()
import os
from dotenv import load_dotenv

secret = os.getenv("MY_SECRET")  # None! .env hasn't been loaded yet
load_dotenv()

# RIGHT — load first, then access
load_dotenv()
secret = os.getenv("MY_SECRET")  # actual value from .env
```

---

## 2. OAuth 2.0 Flow (Installed App)

### What it is
OAuth 2.0 lets your app act on behalf of a user without knowing their password. For a desktop/CLI app, Google uses the "Installed App" flow: your code opens a browser, the user logs in and grants permission, Google sends back an authorization code, and your app exchanges that code for access + refresh tokens. The access token expires (usually 1 hour); the refresh token lets you get a new one without re-prompting the user.

### Syntax
```python
from google_auth_oauthlib.flow import InstalledAppFlow

# client_config is a dict describing your OAuth client (client_id, client_secret, etc.)
# scopes is a list of permission strings
flow = InstalledAppFlow.from_client_config(client_config, scopes=scopes)

# Opens browser for user consent, returns Credentials object
credentials = flow.run_local_server(port=0)

# credentials.token       — the access token (string)
# credentials.refresh_token — the refresh token (string)
# credentials.expired     — bool, True if access token is expired
# credentials.valid       — bool, True if access token is usable right now
```

### Mini example
```python
from google_auth_oauthlib.flow import InstalledAppFlow

SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]

client_config = {
    "installed": {
        "client_id": "YOUR_CLIENT_ID",
        "client_secret": "YOUR_CLIENT_SECRET",
        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
        "token_uri": "https://oauth2.googleapis.com/token",
        "redirect_uris": ["http://localhost"],
    }
}

flow = InstalledAppFlow.from_client_config(client_config, scopes=SCOPES)
creds = flow.run_local_server(port=0)  # port=0 picks a random open port
print(f"Got token: {creds.token[:20]}...")
```

### Common mistake
```python
# WRONG — passing scopes as a single string
flow = InstalledAppFlow.from_client_config(config, scopes="https://...gmail.readonly")
# This silently treats each CHARACTER as a scope!

# RIGHT — scopes must be a list
flow = InstalledAppFlow.from_client_config(config, scopes=["https://...gmail.readonly"])
```

---

## 3. Token Persistence and Refresh

### What it is
You don't want to open the browser every time your script runs. After the first OAuth flow, you save the credentials (including the refresh token) to a file like `token.json`. On the next run, you load that file, check if the token is expired, and refresh it automatically — no browser needed.

### Syntax
```python
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
import json

# Save credentials to a file
def save_token(creds, path="token.json"):
    with open(path, "w") as f:
        f.write(creds.to_json())

# Load credentials from a file
def load_token(path="token.json"):
    return Credentials.from_authorized_user_file(path)

# Refresh expired credentials
if creds and creds.expired and creds.refresh_token:
    creds.refresh(Request())  # uses refresh_token to get a new access_token
```

### Mini example
```python
from pathlib import Path
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request

TOKEN_PATH = Path("token.json")

creds = None
if TOKEN_PATH.exists():
    creds = Credentials.from_authorized_user_file(str(TOKEN_PATH))

if creds and creds.expired and creds.refresh_token:
    creds.refresh(Request())
    # Save the refreshed token
    TOKEN_PATH.write_text(creds.to_json())

if not creds or not creds.valid:
    # Need to run the full OAuth flow
    print("No valid token — run OAuth flow")
```

### Common mistake
```python
# WRONG — checking only creds.expired without checking refresh_token
if creds.expired:
    creds.refresh(Request())
# Crashes if refresh_token is None (e.g., token file was corrupted)

# RIGHT — guard both conditions
if creds and creds.expired and creds.refresh_token:
    creds.refresh(Request())
```

---

## 4. Google API Python Client — `build()`

### What it is
The `googleapiclient.discovery.build()` function creates a service object that knows every method the Gmail API offers. You pass it the API name (`"gmail"`), version (`"v1"`), and your credentials. The returned object has methods like `.users().messages().list()` that map directly to REST API endpoints.

### Syntax
```python
from googleapiclient.discovery import build

# Create the service object
service = build("gmail", "v1", credentials=creds)

# All Gmail API calls go through service.users()
# .execute() actually sends the HTTP request
result = service.users().messages().list(userId="me").execute()
```

### Mini example
```python
from googleapiclient.discovery import build

# Assuming `creds` is a valid Credentials object
service = build("gmail", "v1", credentials=creds)

# Get your own profile (email address, total messages, etc.)
profile = service.users().getProfile(userId="me").execute()
print(profile["emailAddress"])  # your-email@gmail.com
```

### Common mistake
```python
# WRONG — forgetting .execute() (returns a request object, not data)
messages = service.users().messages().list(userId="me")
print(messages)  # <googleapiclient.http.HttpRequest object>

# RIGHT — call .execute() to actually make the API call
messages = service.users().messages().list(userId="me").execute()
print(messages)  # {'messages': [...], 'resultSizeEstimate': 5}
```

---

## 5. Gmail API Resource Model

### What it is
Gmail organizes data into four main resources:
- **Messages**: individual emails. Each has an `id`, `threadId`, `labelIds`, `payload` (headers + body), and `snippet`.
- **Threads**: a conversation — a group of messages sharing the same `threadId`.
- **Drafts**: unsent messages saved for later. Each draft wraps a message.
- **Labels**: tags like `INBOX`, `SENT`, `UNREAD`, or custom ones. Messages can have multiple labels.

All API calls use `userId="me"` to refer to the authenticated user.

### Syntax
```python
# Messages
service.users().messages().list(userId="me", maxResults=5).execute()
service.users().messages().get(userId="me", id=msg_id, format="full").execute()
service.users().messages().send(userId="me", body={"raw": encoded}).execute()

# Threads
service.users().threads().list(userId="me").execute()
service.users().threads().get(userId="me", id=thread_id).execute()

# Drafts
service.users().drafts().create(userId="me", body={"message": {"raw": encoded}}).execute()
service.users().drafts().get(userId="me", id=draft_id).execute()
service.users().drafts().send(userId="me", body={"id": draft_id}).execute()
service.users().drafts().delete(userId="me", id=draft_id).execute()

# Labels
service.users().labels().list(userId="me").execute()
```

### Mini example
```python
# List 3 recent messages, then get the first one's details
results = service.users().messages().list(userId="me", maxResults=3).execute()
messages = results.get("messages", [])

if messages:
    msg = service.users().messages().get(
        userId="me", id=messages[0]["id"], format="full"
    ).execute()
    # Extract subject from headers
    headers = msg["payload"]["headers"]
    subject = next(h["value"] for h in headers if h["name"] == "Subject")
    print(f"Subject: {subject}")
```

### Common mistake
```python
# WRONG — assuming messages().list() returns full message data
results = service.users().messages().list(userId="me").execute()
print(results["messages"][0]["snippet"])  # KeyError! list() only returns id + threadId

# RIGHT — list() gives IDs, then use get() for full details
msg_id = results["messages"][0]["id"]
full_msg = service.users().messages().get(userId="me", id=msg_id).execute()
print(full_msg["snippet"])  # works
```

---

## 6. MIME Message Construction

### What it is
Email messages follow the MIME (Multipurpose Internet Mail Extensions) standard. Python's `email.mime.text.MIMEText` class lets you build a properly formatted email with headers (To, From, Subject) and a body. The Gmail API expects the entire MIME message as a base64url-encoded string.

### Syntax
```python
from email.mime.text import MIMEText

# Create the message
message = MIMEText("This is the email body")  # plain text by default
message["to"] = "recipient@example.com"
message["from"] = "sender@example.com"
message["subject"] = "Hello from Python"

# The raw bytes of the full MIME message
raw_bytes = message.as_bytes()
# Produces something like:
# Content-Type: text/plain; charset="us-ascii"\n
# to: recipient@example.com\n
# from: sender@example.com\n
# subject: Hello from Python\n\n
# This is the email body
```

### Mini example
```python
from email.mime.text import MIMEText

msg = MIMEText("Meeting at 3pm tomorrow.")
msg["to"] = "colleague@example.com"
msg["from"] = "me@example.com"
msg["subject"] = "Quick reminder"

print(msg.as_string())
# Shows the full MIME-formatted email as text
```

### Common mistake
```python
# WRONG — setting headers with the wrong syntax
msg = MIMEText("body")
msg.to = "someone@example.com"       # creates a Python attribute, NOT an email header
msg.subject = "Hello"                 # same problem — no header set

# RIGHT — use dict-style bracket notation for email headers
msg = MIMEText("body")
msg["to"] = "someone@example.com"     # sets the To: header
msg["subject"] = "Hello"              # sets the Subject: header
```

---

## 7. Base64url Encoding and Decoding

### What it is
The Gmail API uses base64url encoding (a URL-safe variant of base64) for message bodies. When **sending**, you encode your MIME message bytes into a base64url string. When **reading**, the message body comes back base64url-encoded and you decode it to get the original text. Python's `base64` module handles both directions.

### Syntax
```python
import base64

# ENCODE (for sending) — bytes in, string out
encoded = base64.urlsafe_b64encode(raw_bytes).decode("ascii")

# DECODE (for reading) — string in, bytes out, then decode to text
decoded_bytes = base64.urlsafe_b64decode(encoded_string)
text = decoded_bytes.decode("utf-8")
```

### Mini example
```python
import base64

# Encoding
original = b"Hello, Gmail!"
encoded = base64.urlsafe_b64encode(original).decode("ascii")
print(encoded)  # SGVsbG8sIEdtYWlsIQ==

# Decoding
decoded = base64.urlsafe_b64decode(encoded).decode("utf-8")
print(decoded)  # Hello, Gmail!
```

### Common mistake
```python
# WRONG — using standard b64decode on Gmail API data (fails on URL-safe chars)
import base64
body_data = msg["payload"]["body"]["data"]
text = base64.b64decode(body_data).decode("utf-8")  # may crash on - or _ characters

# RIGHT — use urlsafe variant, and pad if needed
text = base64.urlsafe_b64decode(body_data + "==").decode("utf-8")
# Adding "==" handles missing padding (Gmail often strips trailing =)
```

---

## 8. RFC 2822 Threading Headers

### What it is
When you reply to an email, email clients need to know which message you're replying to so they can display the conversation correctly. Two standard headers handle this:
- **`In-Reply-To`**: the `Message-ID` of the message you're directly replying to.
- **`References`**: a space-separated list of all `Message-ID`s in the conversation chain.

Gmail also uses its own `threadId` field to group messages, but setting the RFC headers ensures compatibility with non-Gmail clients.

### Syntax
```python
from email.mime.text import MIMEText

reply = MIMEText("Thanks, got it!")
reply["to"] = "original-sender@example.com"
reply["from"] = "me@example.com"
reply["subject"] = "Re: Original Subject"             # Re: prefix convention
reply["In-Reply-To"] = "<original-message-id@mail>"   # Message-ID of parent
reply["References"] = "<original-message-id@mail>"     # full chain of Message-IDs
```

### Mini example
```python
# Suppose the original email has:
#   Message-ID: <abc123@mail.gmail.com>
#   Subject: Project update

from email.mime.text import MIMEText

reply = MIMEText("Looks good, thanks!")
reply["to"] = "alice@example.com"
reply["from"] = "bob@example.com"
reply["subject"] = "Re: Project update"
reply["In-Reply-To"] = "<abc123@mail.gmail.com>"
reply["References"] = "<abc123@mail.gmail.com>"

# When sending via Gmail API, also include threadId in the request body:
# body={"raw": encoded_reply, "threadId": original_thread_id}
```

### Common mistake
```python
# WRONG — using the message `id` from Gmail API as the In-Reply-To value
reply["In-Reply-To"] = "18e3a4b5c6d7e8f9"  # this is a Gmail internal ID, not a Message-ID

# RIGHT — extract the Message-ID header from the original message
headers = original_msg["payload"]["headers"]
message_id = next(h["value"] for h in headers if h["name"] == "Message-Id")
reply["In-Reply-To"] = message_id  # looks like <CABx...@mail.gmail.com>
```

---

## 9. TypedDict for Structured Return Types

### What it is
`TypedDict` lets you define the exact shape of a dictionary — what keys it has and what types the values are. Unlike a regular `dict`, a `TypedDict` gives you autocompletion and type-checking in your editor. It's great for wrapping API responses so callers know exactly what fields to expect without reading docs.

### Syntax
```python
from typing import TypedDict

class EmailResult(TypedDict):
    id: str
    thread_id: str
    label_ids: list[str]

# Usage — just a normal dict, but type checkers know the shape
result: EmailResult = {
    "id": "abc123",
    "thread_id": "thread456",
    "label_ids": ["SENT", "INBOX"],
}
```

### Mini example
```python
from typing import TypedDict

class UserProfile(TypedDict):
    email: str
    messages_total: int
    threads_total: int

def get_profile(service) -> UserProfile:
    raw = service.users().getProfile(userId="me").execute()
    return UserProfile(
        email=raw["emailAddress"],
        messages_total=raw["messagesTotal"],
        threads_total=raw["threadsTotal"],
    )

profile = get_profile(service)
print(profile["email"])  # type checker knows this is a str
```

### Common mistake
```python
# WRONG — using dot notation on a TypedDict (it's still a dict!)
class Config(TypedDict):
    host: str
    port: int

cfg: Config = {"host": "localhost", "port": 8080}
print(cfg.host)  # AttributeError! TypedDict uses [] not .

# RIGHT — use bracket notation
print(cfg["host"])  # "localhost"
```

---

## 10. Class Design — Wrapping an API Client

### What it is
Instead of scattered functions, you wrap related API operations in a class. The class holds shared state (like the authenticated service object) in `__init__`, and each method performs one API operation. This makes the library easy to use: create one instance, call methods on it.

### Syntax
```python
class GmailClient:
    def __init__(self, service):
        self._service = service  # store the authenticated service

    def send_email(self, to: str, subject: str, body: str) -> dict:
        # build MIME message, encode, send via self._service
        ...

    def create_draft(self, to: str, subject: str, body: str) -> dict:
        # build MIME message, encode, create draft via self._service
        ...
```

### Mini example
```python
class Calculator:
    def __init__(self, precision: int = 2):
        self._precision = precision

    def add(self, a: float, b: float) -> float:
        return round(a + b, self._precision)

    def divide(self, a: float, b: float) -> float:
        if b == 0:
            raise ValueError("Cannot divide by zero")
        return round(a / b, self._precision)

calc = Calculator(precision=3)
print(calc.add(1.1, 2.2))     # 3.3
print(calc.divide(10, 3))     # 3.333
```

### Common mistake
```python
# WRONG — forgetting self, so each method recreates the service
class GmailClient:
    def __init__(self, service):
        self._service = service

    def send_email(self, to, subject, body):
        service = build("gmail", "v1", credentials=creds)  # wasteful! already have it
        ...

# RIGHT — use self._service that was set up in __init__
class GmailClient:
    def __init__(self, service):
        self._service = service

    def send_email(self, to, subject, body):
        result = self._service.users().messages().send(...).execute()
        ...
```

---

## 11. TDD with Mocked API Calls

### What it is
You can't (and shouldn't) hit the real Gmail API in your tests — it's slow, requires credentials, and actually sends emails. Instead, you use `unittest.mock.patch` to replace the API calls with fake objects that return predictable data. You write the test first (TDD), define what the mock should return, then write the code to make it pass.

### Syntax
```python
from unittest.mock import patch, MagicMock

# patch() replaces an import path with a mock for the duration of the test
@patch("my_module.build")
def test_something(mock_build):
    # Configure what the mock returns
    mock_service = MagicMock()
    mock_build.return_value = mock_service

    # Chain mock returns for nested calls like service.users().messages().send()
    mock_service.users.return_value.messages.return_value.send.return_value.execute.return_value = {
        "id": "msg123",
        "threadId": "thread456",
    }

    # Now call your code — it uses the mock instead of the real API
    result = my_function()
    assert result["id"] == "msg123"
```

### Mini example
```python
from unittest.mock import patch, MagicMock

def fetch_username(api_client):
    """Calls an API and returns the username."""
    response = api_client.get_user(user_id=1)
    return response["username"]

def test_fetch_username():
    mock_client = MagicMock()
    mock_client.get_user.return_value = {"username": "matt", "id": 1}

    result = fetch_username(mock_client)

    assert result == "matt"
    mock_client.get_user.assert_called_once_with(user_id=1)
```

### Common mistake
```python
# WRONG — patching the wrong path (where the object is defined vs where it's used)
# If client.py does: from googleapiclient.discovery import build

@patch("googleapiclient.discovery.build")  # patches the ORIGINAL location
def test_auth(mock_build):
    ...
# This may not work because client.py already imported `build` into its own namespace

# RIGHT — patch where the name is LOOKED UP (in your module)
@patch("gmail_send.auth.build")  # patches the reference in YOUR module
def test_auth(mock_build):
    ...
```

---

## 12. Editable Installs with uv

### What it is
An editable install (also called "development mode") links your package into another project so that changes to the source code take effect immediately — no reinstall needed. This is how you'll make the `gmail_send` library available to the YPS project while still developing it.

### Syntax
```bash
# From the project that USES the library (e.g., YPS):
uv add --editable /path/to/gmail_send

# This adds an entry to pyproject.toml like:
# gmail-send = { path = "/path/to/gmail_send", editable = true }

# Now you can import it:
# from gmail_send.client import GmailClient
```

### Mini example
```bash
# You have two projects:
# ~/Code/Learning/gmail_send/   (the library)
# ~/Code/YPS/                   (the consumer)

cd ~/Code/YPS
uv add --editable ~/Code/Learning/gmail_send

# Now in YPS code:
# from gmail_send.auth import get_gmail_service
# from gmail_send.client import GmailClient
```

### Common mistake
```bash
# WRONG — using pip install -e (we use uv, not pip)
pip install -e ~/Code/Learning/gmail_send

# RIGHT — use uv
uv add --editable ~/Code/Learning/gmail_send

# ALSO WRONG — forgetting the hatchling build config
# If pyproject.toml doesn't specify [build-system] and [tool.hatch.build.targets.wheel],
# the editable install won't know which package to expose.
```
