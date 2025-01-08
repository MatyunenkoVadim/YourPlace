from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import User
from core.models.db_helper import db_helper
from api_v1.users.fastapi_users_routes import current_active_user
from .db_controller import ReservationRepository
from .schemas import ReservationCreate, ReservationResponse

router = APIRouter(tags=["Reservation"])


@router.get("/reservations", response_model=list[ReservationResponse])
async def get_reservations(
        session: AsyncSession = Depends(db_helper.scoped_session_dependency),
        user: User = Depends(current_active_user),
):
    if user.is_admin == True or user.is_superuser == True:
        return await ReservationRepository.find_all_reservation(session=session)
    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Permission denied"
        )


@router.post("/reservation", response_model=ReservationResponse)
async def create_reservation(
        reservation: ReservationCreate,
        session: AsyncSession = Depends(db_helper.scoped_session_dependency),
        user: User = Depends(current_active_user),
):
    if user.is_admin == True or user.is_superuser == True:
        return await ReservationRepository.add_one_reservation(session=session, data=reservation)
    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Permission denied"
        )


@router.get("/reservations/{reservation_id}", response_model=ReservationResponse)
async def get_reservations(
        reservation_id: int,
        session: AsyncSession = Depends(db_helper.scoped_session_dependency),
        user: User = Depends(current_active_user),
):
    if user.is_admin == True or user.is_superuser == True:
        reservation = await ReservationRepository.find_reservation(session=session, reservation_id=reservation_id)
        if reservation is not None:
            return reservation

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Reservation not found",
        )
    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Permission denied"
        )

@router.get("/users/reservations", response_model=list[ReservationResponse])
async def get_reservation_user(
        session: AsyncSession = Depends(db_helper.scoped_session_dependency),
        user: User = Depends(current_active_user),
):
    return await ReservationRepository.find_reservation_user(session=session, user_id=user.id)