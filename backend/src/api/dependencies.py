from http import HTTPStatus
from typing import Annotated

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jwt import ExpiredSignatureError, PyJWTError, decode
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.database import AsyncSessionLocal
from src.core.settings import settings
from src.models import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/auth/token')


async def get_session():  # pragma: no cover
    async with AsyncSessionLocal() as session: # type: ignore
        yield session


SessionDep = Annotated[AsyncSession, Depends(get_session)]
TokenDep = Annotated[str, Depends(oauth2_scheme)]


async def get_current_user(session: SessionDep, token: TokenDep):
    credentials_exception = HTTPException(
        status_code=HTTPStatus.UNAUTHORIZED,
        detail='Could not validate credentials.',
        headers={'WWW-Authenticate': 'Bearer'},
    )

    try:
        payload = decode(
            token, settings.SECRET_KEY, algorithms=settings.ALGORITHM
        )
        email = payload.get('sub')
        if not email:
            raise credentials_exception
    except ExpiredSignatureError:
        raise credentials_exception
    except PyJWTError:
        raise credentials_exception

    user_db = await session.scalar(select(User).where(User.email == email))

    if not user_db:
        raise credentials_exception

    return user_db


CurrentUser = Annotated[User, Depends(get_current_user)]


async def get_current_active_superuser(current_user: CurrentUser) -> User:
    if not current_user.is_superuser:
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN,
            detail='Insufficient permissions.',
        )
    return current_user
