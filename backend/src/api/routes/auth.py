from http import HTTPStatus

from authlib.integrations.starlette_client import OAuthError
from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select

from src.api.dependencies import CurrentUser, SessionDep
from src.core.security import create_access_token, oauth, verify_password
from src.core.settings import settings
from src.models import User
from src.schemas.token import Token
from src.schemas.users import GoogleUser

router = APIRouter()


@router.post('/token', status_code=HTTPStatus.OK, response_model=Token)
async def access_token(
    session: SessionDep, form_data: OAuth2PasswordRequestForm = Depends()
):
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

    return {'access_token': access_token, 'token_type': 'bearer'}


@router.post('/refresh_token', response_model=Token)
def refresh_access_token(user: CurrentUser):
    new_access_token = create_access_token(data={'sub': user.email})

    return {'access_token': new_access_token, 'token_type': 'bearer'}


@router.get('/google')
async def login_google(request: Request):
    return await oauth.google.authorize_redirect(
        request, settings.GOOGLE_REDIRECT_URI
    )


@router.get('/callback/google')
async def auth_google(request: Request):
    try:
        user_response = await oauth.google.authorize_access_token(request)
    except OAuthError:
        return HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED,
            detail='Could not validate credentials',
        )

    # From here implement the rest of the logic: generate the token,...
    user_info = GoogleUser(**user_response.get('userinfo'))

    return user_info
