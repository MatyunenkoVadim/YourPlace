"""
Этот модуль определяет настройки конфигурации для приложения, включая параметры
аутентификации и базы данных.

Классы:
- AuthJWT: Настройки для JWT аутентификации, включая пути к ключам и алгоритмы.
- DBSettings: Настройки для подключения к базе данных.
- Settings: Общие настройки приложения, включая префиксы API и настройки аутентификации и базы данных.

Зависимости:
- Использует Pydantic для валидации и управления настройками.
- Использует pathlib для работы с путями файловой системы.

Контекст:
Этот файл является частью системы конфигурации и используется для управления
настройками приложения, которые могут быть изменены в зависимости от окружения.
"""

from pathlib import Path
from pydantic import BaseModel
from pydantic_settings import BaseSettings

BASE_DIR = Path(__file__).parent.parent


class AuthJWT(BaseModel):
    """
    Настройки для JWT аутентификации.

    Атрибуты:
    - secret_key_path: Путь к файлу с секретным ключом JWT.
    - public_key_path: Путь к файлу с публичным ключом JWT.
    - algorithm: Алгоритм, используемый для подписи JWT.
    - access_token_expire_minutes: Время жизни токена доступа в минутах.
    - reset_password_token_secret: Секрет для токена сброса пароля.
    - verification_token_secret: Секрет для токена верификации.
    """
    secret_key_path: Path = BASE_DIR / "core" / "secure" / "key" / "jwt-secret.pem"
    public_key_path: Path = BASE_DIR / "core" / "secure" / "key" / "jwt-public.pem"
    algorithm: str = "RS256"
    access_token_expire_minutes: int = 5
    reset_password_token_secret: str = '3543b40a41ba6524542afae200638366053d71f48e17e79d01d6bd257916bb29'
    verification_token_secret: str = '529164a9965294119bb866978749cf0f157ddf2edba8a6245a6081f95eafd7d1'


class DBSettings(BaseModel):
    """
    Настройки для подключения к базе данных.

    Атрибуты:
    - db_url: URL для подключения к базе данных.
    - db_echo: Флаг для вывода SQL-запросов в консоль.
    """
    db_url: str = "sqlite+aiosqlite:///YourPlace.db"
    # "postgresql+asyncpg://postgres:farveh8@localhost:5432/YourPlace"
    db_echo: bool = False


class Settings(BaseSettings):
    """
    Общие настройки приложения.

    Атрибуты:
    - api_v1_prefix: Префикс для API версии 1.
    - auth: Префикс для маршрутов аутентификации.
    - users: Префикс для маршрутов пользователей.
    - db_setting: Настройки базы данных.
    - auth_jwt: Настройки JWT аутентификации.
    """
    api_v1_prefix: str = "/api/v1"
    auth: str = "/auth"
    users: str = "/users"
    db_setting: DBSettings = DBSettings()
    auth_jwt: AuthJWT = AuthJWT()


settings = Settings()
