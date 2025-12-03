from dotenv import load_dotenv
import os

def require_env(*names: str):
    """Ensure required environment variables are set."""
    missing = [name for name in names if not os.environ.get(name)]
    if missing:
        raise RuntimeError(f"Missing required environment variables: {missing}")

load_dotenv()

require_env("PERSIST_DIR", "SPEECHES_CSV", "URL_LIST", "API_KEY")

PERSIST_DIR = os.environ.get("PERSIST_DIR")
SPEECHES_CSV = os.environ.get("SPEECHES_CSV")
URL_LIST = os.environ.get("URL_LIST")
API_KEY = os.environ.get("API_KEY")
