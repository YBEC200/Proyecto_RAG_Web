from dotenv import load_dotenv
from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent.parent.parent

load_dotenv(BASE_DIR / ".env")

class Settings:
    APP_NAME = os.getenv("APP_NAME", "chatlog-api")
    APP_ENV = os.getenv("APP_ENV", "local")
    DEBUG = os.getenv("DEBUG", "false").lower() == "true"

    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4.1-mini")

    LARAVEL_API_BASE = os.getenv("LARAVEL_API_BASE")
settings = Settings()
