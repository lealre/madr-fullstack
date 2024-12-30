from http import HTTPStatus

import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from src.models import Author, Book
from tests.conftest import BookFactory


async def test_add_book(
    async_client: AsyncClient, user_token: str, author: Author
) -> None:
    response = await async_client.post(
        '/book',
        headers={'Authorization': f'Bearer {user_token}'},
        json={'year': 2024, 'title': 'book title', 'author_id': 1},
    )

    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        'id': 1,
        'year': 2024,
        'title': 'book title',
        'author_id': 1,
    }


async def test_add_book_already_exists(
    async_client: AsyncClient, user_token: str, book: Book
) -> None:
    response = await async_client.post(
        '/book',
        headers={'Authorization': f'Bearer {user_token}'},
        json={'year': 2024, 'title': book.title, 'author_id': 1},
    )

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json() == {'detail': f'{book.title} already in MADR.'}


async def test_add_book_author_id_not_found(
    async_client: AsyncClient, user_token: str
) -> None:
    book = BookFactory()
    response = await async_client.post(
        '/book',
        headers={'Authorization': f'Bearer {user_token}'},
        json={
            'year': book.year,
            'title': book.title,
            'author_id': book.author_id,
        },
    )

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json() == {
        'detail': f'Author with ID {book.author_id} not found.'
    }


async def test_add_book_not_authenticated(async_client: AsyncClient) -> None:
    response = await async_client.post(
        '/book',
        json={'year': 2024, 'title': 'book title', 'author_id': 1},
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'Not authenticated'}


async def test_book_title_sanitization_schema(
    async_client: AsyncClient, user_token: str, author: Author
) -> None:
    expected_title = 'a title to correct'
    response = await async_client.post(
        '/book',
        headers={'Authorization': f'Bearer {user_token}'},
        json={
            'year': 2024,
            'title': ' A   TitLE  to correct     ',
            'author_id': 1,
        },
    )

    assert response.json()['title'] == expected_title


async def test_delete_book(
    async_client: AsyncClient, user_token: str, book: Book
) -> None:
    response = await async_client.delete(
        f'/book/{book.id}', headers={'Authorization': f'Bearer {user_token}'}
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'Book deleted from MADR.'}


async def test_delete_book_not_found(
    async_client: AsyncClient, user_token: str, book: Book
) -> None:
    response = await async_client.delete(
        '/book/10', headers={'Authorization': f'Bearer {user_token}'}
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'Book not found in MADR.'}


async def test_delete_book_not_authenticated(
    async_client: AsyncClient, book: Book
) -> None:
    response = await async_client.delete(f'/book/{book.id}')

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'Not authenticated'}


async def test_delete_books_in_batch(
    async_client: AsyncClient,
    async_session: AsyncSession,
    user_token: str,
    author: Author,
) -> None:
    range_list = 20
    async with async_session.begin():
        async_session.add_all(BookFactory.create_batch(range_list))

    response = await async_client.post(
        '/book/delete/batch',
        headers={'Authorization': f'Bearer {user_token}'},
        json={'ids': [n for n in range(1, range_list + 1)]},
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'Books deleted from MADR.'}

    response = await async_client.get(
        '/book',
        headers={'Authorization': f'Bearer {user_token}'},
    )

    assert response.json()['books'] == []
    assert response.json()['total_results'] == 0


async def test_delete_books_in_batch_ids_not_found(
    async_client: AsyncClient,
    async_session: AsyncSession,
    user_token: str,
    author: Author,
) -> None:
    range_list = 20
    async with async_session.begin():
        async_session.add_all(BookFactory.create_batch(range_list))

    response = await async_client.post(
        '/book/delete/batch',
        headers={'Authorization': f'Bearer {user_token}'},
        json={'ids': [n for n in range(1, range_list + 5)]},
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {
        'detail': 'There are IDs that were not found in the database.'
    }


async def test_delete_books_in_batch_not_authenticated(
    async_client: AsyncClient, author: Author
) -> None:
    response = await async_client.post(
        '/book/delete/batch',
        json={'ids': [1, 2, 3]},
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'Not authenticated'}


async def test_patch_book(
    async_client: AsyncClient,
    async_session: AsyncSession,
    user_token: str,
    author: Author,
) -> None:
    input_year = 2000
    book = BookFactory(year=input_year)

    async with async_session.begin():
        async_session.add(book)

    year_expected = 2024

    assert book.year == input_year

    response = await async_client.patch(
        f'/book/{book.id}',
        headers={'Authorization': f'Bearer {user_token}'},
        json={'year': year_expected},
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'id': book.id,
        'year': year_expected,
        'title': book.title,
        'author_id': book.author_id,
    }


async def test_patch_book_not_found(
    async_client: AsyncClient, user_token: str, book: Book
) -> None:
    response = await async_client.patch(
        '/book/10',
        headers={'Authorization': f'Bearer {user_token}'},
        json={'year': 2000},
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'Book not found in MADR.'}


async def test_patch_book_not_authenticated(
    async_client: AsyncClient, book: Book
) -> None:
    response = await async_client.patch('/book/10', json={'year': 2000})

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'Not authenticated'}


