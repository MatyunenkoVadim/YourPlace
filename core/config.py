from pathlib import Path

from pydantic import BaseModel
from pydantic_settings import BaseSettings

BASE_DIR = Path(__file__).parent.parent

class AuthJWT(BaseModel):
    secret_key_path: Path = BASE_DIR / "core" / "secure" / "key" / "jwt-secret.pem"
    public_key_path: Path = BASE_DIR / "core" / "secure" / "key" / "jwt-public.pem"
    algorithm: str = "RS256"
    access_token_expire_minutes: int = 5

class DBSettings(BaseModel):
    db_url: str = "sqlite+aiosqlite:///YourPlace.db"
    # "postgresql+asyncpg://postgres:farveh8@localhost:5432/YourPlace"
    db_echo: bool = False

class Settings(BaseSettings):
    api_v1_prefix: str = "/api/v1"
    db_setting: DBSettings = DBSettings()
    auth_jwt: AuthJWT = AuthJWT()

settings = Settings()