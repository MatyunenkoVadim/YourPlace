from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from api_v1.reservations.db_controller import ReservationRepository
from api_v1.reservations.schemas import ReservationResponse

from api_v1.users.fastapi_users_routes import fastapi_users, current_active_user
from api_v1.dependencies.auth.schemas import (
    UserRead,
    UserUpdate,
)
from core.config import settings
from core.models import User
from core.models.db_helper import db_helper

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
