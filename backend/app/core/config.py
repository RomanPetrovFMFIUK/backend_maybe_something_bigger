from functools import lru_cache
from pathlib import Path

from pydantic import BaseModel
from pydantic_settings import BaseSettings

BASE_DIR = Path(__file__).resolve().parent.parent.parent

class AuthJWT(BaseModel):
    private_key_path: Path = BASE_DIR / 'jwt-private.pem'
    public_key_path: Path = BASE_DIR / 'jwt-public.pem'
    algorithm: str = 'RS256'

class Settings(BaseSettings):
    DB_URL: str = "postgresql+asyncpg://myuser:mypassword@localhost:5433/mydb"
    DB_ECHO: bool = True
    CORS_ORIGINS: list[str] = ["*"]

    model_config = {
        "env_file": ".env",
        "env_file_encoding": "utf-8",
    }

    telegram_bot_token: str

    auth_jwt: AuthJWT = AuthJWT()

    owner_id: int = 1101779478


@lru_cache
def get_settings() -> Settings:
    return Settings()