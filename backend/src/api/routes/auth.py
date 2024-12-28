from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select

from src.api.dependencies import CurrentUser, SessionDep
from src.core.security import create_access_token, verify_password
from src.models import User
from src.schemas.token import Token

router = APIRouter()


@router.post('/token', status_code=HTTPStatus.OK, response_model=Token)
async def access_token(
    session: SessionDep, form_data: OAuth2PasswordRequestForm = Depends()
) -> Token:
    """
    Generate an access token for a user.
    """
    async with session.begin():
        user = await session.scalar(
            select(User).where(User.email == form_data.username)
        )

    if not user:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Incorrect email or password.',
        )

    if not verify_password(form_data.password, user.password_hash):
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Incorrect email or password.',
        )

    access_token = create_access_token(data={'sub': user.email})

    return Token(access_token=access_token, token_type='bearer')


@router.post('/refresh_token', response_model=Token)
async def refresh_access_token(user: CurrentUser) -> Token:
    """
    Refreshes the access token for an authenticated user.
    """
    new_access_token = create_access_token(data={'sub': user.email})

    return Token(access_token=new_access_token, token_type='bearer')
