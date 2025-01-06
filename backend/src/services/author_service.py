from sqlalchemy import delete, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.models import Author
from src.schemas.authors import AuthorSchema


async def add_author(session: AsyncSession, author: AuthorSchema) -> Author:
    """
    Add a new author to the database.

    :param session: The asynchronous database session used for the operation.
    :param author: The AuthorSchema object containing the details of the
        author to add.
    :return: The newly created Author object.
    """
    new_author = Author(**author.model_dump())

    async with session.begin():
        session.add(new_author)

    return new_author


async def get_author_by_id(
    session: AsyncSession, author_id: int
) -> Author | None:
    """
    Retrieve an author from the database by their ID.

    :param session: The asynchronous database session used for the query.
    :param author_id: The ID of the author to retrieve.
    :return: The Author object if found, otherwise None.
    """
    async with session:
        author_db = await session.scalar(
            select(Author).where(Author.id == author_id)
        )

    return author_db


async def get_author_by_name(
    session: AsyncSession, author_name: str
) -> Author | None:
    """
    Retrieve an author from the database by their name.

    :param session: The asynchronous database session used for the query.
    :param author_name: The name of the author to retrieve.
    :return: The Author object if found, otherwise None.
    """
    async with session:
        author_db = await session.scalar(
            select(Author).where(Author.name == author_name)
        )

    return author_db


async def get_filtered_authors_list(
    session: AsyncSession,
    limit: int | None,
    author_name: str | None = None,
    offset: int = 0,
) -> tuple[list[Author], int]:
    """
    Retrieve a paginated list of authors whose names contain a specified
    substring, and return the total number of authors in the database.

    This function supports optional filtering by author name. If a substring
    is provided, the returned list and count will be filtered accordingly.
    If no substring is provided, the function retrieves all authors.

    :param session: The asynchronous database session used to execute the
                    queries.
    :param author_name: An optional substring to filter authors by name. If
                        None, no filtering is applied.
    :param limit: The maximum number of authors to retrieve per page.
    :param offset: The number of authors to skip before retrieving results
                    (default is 0).
    :return: A tuple containing:
             - authors_list: A list of `Author` objects matching the search
               criteria.
             - total_count: The total number of authors in the database
               (filtered or unfiltered).
    """
    async with session:
        query = select(Author)
        count_query = select(func.count(Author.id))

        if author_name:
            filter_condition = Author.name.contains(author_name)
            query = query.filter(filter_condition)
            count_query = count_query.filter(filter_condition)

        if limit:
            query = query.limit(limit).offset(offset)

        total_count = await session.scalar(count_query)
        authors_db = await session.scalars(query)
        authors_list = authors_db.all()

    return list(authors_list), total_count or 0


async def get_authors_ids_list(
    session: AsyncSession, author_ids: list[int]
) -> list[int]:
    """
    Retrieve a list of author IDs that match the given list of IDs.

    :param session: The asynchronous database session used for the query.
    :param author_ids: A list of author IDs to search for in the database.
    :return: A list of author IDs that exist in the database.
    """
    async with session:
        authors_list = await session.scalars(
            select(Author.id).filter(Author.id.in_(author_ids))
        )

    return list(authors_list.all())


async def update_author_info(
    session: AsyncSession, author_to_update: Author, author_info: AuthorSchema
) -> Author:
    """
    Update the information of an existing author with the given data.

    :param session: The asynchronous database session used for the operation.
    :param author_to_update: The existing Author object to be updated.
    :param author_info: The schema containing updated data for the author.
        Only fields that are set will be used for the update.
    :return: The updated Author object after the database commit and refresh.
    """
    for key, value in author_info.model_dump(exclude_unset=True).items():
        setattr(author_to_update, key, value)

    async with session.begin():
        session.add(author_to_update)

    return author_to_update


async def delete_author(
    session: AsyncSession, author_to_delete: Author
) -> None:
    """
    Delete an author from the database and confirm deletion.

    :param session: The asynchronous database session used for the operation.
    :param author_to_delete: The Author object to be deleted from the database.
    :return: True if the author was successfully deleted, False otherwise.
    """
    async with session.begin():
        await session.delete(author_to_delete)


async def delete_authors_batch(
    session: AsyncSession, author_ids: list[int]
) -> None:
    """
    Delete authors in bulk based on a list of their IDs.

    This function removes all authors whose IDs match the provided list from
    the database.

    :param session: The asynchronous database session used for the operation.
    :param author_ids: A list of author IDs to delete from the database.
    :return: None
    """
    async with session.begin():
        await session.execute(delete(Author).where(Author.id.in_(author_ids)))
