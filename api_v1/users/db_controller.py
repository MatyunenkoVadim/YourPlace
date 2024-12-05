from sqlalchemy import select
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession

# from core.models import User
from .schemas import UserAuth, UserInDB


class UsersRepository:
    @classmethod
    async def create_new_user(cls, session: AsyncSession, user_auth: UserAuth) -> User:
        user = User(
            username=user_auth.username,
            phone=user_auth.phone,
            fullname=user_auth.fullname,
            password=user_auth.hashed_password.decode(),
            active=user_auth.active,
        )
        session.add(user)
        await session.commit()
        # await session.refresh(reservation)
        return user

    @classmethod
    async def find_all_users(cls, session: AsyncSession) -> list[User]:
        stmt = select(User).order_by(User.id)
        result: Result = await session.execute(stmt)
        users = result.scalars().all()
        return list(users)

    @classmethod
    async def find_user(cls, session: AsyncSession, username: str) -> User | None:
        stmt = select(User).where(User.username == username)
        result: Result = await session.execute(stmt)
        user = result.scalars().first()
        return user