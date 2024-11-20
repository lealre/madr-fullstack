from http import HTTPStatus


async def test_read_home_root(async_client):
    response = await async_client.get('/')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'Root Endpoint!'}
