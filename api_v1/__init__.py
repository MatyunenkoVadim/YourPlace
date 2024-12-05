from fastapi import APIRouter
from .reservations.view import router as router_reservation
from .users.view import router as router_users
from .users.auth import router as auth_router

router = APIRouter()

router.include_router(router=router_reservation, prefix="/reservation")
router.include_router(router=router_users, prefix="/user")
router.include_router(auth_router)