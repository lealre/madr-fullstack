from http import HTTPStatus


async def test_create_user(async_client):
    response = await async_client.post(
        '/users/',
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
    }


async def test_create_user_with_duplicated_username(async_client, user):
    response = await async_client.post(
        '/users/',
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
        '/users/',
        json={
            'username': 'different_username',
            'email': user.email,
            'password': 'testpass',
        },
    )

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json() == {'detail': 'Email already exists.'}


async def test_update_user(async_client, user, token):
    response = await async_client.put(
        f'/users/{user.id}',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'username': 'update_name',
            'email': 'update@email.com',
            'password': 'update_password',
        },
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'username': 'update_name',
        'email': 'update@email.com',
        'id': user.id,
    }


async def test_update_user_not_enough_permissions(
    async_client, user, token, other_user
):
    response = await async_client.put(
        f'/users/{other_user.id}',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'username': 'update_name',
            'email': 'update@email.com',
            'password': 'update_password',
        },
    )

    assert response.status_code == HTTPStatus.FORBIDDEN
    assert response.json() == {'detail': 'Not enough permissions.'}


async def test_delete_user(async_client, user, token):
    response = await async_client.delete(
        f'/users/{user.id}',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'User Deleted.'}


async def test_delete_user_not_enough_permissions(
    async_client, user, token, other_user
):
    response = await async_client.delete(
        f'/users/{other_user.id}',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.FORBIDDEN
    assert response.json() == {'detail': 'Not enough permissions.'}
