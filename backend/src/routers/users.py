from http import HTTPStatus

from fastapi import APIRouter

from src.core.database import T_Session
from src.core.security import CurrentUser
from src.schemas.base import Message
from src.schemas.users import UserPublic, UserSchema, UsersList
from src.services.users_service import (
    delete_user_in_db,
    register_new_user_in_db,
    update_user_info_in_db,
    get_users_lis_from_db
)

router = APIRouter(prefix='/users', tags=['users'])


@router.post('/', response_model=UserPublic, status_code=HTTPStatus.CREATED)
async def create_user(user: UserSchema, session: T_Session):
    user_db = await register_new_user_in_db(session=session, user=user)
    return user_db


@router.get('/', response_model=UsersList, status_code=HTTPStatus.OK)
async def get_all_users(session: T_Session, user: CurrentUser):
    users_db = await get_users_lis_from_db(session=session)
    return {'users':users_db}


@router.put('/{user_id}', response_model=UserPublic)
async def update_user(
    user_id: int,
    user: UserSchema,
    session: T_Session,
    current_user: CurrentUser,
):
    user_updated = await update_user_info_in_db(
        session=session, user_id=user_id, user=user, current_user=current_user
    )
    return user_updated


@router.delete('/{user_id}', response_model=Message)
async def delete_user(
    user_id: int,
    session: T_Session,
    current_user: CurrentUser,
):
    await delete_user_in_db(
        session=session, user_id=user_id, current_user=current_user
    )

    return {'message': 'User Deleted.'}