async def test_get_book_by_id(async_client: AsyncClient, book: Book) -> None:
    response = await async_client.get(f'/book/{book.id}')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'id': book.id,
        'year': book.year,
        'title': book.title,
        'author_id': book.author_id,
    }


async def test_get_book_by_id_not_found(
    async_client: AsyncClient, book: Book
) -> None:
    response = await async_client.get('/book/10')

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'Book not found in MADR.'}


async def test_list_books_empty(async_client: AsyncClient) -> None:
    expected_results = 0
    response = await async_client.get('/book')

    assert response.json()['books'] == []
    assert response.json()['total_results'] == expected_results


async def test_list_books_filter_title_should_return_5_books(
    async_client: AsyncClient, async_session: AsyncSession, author: Author
) -> None:
    expected_books = 5
    expected_results = 5
    async with async_session.begin():
        async_session.add_all(BookFactory.create_batch(5))
        books_with_title = BookFactory.create_batch(5, title='title')
        for n, book in enumerate(books_with_title):
            book.title = f'title_{n}'
        async_session.add_all(books_with_title)

    response = await async_client.get('/book?title=title')

    assert len(response.json()['books']) == expected_books
    assert response.json()['total_results'] == expected_results


async def test_list_books_filter_title_should_return_empty(
    async_client: AsyncClient, async_session: AsyncSession, author: Author
) -> None:
    expected_results = 0
    async with async_session.begin():
        async_session.add_all(BookFactory.create_batch(5))

    response = await async_client.get('/book?title=title')

    assert response.json()['books'] == []
    assert response.json()['total_results'] == expected_results


async def test_list_books_filter_year_should_return_5_books(
    async_client: AsyncClient, async_session: AsyncSession, author: Author
) -> None:
    expected_books = 5
    expected_results = 5
    async with async_session.begin():
        async_session.add_all(BookFactory.create_batch(5, year=2000))
        async_session.add_all(BookFactory.create_batch(5, year=2024))

    response = await async_client.get('/book?year=2000')

    assert len(response.json()['books']) == expected_books
    assert response.json()['total_results'] == expected_results


async def test_list_books_filter_year_should_return_empty(
    async_client: AsyncClient, async_session: AsyncSession, author: Author
) -> None:
    expected_results = 0
    async with async_session.begin():
        async_session.add_all(BookFactory.create_batch(5, year=2000))

    response = await async_client.get('/book?year=2024')

    assert response.json()['books'] == []
    assert response.json()['total_results'] == expected_results


async def test_list_books_filter_combined_should_return_5_books(
    async_client: AsyncClient, async_session: AsyncSession, author: Author
) -> None:
    expected_books = 5
    expected_results = 5
    books = BookFactory.create_batch(7, year=2000)
    books[-1].title = 'title'
    books[0].year = 2024
    async with async_session.begin():
        async_session.add_all(books)

    response = await async_client.get('/book?year=2000&title=oo')

    assert len(response.json()['books']) == expected_books
    assert response.json()['total_results'] == expected_results


@pytest.mark.parametrize(
    ('limit', 'offset'), [(10, 0), (10, 10), (5, 0), (5, 5)]
)
async def test_list_books_pagination_with_filter(
    async_client: AsyncClient,
    async_session: AsyncSession,
    author: Author,
    limit: int,
    offset: int,
) -> None:
    expected_books = limit
    expected_results = 25
    async with async_session.begin():
        async_session.add_all(BookFactory.create_batch(25, year=2000))

    response = await async_client.get(
        f'/book?year=2000&limit={limit}&offset={offset}'
    )

    assert len(response.json()['books']) == expected_books
    assert response.json()['total_results'] == expected_results
