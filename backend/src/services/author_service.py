from http import HTTPStatus

from fastapi import HTTPException
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.models import Author
from src.schemas.authors import AuthorSchema


async def get_author_by_id(
    session: AsyncSession, author_id: int
) -> Author | None:
    """
    Retrieve an author from the database by their ID.

    :param session: The database session used to perform the query.
    :param author_id: The ID of the author to retrieve.
    :return: The Author object if found, otherwise None.
    """

    author_db = await session.scalar(
        select(Author).where(Author.id == author_id)
    )

    return author_db


async def get_author_by_name(
    session: AsyncSession, author_name: str
) -> Author | None:
    """
    Retrieve an author from the database by their name.

    :param session: The database session used to perform the query.
    :param author_name: The name of the author to retrieve.
    :return: The Author object if found, otherwise None.
    """

    author_db = await session.scalar(
        select(Author).where(Author.name == author_name)
    )

    return author_db


async def add_author(session: AsyncSession, author: AuthorSchema) -> Author:
    """
    Add a new author to the database.

    :param session: The database session used to perform the operation.
    :param author: The AuthorSchema object containing the details of
    the author to add.
    :return: The newly created Author object.
    """

    new_author = Author(**author.model_dump())

    session.add(new_author)
    await session.commit()
    await session.refresh(new_author)

    return new_author


async def delete_author_from_db(session: AsyncSession, author_id: int):
    author_db = await session.scalar(
        select(Author).where(Author.id == author_id)
    )

    if not author_db:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Author not found in MADR.',
        )

    await session.delete(author_db)
    await session.commit()


async def update_author_in_db(
    session: AsyncSession, author_id: int, author: AuthorSchema
):
    author_db = await session.scalar(
        select(Author).where(Author.id == author_id)
    )

    if not author_db:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Author not found in MADR.',
        )

    author_db.name = author.name

    session.add(author_db)
    await session.commit()
    await session.refresh(author_db)

    return author_db


async def get_author_by_id_from_db(session: AsyncSession, author_id: int):
    author_db = await session.scalar(
        select(Author).where(Author.id == author_id)
    )

    if not author_db:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Author not found in MADR.',
        )

    return author_db


async def query_paginated_authors_from_db(
    session: AsyncSession,
    name: str | None,
    limit: int = 20,
    offset: int = 0,
):
    if not name:
        total_results = await session.scalar(select(func.count(Author.id)))
        authors_list = await session.scalars(
            select(Author).limit(limit).offset(offset)
        )
        return authors_list, total_results

    query = select(Author).filter(Author.name.contains(name))

    total_results = await session.scalar(
        select(func.count()).select_from(query.subquery())
    )

    authors_list = await session.scalars(query.limit(limit).offset(offset))

    return authors_list, total_results
