from http import HTTPStatus

from httpx import AsyncClient
from jwt import decode

from src.core.security import create_access_token
from src.core.settings import settings


def test_jwt() -> None:
    data = {'sub': 'test@test.com'}
    token = create_access_token(data)

    result = decode(
        token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
    )

    assert result['sub'] == data['sub']
    assert result['exp']


async def test_jwt_invalid_token(async_client: AsyncClient) -> None:
    response = await async_client.delete(
        '/users/me', headers={'Authorization': 'Bearer token-invalido'}
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'Could not validate credentials.'}
