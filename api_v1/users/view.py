from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import db_helper
from .db_controller import UsersRepository
from .schemas import User, UserAuth

router = APIRouter(tags=["User"])


@router.get("", response_model=list[User])
async def get_users(
        session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    return await UsersRepository.find_all_users(session=session)


@router.post("", response_model=User)
async def create_user(
        user_auth: UserAuth,
        session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    return await UsersRepository.create_new_user(session=session, user_auth=user_auth)


@router.get("/{username}", response_model=User)
async def get_user(
        username: str,
        session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    reservation = await UsersRepository.find_user(session=session, username=username)
    if reservation is not None:
        return reservation

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="User not found",
    )