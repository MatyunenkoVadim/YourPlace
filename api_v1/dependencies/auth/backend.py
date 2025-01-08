"""
Этот модуль определяет бэкенд аутентификации для FastAPI Users с использованием JWT.

Переменные:
- authentication_backend: Бэкенд аутентификации, использующий JWT стратегию и Bearer транспорт.

Зависимости:
- Использует FastAPI Users для работы с аутентификацией.
- Использует JWT стратегию и Bearer транспорт для аутентификации.

Контекст:
Этот файл является частью системы аутентификации и используется для настройки
бэкенда аутентификации, который управляет процессом аутентификации пользователей.
"""

from fastapi_users.authentication import AuthenticationBackend
from core.auth.transport import bearer_transport
from .strategy import get_jwt_strategy

authentication_backend = AuthenticationBackend(
    name="jwt",
    transport=bearer_transport,
    get_strategy=get_jwt_strategy,
)
