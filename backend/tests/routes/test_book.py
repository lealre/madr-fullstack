from http import HTTPStatus

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
        f'/book/{10}', headers={'Authorization': f'Bearer {user_token}'}
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'Book not found in MADR.'}


async def test_delete_book_not_authenticated(
    async_client: AsyncClient, book: Book
) -> None:
    response = await async_client.delete(f'/book/{book.id}')

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

    async_session.add(book)
    await async_session.commit()

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
        f'/book/{10}',
        headers={'Authorization': f'Bearer {user_token}'},
        json={'year': 2000},
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'Book not found in MADR.'}


async def test_patch_book_not_authenticated(
    async_client: AsyncClient, book: Book
) -> None:
    response = await async_client.patch(f'/book/{10}', json={'year': 2000})

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
    response = await async_client.get(f'/book/{10}')

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'Book not found in MADR.'}


async def test_list_books_empty(async_client: AsyncClient) -> None:
    response = await async_client.get('/book')

    assert response.json()['books'] == []


async def test_list_books_filter_name_should_return_5_books(
    async_client: AsyncClient, async_session: AsyncSession, author: Author
) -> None:
    expected_books = 5
    async_session.add_all(BookFactory.create_batch(5))
    books_with_title = BookFactory.create_batch(5, title='title')
    for n, book in enumerate(books_with_title):
        book.title = f'title_{n}'
    async_session.add_all(books_with_title)
    await async_session.commit()

    response = await async_client.get('/book/?title=title')

    assert response.json()['total_results'] == expected_books


async def test_list_books_filter_name_should_return_empty(
    async_client: AsyncClient, async_session: AsyncSession, author: Author
) -> None:
    async_session.add_all(BookFactory.create_batch(5))
    await async_session.commit()

    response = await async_client.get('/book/?title=title')

    assert response.json()['books'] == []


async def test_list_books_filter_year_should_return_5_books(
    async_client: AsyncClient, async_session: AsyncSession, author: Author
) -> None:
    expected_books = 5
    async_session.add_all(BookFactory.create_batch(5, year=2000))
    async_session.add_all(BookFactory.create_batch(5, year=2024))
    await async_session.commit()

    response = await async_client.get('/book/?year=2000')

    assert len(response.json()['books']) == expected_books


async def test_list_books_filter_year_should_return_empty(
    async_client: AsyncClient, async_session: AsyncSession, author: Author
) -> None:
    async_session.add_all(BookFactory.create_batch(5, year=2000))
    await async_session.commit()

    response = await async_client.get('/book/?year=2024')

    assert response.json()['books'] == []


async def test_list_books_filter_combined_should_return_5_books(
    async_client: AsyncClient, async_session: AsyncSession, author: Author
) -> None:
    expected_books = 5
    books = BookFactory.create_batch(7, year=2000)
    books[-1].title = 'title'
    books[0].year = 2024
    async_session.add_all(books)
    await async_session.commit()

    response = await async_client.get('/book?year=2000&title=oo')

    assert len(response.json()['books']) == expected_books


async def test_list_books_pagination_should_return_20_books(
    async_client: AsyncClient, async_session: AsyncSession, author: Author
) -> None:
    expected_books = 20
    async_session.add_all(BookFactory.create_batch(25, year=2000))
    await async_session.commit()

    response = await async_client.get('/book?year=2000')

    assert len(response.json()['books']) == expected_books
