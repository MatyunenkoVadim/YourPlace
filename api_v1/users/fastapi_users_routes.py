"""
Этот модуль настраивает FastAPI Users для управления пользователями, включая
получение текущего активного пользователя и суперпользователя.

Переменные:
- fastapi_users: Экземпляр FastAPIUsers, настроенный для работы с моделью User.
- current_active_user: Зависимость для получения текущего активного пользователя.
- current_active_superuser: Зависимость для получения текущего активного суперпользователя.

Зависимости:
- Использует FastAPI Users для управления пользователями и аутентификацией.
- Использует SQLAlchemy для работы с моделью User.

Контекст:
Этот файл является частью системы управления пользователями и используется для
настройки FastAPI Users, обеспечивая доступ к текущим пользователям и суперпользователям.
"""

from fastapi_users import FastAPIUsers
from core.models import User
# from core.types.user_id import UserIdType
from api_v1.dependencies.auth.user_manager import get_user_manager
from api_v1.dependencies.auth.backend import authentication_backend

# Настройка FastAPI Users для работы с моделью User и аутентификацией
fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [authentication_backend],
)

# Зависимость для получения текущего активного пользователя
current_active_user = fastapi_users.current_user(active=True)

# Зависимость для получения текущего активного суперпользователя
current_active_superuser = fastapi_users.current_user(active=True, superuser=True)
