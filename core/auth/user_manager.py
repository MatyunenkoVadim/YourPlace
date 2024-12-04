import logging
from typing import Optional, TYPE_CHECKING

from fastapi_users import (
    BaseUserManager,
)

from core.config import settings
# TODO: Решить вопрос с UserIdType
# from core.types.user_id import UserIdType
from core.models import UserDB
# from utils.webhooks.user import send_new_user_notification

if TYPE_CHECKING:
    from fastapi import Request

log = logging.getLogger(__name__)


class UserManager(IntegerIDMixin, BaseUserManager[UserDB, int]):
    reset_password_token_secret = settings.auth_jwt.reset_password_token_secret
    verification_token_secret = settings.auth_jwt.verification_token_secret

    async def on_after_register(
        self,
        user: UserDB,
        request: Optional["Request"] = None,
    ):
        log.warning(
            "User %r has registered.",
            user.id,
        )
        await send_new_user_notification(user)

    async def on_after_request_verify(
        self,
        user: UserDB,
        token: str,
        request: Optional["Request"] = None,
    ):
        log.warning(
            "Verification requested for user %r. Verification token: %r",
            user.id,
            token,
        )

    async def on_after_forgot_password(
        self,
        user: UserDB,
        token: str,
        request: Optional["Request"] = None,
    ):
        log.warning(
            "User %r has forgot their password. Reset token: %r",
            user.id,
            token,
        )
