from http import HTTPStatus
from typing import Any

from fastapi import APIRouter, Depends, HTTPException

from src.api.dependencies import CurrentUser, SessionDep, get_current_user
from src.schemas.base import Message
from src.schemas.books import (
    BookList,
    BookPublic,
    BookResponseCreate,
    BookSchema,
    BookUpdate,
    DeteleBooksBulk,
)
from src.services import author_service, book_service

router = APIRouter()


@router.post(
    '',
    response_model=BookResponseCreate,
    status_code=HTTPStatus.CREATED,
    dependencies=[Depends(get_current_user)],
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

    return BookResponseCreate(
        **new_book.to_dict(), author=new_book.author.name
    )


@router.get('/{book_id}', response_model=BookPublic)
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

    return BookPublic(**book_db.to_dict(), author=book_db.author.name)


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

    book_list = [
        BookPublic(**book.to_dict(), author=book.author.name) for book in books
    ]

    return {'books': book_list, 'total_results': total_results}


@router.patch('/{book_id}', response_model=BookPublic)
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

    book_updated = await book_service.update_book_in_db(
        session=session, book_info=book, book_to_update=book_db
    )

    return BookPublic(
        **book_updated.to_dict(), author=book_updated.author.name
    )


@router.delete(
    '/{book_id}',
    response_model=Message,
    dependencies=[Depends(get_current_user)],
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


@router.post(
    '/delete/batch',
    response_model=Message,
    dependencies=[Depends(get_current_user)],
)
async def delete_books_in_batch(
    session: SessionDep,
    books_ids: DeteleBooksBulk,
) -> Message:
    """
    Delete books in batch by their list of ids.
    """
    book_ids_db = await book_service.get_books_ids_list(
        session=session, book_ids=books_ids.ids
    )

    book_ids_in = list(set(books_ids.ids))
    if not all(id in book_ids_db for id in book_ids_in):
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='There are IDs that were not found in the database.',
        )

    await book_service.delete_books_batch(
        session=session, book_ids=book_ids_in
    )

    return Message(message='Books deleted from MADR.')
