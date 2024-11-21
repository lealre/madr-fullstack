from http import HTTPStatus

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.security import get_password_hash
from src.models import User
from src.schemas.users import UserSchema


async def register_new_user_in_db(session: AsyncSession, user: UserSchema):
    user_db = await session.scalar(
        select(User).where(
            (User.username == user.username) | (User.email == user.email)
        )
    )

    if user_db:
        if user_db.username == user.username:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail='Username already exists.',
            )
        if user_db.email == user.email:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail='Email already exists.',
            )

    hashed_password = get_password_hash(user.password)

    user_db = User(
        username=user.username, email=user.email, password=hashed_password
    )

    session.add(user_db)
    await session.commit()
    await session.refresh(user_db)

    return user_db


async def get_users_lis_from_db(session: AsyncSession):
    users_db = await session.scalars(select(User))
    return users_db


async def update_user_info_in_db(
    session: AsyncSession, user_id: int, user: UserSchema, current_user: User
):
    if current_user.id != user_id:
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN, detail='Not enough permissions.'
        )

    hashed_password = get_password_hash(user.password)

    current_user.username = user.username
    current_user.email = user.email
    current_user.password = hashed_password

    session.add(current_user)
    await session.commit()
    await session.refresh(current_user)

    return current_user


async def delete_user_in_db(
    session: AsyncSession, user_id: int, current_user: User
):
    if current_user.id != user_id:
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN, detail='Not enough permissions.'
        )

    await session.delete(current_user)
    await session.commit()
