from http import HTTPStatus

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.models import Author, Book
from src.schemas.books import BookSchema


async def register_new_book_in_db(session: AsyncSession, book: BookSchema):
    new_book = await session.scalar(
        select(Book).where(book.title == Book.title)
    )

    if new_book:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=f'{new_book.title} already in MADR.',
        )

    author = await session.scalar(
        select(Author).where(Author.id == book.author_id)
    )

    if not author:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=f'Author with ID {book.author_id} not found.',
        )

    new_book = Book(**book.model_dump())

    session.add(new_book)
    await session.commit()
    await session.refresh(new_book)

    return new_book


async def delete_book_from_db(session: AsyncSession, book_id: int):
    db_book = await session.scalar(select(Book).where(Book.id == book_id))

    if not db_book:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='Book not found in MADR.'
        )

    await session.delete(db_book)
    await session.commit()


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
