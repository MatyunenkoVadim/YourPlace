from datetime import datetime, timedelta
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from starlette.requests import Request
from starlette.responses import HTMLResponse
from starlette.templating import Jinja2Templates

from app.authentication import authenticate_user, ACCESS_TOKEN_EXPIRE_MINUTES, create_access_token, \
    get_current_active_user
from app.repository import ReservationRepository
from app.schemas import ReservationCreate, Token, User

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

@router.post("/token")
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
) -> Token:
    user = authenticate_user(..., form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")


@router.get("/users/me/", response_model=User)
async def read_users_me(
    current_user: Annotated[User, Depends(get_current_active_user)],
):
    return current_user


@router.get("/users/me/items/")
async def read_own_items(
    current_user: Annotated[User, Depends(get_current_active_user)],
):
    return [{"item_id": "Foo", "owner": current_user.username}]
  