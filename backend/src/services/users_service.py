from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.security import get_password_hash
from src.models import User
from src.schemas.users import SuperUserRequestCreate, SuperUserRequestUpdate


async def get_user(
    session: AsyncSession, user_email: str, username: str
) -> User | None:
    """
    Retrieve a user from the database by username or email.

    :param username: The username of the user to retrieve.
    :param email: The email of the user to retrieve.
    :return: The user object if found, otherwise None.
    """

    user_db = await session.scalar(
        select(User).where(
            (User.username == username) | (User.email == user_email)
        )
    )

    return user_db


async def get_user_by_id(session: AsyncSession, user_id: int) -> User:
    """
    Retrieve a user from the database by their ID.

    :param session: The asynchronous database session used for the query.
    :param user_id: The ID of the user to retrieve.
    :return: The user object if found, otherwise None.
    """

    user = await session.scalar(select(User).where(User.id == user_id))

    return user


async def get_users_list(
    session: AsyncSession, limit: int, offset: int
) -> list[User]:
    """
    Retrieve a paginated list of users from the database.

    :param session: The asynchronous database session used for the query.
    :param limit: The maximum number of users to retrieve.
    :param offset: The number of users to skip before starting
    to retrieve results.
    :return: A list of user objects wrapped in a UserListResponse.
    """

    users_db = await session.scalars(select(User).offset(offset).limit(limit))

    return users_db.all()


async def add_user(
    session: AsyncSession, user: SuperUserRequestCreate
) -> User:
    """
    Add a new user to the database.

    Hashes the user's password, creates a new `User` object, and saves
    it to the database.

    :param session: The asynchronous database session used for the query.
    :param user: A `SuperUserRequestCreate` object containing the user data.
    :return: The created `User` object with the hashed password.
    """

    hashed_password = get_password_hash(user.password)
    del user.password

    new_user = User(**user.model_dump(), password_hash=hashed_password)

    session.add(new_user)
    await session.commit()
    await session.refresh(new_user)

    return new_user


async def update_user_info(
    session: AsyncSession,
    user_info: SuperUserRequestUpdate,
    user_to_update: User,
) -> User:
    """
    Update the information of an existing user.

    Updates the fields of the user identified by `user_to_update` with the
    values provided in `user_info`. Only the fields that are explicitly set
    in `user_info` will be updated. The changes are committed to the database.

    :param session: The asynchronous database session used for the query.
    :param user_info: A `SuperUserRequestUpdate` object containing the updated
    user data.
    :param user_to_update: The `User` object to be updated with the new
    information.
    :return: The updated `User` object after the changes are committed.
    """

    for key, value in user_info.model_dump(exclude_unset=True).items():
        setattr(user_to_update, key, value)

    session.add(user_to_update)
    await session.commit()
    await session.refresh(user_to_update)

    return user_to_update
