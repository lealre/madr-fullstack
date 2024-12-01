from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException

from src.api.dependencies import CurrentUser, SessionDep, get_current_user
from src.schemas.base import Message
from src.schemas.books import BookList, BookPublic, BookSchema, BookUpdate
from src.schemas.responses import response_model
from src.services import author_service, book_service
from src.services.book_service import (
    get_book_by_id_from_db,
    query_paginated_books_from_db,
    update_book_in_db,
)

router = APIRouter()


@router.post(
    '/',
    response_model=BookPublic,
    status_code=HTTPStatus.CREATED,
    dependencies=[Depends(get_current_user)],
    responses={
        HTTPStatus.BAD_REQUEST: response_model,
        HTTPStatus.UNAUTHORIZED: response_model,
    },
)
async def add_book(session: SessionDep, book_in: BookSchema):
    book_db = await book_service.get_book_by_title(
        session=session, book_title=book_in.title
    )

    if book_db:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=f'{book_in.title} already in MADR.',
        )

    author_db = await author_service.get_author_by_id(
        session=session, author_id=book_in.author_id
    )

    if not author_db:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=f'Author with ID {book_in.author_id} not found.',
        )

    new_book = await book_service.add_book(session=session, book=book_in)

    return new_book


@router.delete(
    '/{book_id}',
    response_model=Message,
    dependencies=[Depends(get_current_user)],
    responses={
        HTTPStatus.NOT_FOUND: response_model,
        HTTPStatus.UNAUTHORIZED: response_model,
    },
)
async def delete_book(session: SessionDep, book_id: int):
    book_db = await book_service.get_book_by_id(
        session=session, book_id=book_id
    )

    if not book_db:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='Book not found in MADR.'
        )

    await session.delete(book_db)
    await session.commit()

    return {'message': 'Book deleted from MADR.'}


@router.patch(
    '/{book_id}',
    response_model=BookPublic,
    responses={
        HTTPStatus.NOT_FOUND: response_model,
        HTTPStatus.UNAUTHORIZED: response_model,
    },
)
async def update_book(
    book_id: int, book: BookUpdate, session: SessionDep, user: CurrentUser
):
    db_book = await update_book_in_db(
        session=session, book=book, book_id=book_id
    )
    return db_book


@router.get(
    '/{book_id}',
    response_model=BookPublic,
    responses={
        HTTPStatus.NOT_FOUND: response_model,
        HTTPStatus.UNAUTHORIZED: response_model,
    },
)
async def get_book_by_id(book_id: int, session: SessionDep):
    db_book = await get_book_by_id_from_db(session=session, book_id=book_id)
    return db_book


@router.get('/', response_model=BookList)
async def get_book_like(
    session: SessionDep,
    name: str | None = None,
    year: int | None = None,
    limit: int = 20,
    offset: int = 0,
):
    db_books = await query_paginated_books_from_db(
        session=session, name=name, year=year, limit=limit, offset=offset
    )

    return {'books': db_books}
