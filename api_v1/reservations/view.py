"""
Этот модуль определяет маршруты для управления бронированиями, включая получение
всех бронирований, создание нового бронирования и получение бронирований пользователя.

Маршруты:
- get_reservations: Возвращает список всех бронирований для администраторов.
- create_reservation: Создает новое бронирование.
- get_reservation_by_id: Возвращает бронирование по его идентификатору.
- get_reservation_user: Возвращает список бронирований для текущего пользователя.

Зависимости:
- Использует FastAPI для создания маршрутов и управления зависимостями.
- Использует SQLAlchemy для взаимодействия с базой данных.

Контекст:
Этот файл является частью системы управления бронированиями и используется для
обработки запросов пользователей на создание и просмотр бронирований.
"""

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
    """
    Возвращает список всех бронирований для администраторов.

    Параметры:
    - session: Асинхронная сессия SQLAlchemy.
    - user: Текущий аутентифицированный пользователь.

    Возвращает:
    - Список объектов ReservationResponse, представляющих все бронирования.

    Исключения:
    - HTTPException 403: Если пользователь не является администратором.
    """
    if user.is_admin or user.is_superuser:
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
    """
    Создает новое бронирование.

    Параметры:
    - reservation: Данные для создания нового бронирования.
    - session: Асинхронная сессия SQLAlchemy.
    - user: Текущий аутентифицированный пользователь.

    Возвращает:
    - Объект ReservationResponse, представляющий созданное бронирование.

    Исключения:
    - HTTPException 403: Если пользователь не является администратором.
    """
    if user.is_admin or user.is_superuser:
        return await ReservationRepository.add_one_reservation(session=session, data=reservation)
    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Permission denied"
        )


@router.get("/reservations/{reservation_id}", response_model=ReservationResponse)
async def get_reservation_by_id(
    reservation_id: int,
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
    user: User = Depends(current_active_user),
):
    """
    Возвращает бронирование по его идентификатору.

    Параметры:
    - reservation_id: Идентификатор бронирования.
    - session: Асинхронная сессия SQLAlchemy.
    - user: Текущий аутентифицированный пользователь.

    Возвращает:
    - Объект ReservationResponse, представляющий бронирование.

    Исключения:
    - HTTPException 403: Если пользователь не является администратором.
    - HTTPException 404: Если бронирование не найдено.
    """
    if user.is_admin or user.is_superuser:
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
    """
    Возвращает список бронирований для текущего пользователя.

    Параметры:
    - session: Асинхронная сессия SQLAlchemy.
    - user: Текущий аутентифицированный пользователь.

    Возвращает:
    - Список объектов ReservationResponse, представляющих бронирования пользователя.
    """
    return await ReservationRepository.find_reservation_user(session=session, user_id=user.id)
