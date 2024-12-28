from http import HTTPStatus
from typing import Any

from fastapi import APIRouter, Depends, HTTPException

from src.api.dependencies import (
    CurrentUser,
    SessionDep,
    get_current_active_superuser,
)
from src.schemas.base import Message
from src.schemas.users import (
    SuperUserRequestCreate,
    SuperUserRequestUpdate,
    UserListResponse,
    UserResponse,
)
from src.services import user_service

router = APIRouter(dependencies=[Depends(get_current_active_superuser)])


@router.post('', response_model=UserResponse, status_code=HTTPStatus.CREATED)
async def create_user(
    session: SessionDep, user_in: SuperUserRequestCreate
) -> Any:
    """
    Create a user account.
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


@router.get('/all', response_model=UserListResponse)
async def read_users(
    session: SessionDep, limit: int = 100, offset: int = 0
) -> Any:
    """
    Retrieve all user accounts.
    """
    users = await user_service.get_users_list(
        session=session, offset=offset, limit=limit
    )

    return {'users': users}


@router.get('/{user_id}', response_model=UserResponse)
async def get_user_by_id(session: SessionDep, user_id: int) -> Any:
    """
    Get account by ID.
    """
    user_db = await user_service.get_user_by_id(
        session=session, user_id=user_id
    )

    if not user_db:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='User not found.'
        )

    return user_db


@router.patch('/{user_id}', response_model=UserResponse)
async def update_user_info(
    session: SessionDep, user_id: int, user_in: SuperUserRequestUpdate
) -> Any:
    """
    Update a user's account info.
    """
    user_to_update = await user_service.get_user_by_id(
        session=session, user_id=user_id
    )

    if not user_to_update:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='User not found.'
        )

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
        session=session, user_info=user_in, user_to_update=user_to_update
    )

    return user_updated


@router.delete('/{user_id}', status_code=HTTPStatus.OK, response_model=Message)
async def delete_user(
    session: SessionDep, user_id: int, current_user: CurrentUser
) -> Message:
    """
    Delete a user account by ID.
    """
    user_to_delete = await user_service.get_user_by_id(
        session=session, user_id=user_id
    )

    if not user_to_delete:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='User not found.'
        )
    if user_to_delete.id == current_user.id:
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN,
            detail='Super users are not allowed to delete themselves.',
        )

    await session.delete(user_to_delete)
    await session.commit()

    return Message(message='User deleted.')
