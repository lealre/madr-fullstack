from sqlalchemy import select
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


async def get_authors_list(
    session: AsyncSession, limit: int, offset: int
) -> list[Author]:
    """
    Retrieve a paginated list of authors from the database.

    :param session: The asynchronous database session used for the query.
    :param limit: The maximum number of authors to retrieve.
    :param offset: The number of authors to skip before starting
    to retrieve results.
    :return: A list of author objects.
    """

    authors_db = await session.scalars(
        select(Author).offset(offset).limit(limit)
    )
    authors_list = list(authors_db.all())

    return authors_list


async def get_authors_name_like(
    session: AsyncSession,
    author_name: str,
    limit: int = 20,
    offset: int = 0,
) -> list[Author]:
    """
    Retrieve a paginated list of authors whose names contain the
    given substring.

    :param session: The asynchronous database session used for the query.
    :param author_name: The substring to search for in the author names.
    :param limit: The maximum number of authors to retrieve (default is 20).
    :param offset: The number of authors to skip before starting to
    retrieve results (default is 0).
    :return: A list of author objects matching the search criteria.
    """

    query = select(Author).filter(Author.name.contains(author_name))
    authors_db = await session.scalars(query.limit(limit).offset(offset))
    authors_list = list(authors_db.all())

    return authors_list


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


async def update_author_info(
    session: AsyncSession, author_to_update: Author, author_info: AuthorSchema
) -> Author:
    """
    Updates the information of an existing author with the given data.

    :param session: The asynchronous database session to use for the operation.
    :param author_to_update: The existing author instance to be updated.
    :param author_info: The schema containing updated data for the author.
                        Only fields that are set will be used for the update.
    :return: The updated author instance after the database commit and refresh.
    """

    for key, value in author_info.model_dump(exclude_unset=True).items():
        setattr(author_to_update, key, value)

    session.add(author_to_update)
    await session.commit()
    await session.refresh(author_to_update)

    return author_to_update
