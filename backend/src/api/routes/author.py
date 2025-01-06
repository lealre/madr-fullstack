from http import HTTPStatus
from typing import Any

from fastapi import APIRouter, Depends, HTTPException

from src.api.dependencies import SessionDep, get_current_user
from src.schemas.authors import (
    AuthorList,
    AuthorPublic,
    AuthorSchema,
    DeteleAuthosBulk,
)
from src.schemas.base import Message
from src.schemas.responses import response_model
from src.services import author_service

router = APIRouter()


@router.post(
    '',
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


@router.get('', response_model=AuthorList)
async def get_authors_with_name_like(
    session: SessionDep,
    name: str | None = None,
    limit: int | None = None,
    offset: int = 0,
) -> Any:
    """
    Get authors by filtering by name (like search).
    """
    (
        authors_list,
        total_rows_db,
    ) = await author_service.get_filtered_authors_list(
        session=session, offset=offset, limit=limit, author_name=name
    )

    return {'authors': authors_list, 'total_results': total_rows_db}


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

    await author_service.delete_author(
        session=session, author_to_delete=author_db
    )

    return Message(message='Author deleted from MADR.')


@router.post(
    '/delete/batch',
    response_model=Message,
    dependencies=[Depends(get_current_user)],
    responses={
        HTTPStatus.NOT_FOUND: response_model,
        HTTPStatus.UNAUTHORIZED: response_model,
    },
)
async def delete_author_batch(
    session: SessionDep,
    authors_ids: DeteleAuthosBulk,
) -> Message:
    """
    Delete authors in batch by their list of ids.
    """
    auhtor_ids_db = await author_service.get_authors_ids_list(
        session=session, author_ids=authors_ids.ids
    )

    authors_ids_in = list(set(authors_ids.ids))
    if not all(id in auhtor_ids_db for id in authors_ids_in):
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='There are IDs that were not found in the database.',
        )

    await author_service.delete_authors_batch(
        session=session, author_ids=authors_ids_in
    )

    return Message(message='Authors deleted from MADR.')
