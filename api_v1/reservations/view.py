from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import db_helper
from .db_controller import ReservationRepository
from .schemas import ReservationCreate, ReservationResponse

router = APIRouter()


@router.get("", response_model=list[ReservationResponse])
async def get_reservations(
        session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    return await ReservationRepository.find_all_reservation(session=session)


@router.post("", response_model=ReservationResponse)
async def create_reservation(
        reservation: ReservationCreate,
        session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    return await ReservationRepository.add_one_reservation(session=session, data=reservation)


@router.get("/{reservation_id}", response_model=ReservationResponse)
async def get_reservations(
        reservation_id: int,
        session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    reservation = await ReservationRepository.find_reservation(session=session, reservation_id=reservation_id)
    if reservation is not None:
        return reservation

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Reservation not found",
    )