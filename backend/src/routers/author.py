from http import HTTPStatus

from fastapi import APIRouter

from src.core.database import T_Session
from src.core.security import CurrentUser
from src.schemas.authors import AuthorList, AuthorPublic, AuthorSchema
from src.schemas.base import Message
from src.services.author_service import (
    delete_author_from_db,
    get_author_by_id_from_db,
    query_paginated_authors_from_db,
    register_new_author_in_db,
    update_author_in_db,
)

router = APIRouter(prefix='/author', tags=['author'])


@router.post('/', response_model=AuthorPublic, status_code=HTTPStatus.CREATED)
async def add_author(
    author: AuthorSchema, session: T_Session, user: CurrentUser
):
    author_db = await register_new_author_in_db(session=session, author=author)
    return author_db


@router.delete('/{author_id}', response_model=Message)
async def delete_author(author_id: int, session: T_Session, user: CurrentUser):
    await delete_author_from_db(session=session, author_id=author_id)
    return {'message': 'Author deleted from MADR.'}


@router.patch('/{author_id}', response_model=AuthorPublic)
async def update_author(
    author_id: int, author: AuthorSchema, session: T_Session, user: CurrentUser
):
    author_db = await update_author_in_db(
        session=session, author_id=author_id, author=author
    )
    return author_db


@router.get('/{author_id}', response_model=AuthorPublic)
async def get_author_by_id(author_id: int, session: T_Session):
    author_db = await get_author_by_id_from_db(
        session=session, author_id=author_id
    )
    return author_db


@router.get('/', response_model=AuthorList)
async def get_author_with_name_like(
    session: T_Session,
    name: str | None = None,
    limit: int = 20,
    offset: int = 0,
):
    authors_list, total_results = await query_paginated_authors_from_db(
        session=session, name=name, limit=limit, offset=offset
    )

    return {'authors': authors_list, 'total_results': total_results}
