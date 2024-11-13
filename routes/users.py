from fastapi import (
    APIRouter,
    Depends,
)

from app.schemas import UserAuth, Token
from auth.authentication import authenticate_user
from auth import utils as auth_utils

router = APIRouter(prefix="/users")

@router.post("/login", response_model=Token)
def auth_user_issue_jwt(
    user: UserAuth = Depends(authenticate_user),
):
    jwt_payload = {
        "sub": user.username,
        "username": user.username,
    }
    token = auth_utils.encode_jwt(jwt_payload)
    return Token(
        access_type=token,
        token_type="Bearer",
    )