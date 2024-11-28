from http import HTTPStatus

import pytest

from src.services import users_service
from tests.conftest import UserFactory


async def test_get_all_users(async_client, async_session, superuser_token):
    expected_length = 5
    async_session.add_all(UserFactory.create_batch(expected_length))
    await async_session.commit()

    response = await async_client.get(
        '/users/all',
        headers={'Authorization': f'Bearer {superuser_token}'},
    )

    assert response.status_code == HTTPStatus.OK
    # expected_lenght + superuser
    assert len(response.json()['users']) == (expected_length + 1)


async def test_get_all_users_access_denied_if_not_superuser(
    async_client, async_session, user_token
):
    async_session.add_all(UserFactory.create_batch(5))
    await async_session.commit()

    response = await async_client.get(
        '/users/all',
        headers={'Authorization': f'Bearer {user_token}'},
    )

    assert response.status_code == HTTPStatus.FORBIDDEN
    assert response.json() == {'detail': 'Insufficient permissions.'}


async def test_get_user_by_id(async_client, superuser_token, user):
    response = await async_client.get(
        f'/users/{user.id}',
        headers={'Authorization': f'Bearer {superuser_token}'},
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


async def test_get_user_by_id_not_found(async_client, superuser_token, user):
    response = await async_client.get(
        f'/users/{user.id + 300}',
        headers={'Authorization': f'Bearer {superuser_token}'},
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'User not found.'}


async def test_get_user_by_id_access_denied_if_not_superuser(
    async_client, user_token, user
):
    response = await async_client.get(
        f'/users/{user.id}',
        headers={'Authorization': f'Bearer {user_token}'},
    )

    assert response.status_code == HTTPStatus.FORBIDDEN
    assert response.json() == {'detail': 'Insufficient permissions.'}


async def test_create_user(async_client, superuser_token):
    response = await async_client.post(
        '/users/',
        headers={'Authorization': f'Bearer {superuser_token}'},
        json={
            'username': 'testname',
            'email': 'test@test.com',
            'password': 'testpass',
            'is_verified': True,
        },
    )

    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        'username': 'testname',
        'email': 'test@test.com',
        'id': 2,
        'first_name': None,
        'last_name': None,
        'is_superuser': False,
        'is_active': True,
        'is_verified': True,
        'google_sub': None,
    }


@pytest.mark.parametrize(
    ('payload_creation', 'response_detail_message'),
    [
        (
            lambda user: {
                'username': user.username,
                'email': 'update@email.com',
                'password': 'testpass',
            },
            'Username already exists.',
        ),
        (
            lambda user: {
                'username': 'new_username',
                'email': user.email,
                'password': 'testpass',
            },
            'Email already exists.',
        ),
    ],
)
async def test_create_user_with_credentials_already_in_db(
    payload_creation,
    response_detail_message,
    async_client,
    superuser_token,
    user,
):
    payload = payload_creation(user)

    response = await async_client.post(
        '/users/',
        headers={'Authorization': f'Bearer {superuser_token}'},
        json=payload,
    )

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json() == {'detail': response_detail_message}


async def test_create_user_access_denied_if_not_superuser(
    async_client, user_token
):
    response = await async_client.post(
        '/users/',
        headers={'Authorization': f'Bearer {user_token}'},
        json={
            'username': 'testname',
            'email': 'test@test.com',
            'password': 'testpass',
            'is_verified': True,
        },
    )

    assert response.status_code == HTTPStatus.FORBIDDEN
    assert response.json() == {'detail': 'Insufficient permissions.'}


@pytest.mark.parametrize(
    ('payload_key', 'payload_value'),
    [
        ('username', 'update_username'),
        ('email', 'email@updated.com'),
    ],
)
async def test_update_user_info(
    payload_key, payload_value, async_client, superuser_token, user
):
    response = await async_client.patch(
        f'/users/{user.id}',
        headers={'Authorization': f'Bearer {superuser_token}'},
        json={payload_key: payload_value},
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json()[payload_key] == payload_value


async def test_update_user_info_user_not_found(
    async_client, superuser_token, user
):
    response = await async_client.patch(
        f'/users/{user.id + 300}',
        headers={'Authorization': f'Bearer {superuser_token}'},
        json={'usename': 'test'},
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'User not found.'}


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
    user,
    superuser_token,
    other_user,
):
    payload = update_payload(other_user)

    response = await async_client.patch(
        f'/users/{user.id}',
        headers={'Authorization': f'Bearer {superuser_token}'},
        json=payload,
    )

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json() == {'detail': response_detail_message}


async def test_update_user_info_denied_if_not_superuser(
    async_client, user_token, user
):
    response = await async_client.patch(
        f'/users/{user.id}',
        headers={'Authorization': f'Bearer {user_token}'},
        json={
            'is_verified': True,
        },
    )

    assert response.status_code == HTTPStatus.FORBIDDEN
    assert response.json() == {'detail': 'Insufficient permissions.'}


async def test_delete_user(async_client, async_session, superuser_token, user):
    response = await async_client.delete(
        f'/users/{user.id}',
        headers={'Authorization': f'Bearer {superuser_token}'},
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'User deleted.'}

    user_excluded = await users_service.get_user_by_id(
        session=async_session, user_id=user.id
    )

    assert not user_excluded


async def test_delete_user_not_found(async_client, superuser_token, user):
    response = await async_client.delete(
        f'/users/{user.id + 300}',
        headers={'Authorization': f'Bearer {superuser_token}'},
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'User not found.'}


async def test_delete_user_denied_if_not_superuser(
    async_client, user_token, other_user
):
    response = await async_client.delete(
        f'/users/{other_user.id}',
        headers={'Authorization': f'Bearer {user_token}'},
    )

    assert response.status_code == HTTPStatus.FORBIDDEN
    assert response.json() == {'detail': 'Insufficient permissions.'}


async def test_delete_superuser_denied(
    async_client, superuser_token, superuser
):
    response = await async_client.delete(
        f'/users/{superuser.id}',
        headers={'Authorization': f'Bearer {superuser_token}'},
    )

    assert response.status_code == HTTPStatus.FORBIDDEN
    assert response.json() == {
        'detail': 'Super users are not allowed to delete themselves.'
    }
