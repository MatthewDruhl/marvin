"""AI agent module — intentionally vulnerable for harden testing."""


# --- Prompt injection: user input flows into prompt unsanitized ---
def generate_response(user_message):
    prompt = f"You are a helpful assistant. User says: {user_message}"
    return _call_llm(prompt)


def draft_email(user_input, context):
    """Draft email from user input."""
    # --- Prompt injection: format string with user input ---
    message = "Write an email about: {}".format(user_input)
    return _call_llm(message)


def process_document(doc_bytes):
    """Process uploaded document."""
    # --- Unsafe deserialization: pickle.loads ---
    import pickle

    data = pickle.loads(doc_bytes)
    return data


def load_config(config_bytes):
    """Load YAML config."""
    # --- Unsafe deserialization: yaml.load without SafeLoader ---
    import yaml

    return yaml.load(config_bytes)


def classify_text(text):
    """Classify text using ML model."""
    # --- Late import: possible circular dependency workaround ---
    from src.utils import get_classifier

    return get_classifier().predict(text)


def _call_llm(prompt):
    return {"response": "mock"}
