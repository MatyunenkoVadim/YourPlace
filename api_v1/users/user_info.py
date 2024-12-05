from fastapi import APIRouter

from api_v1.users.fastapi_users_routes import fastapi_users
from api_v1.dependencies.auth.schemas import (
    UserRead,
    UserUpdate,
)
from core.config import settings

router = APIRouter(
    prefix=settings.users,
    tags=["Users"],
)

# /me
# /{id}
router.include_router(
    router=fastapi_users.get_users_router(
        UserRead,
        UserUpdate,
    ),
)
