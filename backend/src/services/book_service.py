from sqlalchemy import and_, delete, func, select
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
    by title and/or year, and return the total count of books in the database.

    :param session: The asynchronous database session used for the query.
    :param limit: The maximum number of books to retrieve.
    :param offset: The number of books to skip before starting to retrieve
        results.
    :param book_title: An optional substring to filter books by their title.
        If provided, only books with titles containing this substring will
        be returned.
    :param book_year: An optional year to filter books by their publication
        year. If provided, only books published in this year will be returned.
    :return: A tuple containing:
        - A list of `Book` objects that match the provided filters (if any).
        - The total count of books in the database
        (not filtered by title or year).
    """
    async with session:
        query = select(Book)
        count_query = select(func.count(Book.id))

        has_filter = True

        if book_title and book_year:
            filter_condition = and_(
                Book.title.contains(book_title), Book.year == book_year
            )
        elif book_title:
            filter_condition = Book.title.contains(book_title)
        elif book_year:
            filter_condition = Book.year == book_year
        else:
            has_filter = False

        if has_filter:
            query = query.where(filter_condition)
            count_query = count_query.filter(filter_condition)

        total_count = await session.scalar(count_query)
        authors_db = await session.scalars(query.limit(limit).offset(offset))
        authors_list = authors_db.all()

    return list(authors_list), total_count or 0


async def get_books_ids_list(
    session: AsyncSession, book_ids: list[int]
) -> list[int]:
    """
    Retrieve a list of book IDs that match the given list of IDs.

    :param session: The asynchronous database session used for the query.
    :param book_ids: A list of book IDs to search for in the database.
    :return: A list of book IDs that exist in the database.
    """
    async with session:
        authors_list = await session.scalars(
            select(Book.id).filter(Book.id.in_(book_ids))
        )

    return list(authors_list.all())


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


async def delete_book(session: AsyncSession, book_to_delete: Book) -> None:
    """
    Delete a book from the database and confirm deletion.

    :param session: The asynchronous database session used for the operation.
    :param book_to_delete: The Book object to be deleted from the database.
    :return: True if the book was successfully deleted, False otherwise.
    """
    async with session.begin():
        await session.delete(book_to_delete)


async def delete_books_batch(
    session: AsyncSession, book_ids: list[int]
) -> None:
    """
    Delete books in bulk based on a list of their IDs.

    This function removes all books whose IDs match the provided list from
    the database.

    :param session: The asynchronous database session used for the operation.
    :param book_ids: A list of book IDs to delete from the database.
    :return: None
    """
    async with session.begin():
        await session.execute(delete(Book).where(Book.id.in_(book_ids)))
