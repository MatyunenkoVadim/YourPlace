"""
Этот модуль определяет стратегию JWT для аутентификации пользователей.

Функции:
- get_jwt_strategy: Возвращает стратегию JWT для использования в FastAPI Users.

Зависимости:
- Использует FastAPI Users для работы с JWT стратегией.
- Использует настройки из core.config для конфигурации JWT.

Контекст:
Этот файл является частью системы аутентификации и используется для настройки
JWT стратегии, которая управляет созданием и проверкой JWT токенов.
"""

from fastapi_users.authentication import JWTStrategy
from core.config import settings


def get_jwt_strategy() -> JWTStrategy:
    """
    Возвращает стратегию JWT для использования в FastAPI Users.

    Возвращает:
    - Экземпляр JWTStrategy, настроенный с использованием секретного ключа,
      времени жизни токена и алгоритма из настроек.
    """
    return JWTStrategy(
        secret=settings.auth_jwt.secret_key_path.read_text(),
        lifetime_seconds=settings.auth_jwt.access_token_expire_minutes * 60,
        algorithm=settings.auth_jwt.algorithm,
        public_key=settings.auth_jwt.public_key_path.read_text(),
    )
