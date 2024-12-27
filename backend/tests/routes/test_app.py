from http import HTTPStatus

from httpx import AsyncClient


async def test_read_home_root(async_client: AsyncClient) -> None:
    response = await async_client.get('/')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'Root Endpoint!'}
