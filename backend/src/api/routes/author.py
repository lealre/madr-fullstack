from http import HTTPStatus
from typing import Any

from fastapi import APIRouter, Depends, HTTPException

from src.api.dependencies import SessionDep, get_current_user
from src.schemas.authors import AuthorList, AuthorPublic, AuthorSchema
from src.schemas.base import Message
from src.schemas.responses import response_model
from src.services import author_service

router = APIRouter()


@router.post(
    '/',
    response_model=AuthorPublic,
    status_code=HTTPStatus.CREATED,
    dependencies=[Depends(get_current_user)],
    responses={
        HTTPStatus.BAD_REQUEST: response_model,
        HTTPStatus.UNAUTHORIZED: response_model,
    },
)
async def add_author(author_in: AuthorSchema, session: SessionDep) -> Any:
    """
    Adds a new author.
    """
    author_db = await author_service.get_author_by_name(
        session=session, author_name=author_in.name
    )

    if author_db:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=f'{author_in.name} already in MADR.',
        )

    new_author = await author_service.add_author(
        session=session, author=author_in
    )

    return new_author


@router.delete(
    '/{author_id}',
    response_model=Message,
    dependencies=[Depends(get_current_user)],
    responses={
        HTTPStatus.NOT_FOUND: response_model,
        HTTPStatus.UNAUTHORIZED: response_model,
    },
)
async def delete_author(
    session: SessionDep,
    author_id: int,
) -> Message:
    """
    Delete an author.
    """
    author_db = await author_service.get_author_by_id(
        session=session, author_id=author_id
    )

    if not author_db:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Author not found in MADR.',
        )

    await session.delete(author_db)
    await session.commit()

    return Message(message='Author deleted from MADR.')


@router.patch(
    '/{author_id}',
    response_model=AuthorPublic,
    dependencies=[Depends(get_current_user)],
    responses={
        HTTPStatus.NOT_FOUND: response_model,
        HTTPStatus.UNAUTHORIZED: response_model,
    },
)
async def update_author(
    author_id: int,
    author_in: AuthorSchema,
    session: SessionDep,
) -> Any:
    """
    Update an author's name.
    """

    author_db = await author_service.get_author_by_id(
        session=session, author_id=author_id
    )

    if not author_db:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Author not found in MADR.',
        )

    author_updated = await author_service.update_author_info(
        session=session, author_to_update=author_db, author_info=author_in
    )

    return author_updated


@router.get(
    '/{author_id}',
    response_model=AuthorPublic,
    responses={
        HTTPStatus.NOT_FOUND: response_model,
        HTTPStatus.UNAUTHORIZED: response_model,
    },
)
async def get_author_by_id(author_id: int, session: SessionDep) -> Any:
    """
    Get an author by their ID.
    """

    author_db = await author_service.get_author_by_id(
        session=session, author_id=author_id
    )

    if not author_db:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Author not found in MADR.',
        )

    return author_db


@router.get('/', response_model=AuthorList)
async def get_authors_with_name_like(
    session: SessionDep,
    name: str | None = None,
    limit: int = 20,
    offset: int = 0,
) -> Any:
    """
    Get authors by filtering by name (like search).
    """

    if not name:
        authors_list = await author_service.get_authors_list(
            session=session, offset=offset, limit=limit
        )

        return {'authors': authors_list, 'total_results': len(authors_list)}

    authors_list = await author_service.get_authors_name_like(
        session=session, offset=offset, limit=limit, author_name=name
    )

    return {'authors': authors_list, 'total_results': len(authors_list)}
