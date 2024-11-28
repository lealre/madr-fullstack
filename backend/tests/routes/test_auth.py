from http import HTTPStatus

from freezegun import freeze_time


async def test_get_token(async_client, user):
    response = await async_client.post(
        '/auth/token',
        data={'username': user.email, 'password': user.clean_password},
    )

    token = response.json()

    assert response.status_code == HTTPStatus.OK
    assert 'access_token' in token
    assert 'token_type' in token


async def test_token_wrong_user(async_client, user):
    response = await async_client.post(
        '/auth/token',
        data={
            'username': 'no_user@no_domain.com',
            'password': user.clean_password,
        },
    )
    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json() == {'detail': 'Incorrect email or password.'}


async def test_token_wrong_password(async_client, user):
    response = await async_client.post(
        '/auth/token',
        data={'username': user.email, 'password': 'wrong_password'},
    )
    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json() == {'detail': 'Incorrect email or password.'}


async def test_token_expired_after_time(async_client, user):
    with freeze_time('2024-01-01 12:00:00'):
        response = await async_client.post(
            '/auth/token',
            data={'username': user.email, 'password': user.clean_password},
        )

        assert response.status_code == HTTPStatus.OK
        token = response.json()['access_token']

    with freeze_time('2024-01-01 13:01:00'):
        response = await async_client.patch(
            f'/users/me/{user.id}',
            headers={'Authorization': f'Bearer {token}'},
            json={
                'username': 'update',
                'email': 'update@update.com',
                'password': 'update',
            },
        )

        assert response.status_code == HTTPStatus.UNAUTHORIZED
        assert response.json() == {'detail': 'Could not validate credentials.'}


async def test_refresh_token(async_client, token, user):
    response = await async_client.post(
        '/auth/refresh_token', headers={'Authorization': f'Bearer {token}'}
    )

    data = response.json()

    assert response.status_code == HTTPStatus.OK
    assert 'access_token' in data
    assert 'token_type' in data


async def test_token_expired_dont_refresh(async_client, user):
    with freeze_time('2024-01-01 12:00:00'):
        response = await async_client.post(
            '/auth/token',
            data={'username': user.email, 'password': user.clean_password},
        )

        assert response.status_code == HTTPStatus.OK
        token = response.json()['access_token']

    with freeze_time('2024-01-01 13:01:00'):
        response = await async_client.post(
            '/auth/refresh_token', headers={'Authorization': f'Bearer {token}'}
        )

        assert response.status_code == HTTPStatus.UNAUTHORIZED
        assert response.json() == {'detail': 'Could not validate credentials.'}


async def test_user_not_found_get_current_user(async_client, user, token):
    response = await async_client.delete(
        f'/users/me/{user.id}', headers={'Authorization': f'Bearer {token}'}
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'User deleted.'}

    response = await async_client.post(
        '/auth/refresh_token', headers={'Authorization': f'Bearer {token}'}
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'Could not validate credentials.'}
