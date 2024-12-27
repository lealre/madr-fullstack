import typing
from http import HTTPStatus

import pytest
from fastapi import HTTPException
from freezegun import freeze_time
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.dependencies import get_current_user
from src.core.security import create_access_token
from tests.conftest import MockedUser


async def test_get_token(async_client: AsyncClient, user: MockedUser) -> None:
    response = await async_client.post(
        '/auth/token',
        data={'username': user.email, 'password': user.clean_password},
    )

    token = response.json()

    assert response.status_code == HTTPStatus.OK
    assert 'access_token' in token
    assert 'token_type' in token


async def test_token_wrong_user(
    async_client: AsyncClient, user: MockedUser
) -> None:
    response = await async_client.post(
        '/auth/token',
        data={
            'username': 'no_user@no_domain.com',
            'password': user.clean_password,
        },
    )
    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json() == {'detail': 'Incorrect email or password.'}


async def test_token_wrong_password(
    async_client: AsyncClient, user: MockedUser
) -> None:
    response = await async_client.post(
        '/auth/token',
        data={'username': user.email, 'password': 'wrong_password'},
    )
    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json() == {'detail': 'Incorrect email or password.'}


async def test_token_expired_after_time(
    async_client: AsyncClient, user: MockedUser
) -> None:
    with freeze_time('2024-01-01 12:00:00'):
        response = await async_client.post(
            '/auth/token',
            data={'username': user.email, 'password': user.clean_password},
        )

        assert response.status_code == HTTPStatus.OK
        token = response.json()['access_token']

    with freeze_time('2024-01-01 13:01:00'):
        response = await async_client.patch(
            '/users/me/',
            headers={'Authorization': f'Bearer {token}'},
            json={
                'username': 'update',
                'email': 'update@update.com',
                'password': 'update',
            },
        )

        assert response.status_code == HTTPStatus.UNAUTHORIZED
        assert response.json() == {'detail': 'Could not validate credentials.'}


async def test_refresh_token(
    async_client: AsyncClient, user_token: str
) -> None:
    response = await async_client.post(
        '/auth/refresh_token/',
        headers={'Authorization': f'Bearer {user_token}'},
    )

    data = response.json()

    assert response.status_code == HTTPStatus.OK
    assert 'access_token' in data
    assert 'token_type' in data


async def test_token_expired_dont_refresh(
    async_client: AsyncClient, user: MockedUser
) -> None:
    with freeze_time('2024-01-01 12:00:00'):
        response = await async_client.post(
            '/auth/token',
            data={'username': user.email, 'password': user.clean_password},
        )

        assert response.status_code == HTTPStatus.OK
        token = response.json()['access_token']

    with freeze_time('2024-01-01 13:01:00'):
        response = await async_client.post(
            '/auth/refresh_token/',
            headers={'Authorization': f'Bearer {token}'},
        )

        assert response.status_code == HTTPStatus.UNAUTHORIZED
        assert response.json() == {'detail': 'Could not validate credentials.'}


async def test_user_not_found_get_current_user(
    async_client: AsyncClient, user_token: str
) -> None:
    response = await async_client.delete(
        '/users/me/',
        headers={'Authorization': f'Bearer {user_token}'},
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'User deleted.'}

    response = await async_client.post(
        '/auth/refresh_token/',
        headers={'Authorization': f'Bearer {user_token}'},
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'Could not validate credentials.'}


async def test_token_with_empty_email_sub(async_session: AsyncSession) -> None:
    token_payload: dict[str, typing.Any] = {}
    token = create_access_token(token_payload)

    with pytest.raises(HTTPException) as exc_info:
        await get_current_user(session=async_session, token=token)

    assert exc_info.value.status_code == HTTPStatus.UNAUTHORIZED
    assert exc_info.value.detail == 'Could not validate credentials.'
