from fastapi import APIRouter
from api_v1.reservations.view import router as router_reservation
from api_v1.users.view import router as router_users

router = APIRouter()

router.include_router(router=router_reservation, prefix="/reservation")
router.include_router(router=router_users, prefix="/user")