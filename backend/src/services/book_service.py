from sqlalchemy import and_, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.models import Book
from src.schemas.books import BookSchema, BookUpdate


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

    async with session.begin():
        session.add(new_book)

    return new_book


async def get_book_by_id(session: AsyncSession, book_id: int) -> Book | None:
    """
    Retrieve a book by its ID from the database.

    :param session: The asynchronous database session used for the query.
    :param book_id: The ID of the book to retrieve.
    :return: The Book object if found, or None if no book with the specified
        ID exists.
    """
    async with session:
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
    async with session:
        book_db = await session.scalar(
            select(Book).where(Book.title == book_title)
        )

    return book_db


async def get_books_list(
    session: AsyncSession,
    limit: int,
    offset: int,
    book_title: str | None = None,
    book_year: int | None = None,
) -> tuple[list[Book], int]:
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
    :return: A tuple containing a list of Book objects that match the filters
        and the total count of books, or None if no filters are provided or no
        books match.
    """
    async with session:
        query_rows = select(func.count(Book.id))
        total_count = await session.scalar(query_rows)

    if book_title and book_year:
        query = select(Book).where(
            and_(Book.title.contains(book_title), Book.year == book_year)
        )
    elif book_title:
        query = select(Book).where(Book.title.contains(book_title))
    elif book_year:
        query = select(Book).where(Book.year == book_year)
    else:
        query = select(Book)

    async with session:
        books_db = await session.scalars(query.limit(limit).offset(offset))
        authors_list = books_db.all()

    return list(authors_list), total_count or 0


async def update_book_in_db(
    session: AsyncSession, book_info: BookUpdate, book_to_update: Book
) -> Book:
    """
    Update an existing book record in the database.

    :param session: The asynchronous database session used for the operation.
    :param book_info: The schema object containing the updated details for the
        book.
    :param book_to_update: The existing Book object to be updated.
    :return: The updated Book object after the changes have been committed and
        refreshed.
    """
    for key, value in book_info.model_dump(exclude_unset=True).items():
        setattr(book_to_update, key, value)

    async with session.begin():
        session.add(book_to_update)

    return book_to_update


async def delete_book(session: AsyncSession, book_to_delete: Book) -> bool:
    """
    Delete a book from the database and confirm deletion.

    :param session: The asynchronous database session used for the operation.
    :param book_to_delete: The Book object to be deleted from the database.
    :return: True if the book was successfully deleted, False otherwise.
    """
    async with session.begin():
        book_deleted = await session.delete(book_to_delete)

    return book_deleted is None
