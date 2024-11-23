from datetime import datetime

from fastapi import APIRouter
from starlette.requests import Request
from starlette.responses import HTMLResponse
from starlette.templating import Jinja2Templates

from api_v1.reservations.db_controller import ReservationRepository
from api_v1.reservations.schemas import ReservationCreate

router = APIRouter()
templates = Jinja2Templates(directory="templates")


@router.get("/guests", response_class=HTMLResponse)
async def select_guests(request: Request):
    return templates.TemplateResponse("guests.html", {"request": request})


@router.get("/datetime", response_class=HTMLResponse)
async def select_datetime(request: Request, guest_count: int):
    return templates.TemplateResponse("datetime.html", {"request": request, "guest_count": guest_count})


@router.get("/table_selection", response_class=HTMLResponse)
async def select_table(request: Request, guest_count: int, reservation_date: str):
    print(f"Guest count: {guest_count}, Reservation date: {reservation_date}")
    try:
        reservation_date = datetime.fromisoformat(reservation_date)
    except ValueError:
        return HTMLResponse(content="Invalid date format.", status_code=400)

    return templates.TemplateResponse("table_selection.html", {
        "request": request,
        "guest_count": guest_count,
        "reservation_date": reservation_date
    })


@router.post("/result", response_class=HTMLResponse)
async def reserve_table(request: Request):
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
    await ReservationRepository.add_one_reservation(new_reservation)

    print(f"Reservation made: {guest_count} guests on {reservation_date} at Table {table_number}")

    return templates.TemplateResponse("result.html", {
        "request": request,
        "guest_count": guest_count,
        "reservation_date": reservation_date.strftime("%Y-%m-%d %H:%M:%S"),
        "table_number": table_number
    })
  