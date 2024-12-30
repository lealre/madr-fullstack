from http import HTTPStatus

from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from src.models import Author
from tests.conftest import AuthorFactory


async def test_add_author(async_client: AsyncClient, user_token: str) -> None:
    response = await async_client.post(
        '/author',
        headers={'Authorization': f'Bearer {user_token}'},
        json={'name': 'test-name'},
    )

    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {'id': 1, 'name': 'test-name'}


async def test_add_author_already_exists(
    async_client: AsyncClient, user_token: str, author: Author
) -> None:
    response = await async_client.post(
        '/author',
        headers={'Authorization': f'Bearer {user_token}'},
        json={'name': author.name},
    )

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json() == {'detail': f'{author.name} already in MADR.'}


async def test_add_author_not_authenticated(async_client: AsyncClient) -> None:
    response = await async_client.post(
        '/author',
        json={'name': 'test'},
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'Not authenticated'}


async def test_author_name_sanitization_schema(
    async_client: AsyncClient, user_token: str
) -> None:
    expected_name = 'a name to correct'
    response = await async_client.post(
        '/author',
        headers={'Authorization': f'Bearer {user_token}'},
        json={'name': ' A   NAmE to correct     '},
    )

    assert response.json()['name'] == expected_name


async def test_delete_author(
    async_client: AsyncClient, user_token: str, author: Author
) -> None:
    response = await async_client.delete(
        f'/author/{author.id}',
        headers={'Authorization': f'Bearer {user_token}'},
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'Author deleted from MADR.'}


async def test_delete_author_not_found(
    async_client: AsyncClient, user_token: str, author: Author
) -> None:
    response = await async_client.delete(
        '/author/555',
        headers={'Authorization': f'Bearer {user_token}'},
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'Author not found in MADR.'}


async def test_delete_author_not_authenticated(
    async_client: AsyncClient, author: Author
) -> None:
    response = await async_client.delete(f'/author/{author.id}')

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'Not authenticated'}


async def test_delete_authors_in_batch(
    async_client: AsyncClient,
    async_session: AsyncSession,
    user_token: str,
) -> None:
    range_list = 20
    async with async_session.begin():
        async_session.add_all(AuthorFactory.create_batch(range_list))

    response = await async_client.post(
        '/author/delete/batch',
        headers={'Authorization': f'Bearer {user_token}'},
        json={'ids': [n for n in range(1, range_list + 1)]},
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'Authors deleted from MADR.'}

    response = await async_client.get(
        '/author',
        headers={'Authorization': f'Bearer {user_token}'},
    )

    assert response.json()['authors'] == []
    assert response.json()['total_results'] == 0


async def test_delete_authors_in_batch_ids_not_found(
    async_client: AsyncClient,
    async_session: AsyncSession,
    user_token: str,
) -> None:
    range_list = 20
    async with async_session.begin():
        async_session.add_all(AuthorFactory.create_batch(range_list))

    response = await async_client.post(
        '/author/delete/batch',
        headers={'Authorization': f'Bearer {user_token}'},
        json={'ids': [n for n in range(1, range_list + 5)]},
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {
        'detail': 'There are IDs that were not found in the database.'
    }


async def test_delete_authors_in_batch_not_authenticated(
    async_client: AsyncClient, author: Author
) -> None:
    response = await async_client.post(
        '/author/delete/batch',
        json={'ids': [1, 2, 3]},
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'Not authenticated'}


async def test_update_author(
    async_client: AsyncClient, user_token: str, author: Author
) -> None:
    expected_name = 'name updated'
    response = await async_client.patch(
        f'/author/{author.id}',
        headers={'Authorization': f'Bearer {user_token}'},
        json={'name': expected_name},
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'id': author.id, 'name': expected_name}


async def test_update_author_not_found(
    async_client: AsyncClient, user_token: str, author: Author
) -> None:
    response = await async_client.patch(
        '/author/555',
        headers={'Authorization': f'Bearer {user_token}'},
        json={'name': 'update'},
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'Author not found in MADR.'}


async def test_update_author_not_authenticated(
    async_client: AsyncClient, author: Author
) -> None:
    response = await async_client.patch(
        '/author/555',
        json={'name': 'update'},
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'Not authenticated'}


async def test_get_author_by_id(
    async_client: AsyncClient, author: Author
) -> None:
    response = await async_client.get(f'/author/{author.id}')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'id': author.id, 'name': author.name}


async def test_get_author_by_id_not_found(
    async_client: AsyncClient, author: Author
) -> None:
    response = await async_client.get('/author/555')

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'Author not found in MADR.'}


async def test_list_authors_filter_name_should_return_5_authors(
    async_client: AsyncClient, async_session: AsyncSession
) -> None:
    expected_authors = 5
    expected_results = 5
    authors_to_add = AuthorFactory.create_batch(5)
    async with async_session.begin():
        async_session.add_all(authors_to_add)

    response = await async_client.get('/author?name=author')

    assert len(response.json()['authors']) == expected_authors
    assert response.json()['total_results'] == expected_results


async def test_list_authors_filter_name_should_return_empty(
    async_client: AsyncClient, async_session: AsyncSession
) -> None:
    expected_results = 0
    async with async_session.begin():
        async_session.add_all(AuthorFactory.create_batch(5))

    response = await async_client.get('/author?name=different name')

    assert response.json()['authors'] == []
    assert response.json()['total_results'] == expected_results


async def test_list_authors_filter_name_empty_return_all_authors(
    async_client: AsyncClient, async_session: AsyncSession
) -> None:
    expected_authors = 10
    expected_results = 10

    async with async_session.begin():
        async_session.add_all(AuthorFactory.create_batch(10))

    response = await async_client.get('/author')

    assert len(response.json()['authors']) == expected_authors
    assert response.json()['total_results'] == expected_results


async def test_list_authors_pagination_should_return_20_authors(
    async_client: AsyncClient, async_session: AsyncSession
) -> None:
    expected_authors = 20
    expected_results = 25

    async with async_session.begin():
        async_session.add_all(AuthorFactory.create_batch(25))

    response = await async_client.get('/author?name=author')

    assert len(response.json()['authors']) == expected_authors
    assert response.json()['total_results'] == expected_results


async def test_list_authors_pagination_with_name_filter_return_10_authors(
    async_client: AsyncClient, async_session: AsyncSession
) -> None:
    expected_authors = 10
    expected_results = 20

    async with async_session.begin():
        async_session.add_all(AuthorFactory.create_batch(20))
        author_different_name = AuthorFactory.create_batch(20, name='other')
        for n, book in enumerate(author_different_name):
            book.name = f'other_{n}'
        async_session.add_all(author_different_name)

    response = await async_client.get('/author?name=author&limit=10&offset=10')

    assert len(response.json()['authors']) == expected_authors
    assert response.json()['total_results'] == expected_results
