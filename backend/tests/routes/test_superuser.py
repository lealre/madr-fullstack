from http import HTTPStatus

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
