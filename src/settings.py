from pydantic import SecretStr
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Configuration de l'application."""

    # Base de données
    DATABASE_URL: str = "sqlite+aiosqlite:///./realworld.db"

    # JWT
    SECRET_KEY: SecretStr = SecretStr("your-secret-key")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # API
    API_V1_STR: str = "/api"
    PROJECT_NAME: str = "RealWorld API"
    VERSION: str = "1.0.0"

    # Additional environment variables that might be in .env
    PYTHONPATH: str = "./src"
    COVERAGE_RCFILE: str = "./coverage.ini"
    AZURE_FUNCTION_KEY: str = ""

    class Config:
        case_sensitive = True
        env_file = ".env"
        extra = "allow"  # Allow extra fields from environment


settings = Settings()
