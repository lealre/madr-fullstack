from http import HTTPStatus

import pytest

from src.core.security import verify_password
from src.services import users_service


async def test_create_user(async_client):
    response = await async_client.post(
        '/users/singup',
        json={
            'username': 'testname',
            'email': 'test@test.com',
            'password': 'testpass',
        },
    )

    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        'username': 'testname',
        'email': 'test@test.com',
        'id': 1,
        'first_name': None,
        'last_name': None,
        'is_superuser': False,
        'is_active': True,
        'is_verified': False,
        'google_sub': None,
    }


async def test_create_user_with_duplicated_username(async_client, user):
    response = await async_client.post(
        '/users/singup',
        json={
            'username': user.username,
            'email': 'different@email.com',
            'password': 'testpass',
        },
    )

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json() == {'detail': 'Username already exists.'}


async def test_create_user_with_duplicated_email(async_client, user):
    response = await async_client.post(
        '/users/singup',
        json={
            'username': 'different_username',
            'email': user.email,
            'password': 'testpass',
        },
    )

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json() == {'detail': 'Email already exists.'}


async def test_get_user_info_me(async_client, user, user_token):
    response = await async_client.get(
        '/users/me/',
        headers={'Authorization': f'Bearer {user_token}'},
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'username': user.username,
        'email': user.email,
        'id': user.id,
        'first_name': user.first_name,
        'last_name': user.last_name,
        'is_superuser': user.is_superuser,
        'is_active': user.is_active,
        'is_verified': user.is_verified,
        'google_sub': user.google_sub,
    }


async def test_get_user_info_me_not_authenticated(async_client):
    response = await async_client.get('/users/me/')

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'Not authenticated'}


async def test_update_user_info(async_client, user, user_token):
    username_updated = 'update_name'
    email_updated = 'update@email.com'
    response = await async_client.patch(
        '/users/me/',
        headers={'Authorization': f'Bearer {user_token}'},
        json={
            'username': username_updated,
            'email': email_updated,
        },
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'username': username_updated,
        'email': email_updated,
        'id': user.id,
        'first_name': user.first_name,
        'last_name': user.last_name,
        'is_superuser': user.is_superuser,
        'is_active': user.is_active,
        'is_verified': user.is_verified,
        'google_sub': user.google_sub,
    }


@pytest.mark.parametrize(
    ('update_payload', 'response_detail_message'),
    [
        (
            lambda other_user: {
                'username': other_user.username,
                'email': 'update@email.com',
            },
            'Username already exists.',
        ),
        (
            lambda other_user: {
                'username': 'new_username',
                'email': other_user.email,
            },
            'Email already exists.',
        ),
    ],
)
async def test_update_user_info_with_credentials_already_in_db(  # noqa: PLR0917, PLR0913
    update_payload,
    response_detail_message,
    async_client,
    user_token,
    other_user,
):
    payload = update_payload(other_user)

    response = await async_client.patch(
        '/users/me/',
        headers={'Authorization': f'Bearer {user_token}'},
        json=payload,
    )

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json() == {'detail': response_detail_message}


async def test_update_user_password(
    async_client, async_session, user, user_token
):
    new_password = 'new_password'

    response = await async_client.patch(
        '/users/me/change-password/',
        headers={'Authorization': f'Bearer {user_token}'},
        json={
            'password': new_password,
            'password_confirmation': new_password,
        },
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'Password has been changed!'}

    updated_user = await users_service.get_user_by_id(
        session=async_session, user_id=user.id
    )

    assert updated_user
    assert verify_password(new_password, updated_user.password_hash)


async def test_update_user_password_mismatch(async_client, user, user_token):
    new_password = 'new_password'

    response = await async_client.patch(
        '/users/me/change-password',
        headers={'Authorization': f'Bearer {user_token}'},
        json={
            'password': new_password + 'difference',
            'password_confirmation': new_password,
        },
    )

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json() == {'detail': 'Passwords dont match.'}


async def test_delete_user(async_client, user_token):
    response = await async_client.delete(
        '/users/me/',
        headers={'Authorization': f'Bearer {user_token}'},
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'User deleted.'}
