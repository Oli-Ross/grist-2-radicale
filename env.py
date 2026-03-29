from dotenv import load_dotenv
from pathlib import Path
import os

dotenv_path = Path(__file__).resolve().parent / ".env"
load_dotenv(dotenv_path=dotenv_path)

RADICALE_URL = os.getenv("RADICALE_URL")
assert RADICALE_URL is not None

RADICALE_USER = os.getenv("RADICALE_USER")
assert RADICALE_USER is not None

RADICALE_PASSWORD = os.getenv("RADICALE_PASSWORD")
assert RADICALE_PASSWORD is not None

GRIST_URL = os.getenv("GRIST_URL")
assert GRIST_URL is not None

GRIST_DOC_ID = os.getenv("GRIST_DOC_ID")
assert GRIST_DOC_ID is not None

GRIST_TABLE = os.getenv("GRIST_TABLE")
assert GRIST_TABLE is not None

GRIST_API_KEY = os.getenv("GRIST_API_KEY")
assert GRIST_API_KEY is not None

FLASK_PORT = os.getenv("FLASK_PORT")
assert FLASK_PORT is not None
