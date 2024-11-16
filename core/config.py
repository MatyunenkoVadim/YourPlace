from pathlib import Path

from pydantic import BaseModel
from pydantic_settings import BaseSettings

BASE_DIR = Path(__file__).parent.parent

class AuthJWT(BaseModel):
    secret_key_path: Path = BASE_DIR / "secure" / "key" / "jwt-secret.pem"
    public_key_path: Path = BASE_DIR / "secure" / "key" / "jwt-public.pem"
    algorithm: str = "RS256"
    access_token_expire_minutes: int = 5

class Settings(BaseSettings):
    db_url: str = "postgresql+asyncpg://postgres:farveh8@localhost:5432/YourPlace"

    auth_jwt: AuthJWT = AuthJWT()

settings = Settings()