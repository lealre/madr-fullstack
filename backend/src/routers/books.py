from http import HTTPStatus

from fastapi import APIRouter

from src.core.database import T_Session
from src.core.security import CurrentUser
from src.schemas.base import Message
from src.schemas.books import BookList, BookPublic, BookSchema, BookUpdate
from src.services.book_service import (
    delete_book_from_db,
    get_book_by_id_from_db,
    query_paginated_books_from_db,
    register_new_book_in_db,
    update_book_in_db,
)

router = APIRouter(prefix='/book', tags=['book'])


@router.post('/', response_model=BookPublic, status_code=HTTPStatus.CREATED)
async def add_book(book: BookSchema, session: T_Session, user: CurrentUser):
    db_book = await register_new_book_in_db(session=session, book=book)
    return db_book


@router.delete('/{book_id}', response_model=Message)
async def delete_book(book_id: int, session: T_Session, user: CurrentUser):
    await delete_book_from_db(session=session, book_id=book_id)
    return {'message': 'Book deleted from MADR.'}


@router.patch('/{book_id}', response_model=BookPublic)
async def update_book(
    book_id: int, book: BookUpdate, session: T_Session, user: CurrentUser
):
    db_book = await update_book_in_db(
        session=session, book=book, book_id=book_id
    )
    return db_book


@router.get('/{book_id}', response_model=BookPublic)
async def get_book_by_id(book_id: int, session: T_Session):
    db_book = await get_book_by_id_from_db(session=session, book_id=book_id)
    return db_book


@router.get('/', response_model=BookList)
async def get_book_like(
    session: T_Session,
    name: str | None = None,
    year: int | None = None,
    limit: int = 20,
    offset: int = 0,
):
    db_books = await query_paginated_books_from_db(
        session=session, name=name, year=year, limit=limit, offset=offset
    )

    return {'books': db_books}
