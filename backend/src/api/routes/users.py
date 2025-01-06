from http import HTTPStatus
from typing import Any

from fastapi import APIRouter, HTTPException

from src.api.dependencies import (
    CurrentUser,
    SessionDep,
)
from src.schemas.base import Message
from src.schemas.users import (
    PasswordChange,
    UserRequestCreate,
    UserRequestUpdate,
    UserResponse,
)
from src.services import user_service

router = APIRouter()


@router.post(
    '/singup', status_code=HTTPStatus.CREATED, response_model=UserResponse
)
async def singup(session: SessionDep, user_in: UserRequestCreate) -> Any:
    """
    Create an account.
    """
    user_db = await user_service.get_user(
        session=session, user_email=user_in.email, username=user_in.username
    )

    if user_db:
        if user_db.username == user_in.username:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail='Username already exists.',
            )
        if user_db.email == user_in.email:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail='Email already exists.',
            )

    new_user = await user_service.add_user(session=session, user=user_in)

    return new_user


@router.get('/me', response_model=UserResponse)
async def get_user_info_me(current_user: CurrentUser) -> Any:
    """
    Get own account details.
    """
    return current_user


@router.patch('/me', response_model=UserResponse)
async def update_user_info_me(
    session: SessionDep,
    user_in: UserRequestUpdate,
    current_user: CurrentUser,
) -> Any:
    """
    Update own account information.
    """
    user_db = await user_service.get_user(
        session=session, username=user_in.username, user_email=user_in.email
    )

    if user_db:
        if user_db.username == user_in.username:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail='Username already exists.',
            )
        if user_db.email == user_in.email:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail='Email already exists.',
            )

    user_updated = await user_service.update_user_info(
        session=session, user_info=user_in, user_to_update=current_user
    )

    return user_updated


@router.patch('/me/change-password', response_model=Message)
async def update_password_me(
    session: SessionDep,
    passwords: PasswordChange,
    current_user: CurrentUser,
) -> Any:
    """
    Change own password
    """

    if passwords.password != passwords.password_confirmation:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST, detail='Passwords dont match.'
        )

    await user_service.change_password(
        session=session,
        user_to_update=current_user,
        password=passwords.password,
    )

    return {'message': 'Password has been changed!'}


@router.delete('/me', response_model=Message)
async def delete_user_me(
    session: SessionDep, current_user: CurrentUser
) -> Message:
    """
    Delete own account.
    """
    await user_service.delete_user(
        session=session, user_to_delete=current_user
    )

    return Message(message='User deleted.')
