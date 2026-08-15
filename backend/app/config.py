import os

try:
    from pydantic_settings import BaseSettings, SettingsConfigDict
    class Settings(BaseSettings):
        PROJECT_NAME: str = "BugSense AI"
        API_V1_STR: str = "/api"
        SECRET_KEY: str = "super-secret-key-change-this-in-production-bugsense-ai-2026"
        ALGORITHM: str = "HS256"
        ACCESS_TOKEN_EXPIRE_MINUTES: int = 1440
        DATABASE_URL: str = "sqlite:///./bugsense.db"

        model_config = SettingsConfigDict(
            env_file=".env",
            env_file_encoding="utf-8",
            extra="ignore"
        )
except ImportError:
    try:
        from pydantic import BaseSettings
        class Settings(BaseSettings):
            PROJECT_NAME: str = "BugSense AI"
            API_V1_STR: str = "/api"
            SECRET_KEY: str = "super-secret-key-change-this-in-production-bugsense-ai-2026"
            ALGORITHM: str = "HS256"
            ACCESS_TOKEN_EXPIRE_MINUTES: int = 1440
            DATABASE_URL: str = "sqlite:///./bugsense.db"

            class Config:
                env_file = ".env"
                env_file_encoding = "utf-8"
                extra = "ignore"
    except ImportError:
        class Settings:
            def __init__(self):
                self.PROJECT_NAME = os.getenv("PROJECT_NAME", "BugSense AI")
                self.API_V1_STR = os.getenv("API_V1_STR", "/api")
                self.SECRET_KEY = os.getenv("SECRET_KEY", "super-secret-key-change-this-in-production-bugsense-ai-2026")
                self.ALGORITHM = os.getenv("ALGORITHM", "HS256")
                self.ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "1440"))
                self.DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./bugsense.db")

settings = Settings()
