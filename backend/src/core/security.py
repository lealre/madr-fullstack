from datetime import datetime, timedelta
from typing import Any
from zoneinfo import ZoneInfo

from fastapi.security import OAuth2PasswordBearer
from itsdangerous import URLSafeTimedSerializer
from jwt import encode
from pwdlib import PasswordHash

from src.core.settings import settings

pwd_context = PasswordHash.recommended()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/auth/token')


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict[str, Any]) -> str:
    to_encode = data.copy()
    expire = datetime.now(tz=ZoneInfo('UTC')) + timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )
    to_encode['exp'] = expire

    encoded_jwt = encode(
        to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM
    )

    return encoded_jwt


serializer = URLSafeTimedSerializer(
    secret_key=settings.SECRET_KEY, salt='email-configuration'
)


def create_url_safe_token(data: dict[str, str]) -> str:
    token = serializer.dumps(data)
    return token


def decode_url_safe_token(token: str) -> str | None:
    try:
        token_data: str = serializer.loads(token)
        return token_data
    except Exception:
        return None
