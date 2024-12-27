from sqlalchemy import and_, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.models import Book
from src.schemas.books import BookSchema, BookUpdate


async def get_book_by_id(session: AsyncSession, book_id: int) -> Book | None:
    """
    Retrieve a book by its ID from the database.

    :param session: The asynchronous database session used for the query.
    :param book_id: The ID of the book to retrieve.
    :return: The Book object if found, or None if no book with the specified
    ID exists.
    """

    book_db = await session.scalar(select(Book).where(Book.id == book_id))

    return book_db


async def get_book_by_title(
    session: AsyncSession, book_title: str
) -> Book | None:
    """
    Retrieve a book by its title from the database.

    :param session: The asynchronous database session used for the query.
    :param book_title: The title of the book to retrieve.
    :return: The Book object if found, or None if no book with the specified
    title exists.
    """

    book_db = await session.scalar(
        select(Book).where(Book.title == book_title)
    )

    return book_db


async def add_book(session: AsyncSession, book: BookSchema) -> Book:
    """
    Add a new book to the database.

    :param session: The asynchronous database session used for the operation.
    :param book: The schema object containing the details of the book to be
    added.
    :return: The newly created Book object after it has been committed and
    refreshed.
    """

    new_book = Book(**book.model_dump())

    session.add(new_book)
    await session.commit()
    await session.refresh(new_book)

    return new_book


async def update_book_in_db(
    session: AsyncSession, book_info: BookUpdate, book_to_update: Book
) -> Book:
    """
    Update an existing book record in the database.

    :param session: The asynchronous database session used for the operation.
    :param book_info: The schema object containing the updated details for
    the book.
    :param book_to_update: The existing Book object to be updated.
    :return: The updated Book object after the changes have been committed
    and refreshed.
    """

    for key, value in book_info.model_dump(exclude_unset=True).items():
        setattr(book_to_update, key, value)

    session.add(book_to_update)
    await session.commit()
    await session.refresh(book_to_update)

    return book_to_update


async def get_books_list(
    session: AsyncSession,
    limit: int,
    offset: int,
    book_title: str | None = None,
    book_year: int | None = None,
) -> list[Book]:
    """
    Retrieve a paginated list of books from the database, optionally filtered
    by title and/or year.

    :param session: The asynchronous database session used for the query.
    :param limit: The maximum number of books to retrieve.
    :param offset: The number of books to skip before starting to retrieve
    results.
    :param book_title: An optional substring to filter books by their title
    (default is None).
    :param book_year: An optional year to filter books by their publication
    year (default is None).
    :return: A list of Book objects that match the filters, or None if no
    filters are provided or no books match.
    """

    if book_title and book_year:
        query = select(Book).where(
            and_(Book.title.contains(book_title), Book.year == book_year)
        )

    elif book_title:
        query = select(Book).where(Book.title.contains(book_title))

    elif book_year:
        query = select(Book).where(Book.year == book_year)

    else:
        return []

    query = query.limit(limit).offset(offset)
    books_db = await session.scalars(query)

    return list(books_db.all())
