from http import HTTPStatus

from fastapi import APIRouter

from src.api.dependencies import CurrentUser, SessionDep
from src.schemas.authors import AuthorList, AuthorPublic, AuthorSchema
from src.schemas.base import Message
from src.schemas.responses import response_model
from src.services.author_service import (
    delete_author_from_db,
    get_author_by_id_from_db,
    query_paginated_authors_from_db,
    register_new_author_in_db,
    update_author_in_db,
)

router = APIRouter()


@router.post(
    '/',
    response_model=AuthorPublic,
    status_code=HTTPStatus.CREATED,
    responses={
        HTTPStatus.BAD_REQUEST: response_model,
        HTTPStatus.UNAUTHORIZED: response_model,
    },
)
async def add_author(
    author: AuthorSchema, session: SessionDep, user: CurrentUser
):
    author_db = await register_new_author_in_db(session=session, author=author)
    return author_db


@router.delete(
    '/{author_id}',
    response_model=Message,
    responses={
        HTTPStatus.NOT_FOUND: response_model,
        HTTPStatus.UNAUTHORIZED: response_model,
    },
)
async def delete_author(
    author_id: int, session: SessionDep, user: CurrentUser
):
    await delete_author_from_db(session=session, author_id=author_id)
    return {'message': 'Author deleted from MADR.'}


@router.patch(
    '/{author_id}',
    response_model=AuthorPublic,
    responses={
        HTTPStatus.NOT_FOUND: response_model,
        HTTPStatus.UNAUTHORIZED: response_model,
    },
)
async def update_author(
    author_id: int,
    author: AuthorSchema,
    session: SessionDep,
    user: CurrentUser,
):
    author_db = await update_author_in_db(
        session=session, author_id=author_id, author=author
    )
    return author_db


@router.get(
    '/{author_id}',
    response_model=AuthorPublic,
    responses={
        HTTPStatus.NOT_FOUND: response_model,
        HTTPStatus.UNAUTHORIZED: response_model,
    },
)
async def get_author_by_id(author_id: int, session: SessionDep):
    author_db = await get_author_by_id_from_db(
        session=session, author_id=author_id
    )
    return author_db


@router.get('/', response_model=AuthorList)
async def get_author_with_name_like(
    session: SessionDep,
    name: str | None = None,
    limit: int = 20,
    offset: int = 0,
):
    authors_list, total_results = await query_paginated_authors_from_db(
        session=session, name=name, limit=limit, offset=offset
    )

    return {'authors': authors_list, 'total_results': total_results}
