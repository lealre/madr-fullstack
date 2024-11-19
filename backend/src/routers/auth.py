from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from src.core.database import T_Session
from src.core.security import CurrentUser
from src.schemas.token import Token
from src.services.auth_service import generate_access_token, refresh_token

router = APIRouter(prefix='/auth', tags=['auth'])


@router.post('/token', response_model=Token)
async def login_for_access_token(
    session: T_Session, form_data: OAuth2PasswordRequestForm = Depends()
):
    access_token = await generate_access_token(
        session=session, form_data=form_data
    )

    return {'access_token': access_token, 'token_type': 'bearer'}


@router.post('/refresh_token', response_model=Token)
def refresh_access_token(user: CurrentUser):
    new_access_token = refresh_token(user=user)

    return {'access_token': new_access_token, 'token_type': 'bearer'}
