from pathlib import Path

from pydantic import BaseModel
from pydantic_settings import BaseSettings

BASE_DIR = Path(__file__).parent.parent

class AuthJWT(BaseModel):
    secret_key_path: Path = BASE_DIR / "core" / "secure" / "key" / "jwt-secret.pem"
    public_key_path: Path = BASE_DIR / "core" / "secure" / "key" / "jwt-public.pem"
    algorithm: str = "RS256"
    access_token_expire_minutes: int = 5
    reset_password_token_secret: str = '3543b40a41ba6524542afae200638366053d71f48e17e79d01d6bd257916bb29'
    verification_token_secret: str = '529164a9965294119bb866978749cf0f157ddf2edba8a6245a6081f95eafd7d1'

class DBSettings(BaseModel):
    db_url: str = "sqlite+aiosqlite:///YourPlace.db"
    # "postgresql+asyncpg://postgres:farveh8@localhost:5432/YourPlace"
    db_echo: bool = True

class Settings(BaseSettings):
    api_v1_prefix: str = "/api/v1"
    auth: str = "/auth"
    users: str = "/users"
    db_setting: DBSettings = DBSettings()
    auth_jwt: AuthJWT = AuthJWT()

settings = Settings()