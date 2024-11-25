from fastapi import (
    APIRouter,
    Depends,
)

from core.auth.schemas import Token
from api_v1.users.schemas import UserAuth
from core.auth.authentication import (
    authenticate_user,
    get_current_auth_active_user,
    get_current_token_payload_user,
)
from core.auth import utils as auth_utils

router = APIRouter(prefix="/users", tags=["Authorization"])

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
        access_token=token,
        token_type="Bearer",
    )


@router.get("/me")
def auth_user_check_self_info(
    payload: dict = Depends(get_current_token_payload_user),
    user: UserAuth = Depends(get_current_auth_active_user),
):
    iat = payload.get("iat")
    return {
        "username": user.username,
        "phone": user.phone,
        "logged_in_at": iat,
    }