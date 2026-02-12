from dotenv import load_dotenv
import os

load_dotenv()

class Settings:
    LARAVEL_API_BASE = os.getenv("LARAVEL_API_BASE")
    LARAVEL_API_TOKEN = os.getenv("LARAVEL_API_TOKEN")
    GROQ_API_KEY = os.getenv("GROQ_API_KEY")

settings = Settings()
