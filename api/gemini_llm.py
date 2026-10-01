from google import genai
from dotenv import load_dotenv
from pathlib import Path
import os


# Find the project root
BASE_DIR = Path(__file__).resolve().parents[1]

# Load .env from the api folder
ENV_PATH = BASE_DIR / "api" / ".env"

load_dotenv(ENV_PATH)


api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError(
        "GEMINI_API_KEY was not found. "
        "Check that api/.env contains GEMINI_API_KEY."
    )


client = genai.Client(
    api_key=api_key
)