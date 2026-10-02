import os
from dotenv import load_dotenv
load_dotenv()

class Settings:
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "").strip()
    SECRET_KEY = os.getenv("SECRET_KEY", "some_super_secret_key_12345")
    DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./pocketsmart.db")
    ALGORITHM = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24

settings = Settings()