from http import HTTPStatus

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.models import Book
from src.schemas.books import BookSchema


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

    book_db = await session.scalar(select(Book).where(Book.title == book_title))

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
    session: AsyncSession, book_id: int, book: BookSchema
):
    db_book = await session.scalar(select(Book).where(Book.id == book_id))

    if not db_book:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='Book not found in MADR.'
        )

    db_book.year = book.year

    session.add(db_book)
    await session.commit()
    await session.refresh(db_book)

    return db_book


async def get_book_by_id_from_db(session: AsyncSession, book_id: int):
    db_book = await session.scalar(select(Book).where(Book.id == book_id))

    if not db_book:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='Book not found in MADR.'
        )

    return db_book


async def query_paginated_books_from_db(
    session: AsyncSession,
    name: str | None = None,
    year: int | None = None,
    limit: int = 20,
    offset: int = 0,
):
    query = select(Book)

    if name:
        query = query.filter(Book.title.contains(name))

    if year:
        query = query.filter(Book.year == year)

    db_books = await session.scalars(query.limit(limit).offset(offset))

    return db_books
