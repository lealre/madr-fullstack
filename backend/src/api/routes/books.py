from http import HTTPStatus
from typing import Any

from fastapi import APIRouter, Depends, HTTPException

from src.api.dependencies import CurrentUser, SessionDep, get_current_user
from src.schemas.base import Message
from src.schemas.books import BookList, BookPublic, BookSchema, BookUpdate
from src.schemas.responses import response_model
from src.services import author_service, book_service

router = APIRouter()


@router.post(
    '',
    response_model=BookPublic,
    status_code=HTTPStatus.CREATED,
    dependencies=[Depends(get_current_user)],
    responses={
        HTTPStatus.BAD_REQUEST: response_model,
        HTTPStatus.UNAUTHORIZED: response_model,
    },
)
async def add_book(session: SessionDep, book_in: BookSchema) -> Any:
    """
    Add a new book.

    It is necessary to have the author registered beforehand.
    """
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


@router.get(
    '/{book_id}',
    response_model=BookPublic,
    responses={
        HTTPStatus.NOT_FOUND: response_model,
        HTTPStatus.UNAUTHORIZED: response_model,
    },
)
async def get_book_by_id(book_id: int, session: SessionDep) -> Any:
    """
    Get a book by ID.
    """
    book_db = await book_service.get_book_by_id(
        session=session, book_id=book_id
    )

    if not book_db:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='Book not found in MADR.'
        )

    return book_db


@router.get('', response_model=BookList)
async def get_books_like(
    session: SessionDep,
    title: str | None = None,
    year: int | None = None,
    limit: int = 20,
    offset: int = 0,
) -> Any:
    """
    Get a list of books filtered by title (like search) and/or year.
    """
    books, total_results = await book_service.get_books_list(
        session=session,
        book_title=title,
        book_year=year,
        limit=limit,
        offset=offset,
    )

    return {'books': books, 'total_results': total_results}


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
) -> Any:
    """
    Update the year of a book by its ID.
    """
    book_db = await book_service.get_book_by_id(
        session=session, book_id=book_id
    )

    if not book_db:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='Book not found in MADR.'
        )

    db_book = await book_service.update_book_in_db(
        session=session, book_info=book, book_to_update=book_db
    )

    return db_book


@router.delete(
    '/{book_id}',
    response_model=Message,
    dependencies=[Depends(get_current_user)],
    responses={
        HTTPStatus.NOT_FOUND: response_model,
        HTTPStatus.UNAUTHORIZED: response_model,
    },
)
async def delete_book(session: SessionDep, book_id: int) -> Message:
    """
    Delete a book.
    """
    book_db = await book_service.get_book_by_id(
        session=session, book_id=book_id
    )

    if not book_db:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='Book not found in MADR.'
        )

    await book_service.delete_book(session=session, book_to_delete=book_db)

    return Message(message='Book deleted from MADR.')
