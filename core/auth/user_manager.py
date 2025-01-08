"""
Этот модуль определяет менеджер пользователей, который управляет событиями, связанными с пользователями,
такими как регистрация, запрос на верификацию и сброс пароля.

Классы:
- UserManager: Менеджер пользователей, который наследуется от IntegerIDMixin и BaseUserManager.
  Он переопределяет методы для обработки событий после регистрации, запроса верификации и сброса пароля.

Зависимости:
- Использует FastAPI Users для управления пользователями.
- Использует настройки из core.config для секретов токенов.
- Использует модели из core.models для представления пользователей.

Контекст:
Этот файл является частью системы управления пользователями и используется для обработки
различных событий, связанных с пользователями, таких как регистрация и восстановление пароля.
"""

import logging
from typing import Optional, TYPE_CHECKING

from fastapi_users import (
    BaseUserManager,
    IntegerIDMixin,
)

from core.config import settings
from core.models import User

if TYPE_CHECKING:
    from fastapi import Request

log = logging.getLogger(__name__)

class UserManager(IntegerIDMixin, BaseUserManager[User, int]):
    """
    Менеджер пользователей, который управляет событиями, связанными с пользователями.
    """

    reset_password_token_secret = settings.auth_jwt.reset_password_token_secret
    verification_token_secret = settings.auth_jwt.verification_token_secret

    async def on_after_register(
        self,
        user: User,
        request: Optional["Request"] = None,
    ):
        """
        Обрабатывает событие после регистрации пользователя.

        Параметры:
        - user: Зарегистрированный пользователь.
        - request: Объект запроса, если доступен.
        """
        log.warning(
            "User %r has registered.",
            user.id,
        )

    async def on_after_request_verify(
        self,
        user: User,
        token: str,
        request: Optional["Request"] = None,
    ):
        """
        Обрабатывает событие после запроса верификации пользователя.

        Параметры:
        - user: Пользователь, запросивший верификацию.
        - token: Токен верификации.
        - request: Объект запроса, если доступен.
        """
        log.warning(
            "Verification requested for user %r. Verification token: %r",
            user.id,
            token,
        )

    async def on_after_forgot_password(
        self,
        user: User,
        token: str,
        request: Optional["Request"] = None,
    ):
        """
        Обрабатывает событие после запроса на сброс пароля пользователем.

        Параметры:
        - user: Пользователь, запросивший сброс пароля.
        - token: Токен сброса пароля.
        - request: Объект запроса, если доступен.
        """
        log.warning(
            "User %r has forgot their password. Reset token: %r",
            user.id,
            token,
        )