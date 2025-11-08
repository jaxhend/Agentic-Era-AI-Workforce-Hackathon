import os
from dotenv import load_dotenv

load_dotenv()

VLLM_BASE_URL = os.getenv("VLLM_BASE_URL", "http://31.22.104.92:8000")
VLLM_MODEL = os.getenv("VLLM_MODEL", "google/gemma-3-27b-it")
DB_URL = os.getenv("DB_URL", "./agent_context.json")
DEFAULT_LOCALE = os.getenv("DEFAULT_LOCALE", "et")

