"""
Этот модуль определяет маршруты для управления бронированиями столов через веб-интерфейс.

Маршруты:
- select_reservation: Отображает страницу выбора бронирования.
- select_table: Отображает страницу выбора стола для бронирования.
- reserve_table: Обрабатывает данные формы для создания нового бронирования.

Зависимости:
- Использует FastAPI для создания маршрутов и управления зависимостями.
- Использует SQLAlchemy для взаимодействия с базой данных.
- Использует Jinja2 для рендеринга HTML-шаблонов.

Контекст:
Этот файл является частью системы управления бронированиями и используется для
обработки запросов пользователей на создание и просмотр бронирований.
"""

from datetime import datetime
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.requests import Request
from starlette.responses import HTMLResponse
from starlette.templating import Jinja2Templates
from api_v1.reservations.schemas import ReservationCreate
from api_v1.reservations.db_controller import ReservationRepository
from core.models.db_helper import db_helper

router = APIRouter()
templates = Jinja2Templates(directory="resources/static")


@router.get("/reservation", response_class=HTMLResponse)
async def select_reservation(request: Request, guest_count: int = None, reservation_date: str = None):
    """
    Отображает страницу выбора бронирования.

    Параметры:
    - request: Объект запроса.
    - guest_count: Количество гостей для бронирования.
    - reservation_date: Дата бронирования в формате строки.

    Возвращает:
    - HTML-ответ с рендерингом шаблона.
    """
    return templates.TemplateResponse("index.html", {
        "request": request,
        "guest_count": guest_count,
        "reservation_date": reservation_date
    })


@router.get("/table_selection", response_class=HTMLResponse)
async def select_table(request: Request, guest_count: int, reservation_date: str):
    """
    Отображает страницу выбора стола для бронирования.

    Параметры:
    - request: Объект запроса.
    - guest_count: Количество гостей для бронирования.
    - reservation_date: Дата бронирования в формате строки.

    Возвращает:
    - HTML-ответ с рендерингом шаблона или сообщение об ошибке, если формат даты неверен.
    """
    print(f"Guest count: {guest_count}, Reservation date: {reservation_date}")
    try:
        reservation_date = datetime.fromisoformat(reservation_date)
    except ValueError:
        return HTMLResponse(content="Invalid date format.", status_code=400)

    return templates.TemplateResponse("index.html", {
        "request": request,
        "guest_count": guest_count,
        "reservation_date": reservation_date
    })


@router.post("/result", response_class=HTMLResponse)
async def reserve_table(
        request: Request,
        session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    """
    Обрабатывает данные формы для создания нового бронирования.

    Параметры:
    - request: Объект запроса.
    - session: Асинхронная сессия SQLAlchemy.

    Возвращает:
    - HTML-ответ с рендерингом шаблона или сообщение об ошибке, если формат даты неверен.
    """
    form_data = await request.form()
    guest_count = int(form_data.get("guest_count"))
    reservation_date_str = form_data.get("reservation_date")
    table_number = form_data.get("table_number")

    try:
        reservation_date = datetime.fromisoformat(reservation_date_str)
    except ValueError:
        return HTMLResponse(content="Invalid reservation date format.", status_code=400)

    new_reservation = ReservationCreate(
        guest_count=guest_count,
        reservation_date=reservation_date,
        table_number=table_number
    )
    await ReservationRepository.add_one_reservation(session=session, data=new_reservation)

    print(f"Reservation made: {guest_count} guests on {reservation_date} at Table {table_number}")

    return templates.TemplateResponse("index.html", {
        "request": request,
        "guest_count": guest_count,
        "reservation_date": reservation_date.strftime("%Y-%m-%d %H:%M:%S"),
        "table_number": table_number
    })