from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI, HTTPException, status
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from starlette.requests import Request
from starlette.responses import HTMLResponse
from starlette.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates

from app.customStaticFiles import CustomStaticFiles
from core.config import settings
from core.models import db_helper
# from routes.users import router as router_users
from api_v1 import router as router_api_vi
from routes.reservation import router as router_reservation


@asynccontextmanager
async def lifespan(app: FastAPI):
    # startup
    yield
    # shutdown
    await db_helper.dispose()


app = FastAPI(
    lifespan=lifespan,
)

templates = Jinja2Templates(directory="resources/static")
app.mount("/assets", CustomStaticFiles(directory="resources/static/assets"), name="assets")
app.mount("/static", StaticFiles(directory="resources/static"), name="static")

origins = [
    "http://localhost:8000",
    "http://127.0.0.1:8000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router=router_api_vi, prefix=settings.api_v1_prefix)
app.include_router(router_reservation)

react_routes = [
    "/reservation",
    "/table_selection",
    "/result",
    "/users/login",
    "/users/register",
    "/users/me",
]

@app.get("/", response_class=HTMLResponse)
async def read_index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/{path:path}")
async def serve_react_app(request: Request, path: str):
    if f"/{path}" in react_routes:
        return templates.TemplateResponse("index.html", {"request": request})
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Not Found",
    )
