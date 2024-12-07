from fastapi import APIRouter
from .reservations.view import router as router_reservation
from .users.auth import router as auth_router
from .users.user_info import router as user_router

router = APIRouter()

router.include_router(router=router_reservation, prefix="/reservation")
router.include_router(auth_router)
router.include_router(user_router)