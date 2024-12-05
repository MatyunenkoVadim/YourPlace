from fastapi import APIRouter

from core.config import settings

from api_v1.dependencies.auth.backend import authentication_backend
from .fastapi_users_routes import fastapi_users
from ..dependencies.auth.schemas import (
    UserRead,
    UserCreate,
)

router = APIRouter(
    prefix=settings.auth,
    tags=["Auth"],
)

# /login
# /logout
router.include_router(
    router=fastapi_users.get_auth_router(
        authentication_backend,
        # requires_verification=True,
    ),
)

# /register
router.include_router(
    router=fastapi_users.get_register_router(
        UserRead,
        UserCreate,
    ),
)