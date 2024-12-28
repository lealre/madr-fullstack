from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.security import get_password_hash
from src.models import User
from src.schemas.users import (
    SuperUserRequestCreate,
    SuperUserRequestUpdate,
    UserRequestCreate,
    UserRequestUpdate,
)


async def add_user(
    session: AsyncSession, user: SuperUserRequestCreate | UserRequestCreate
) -> User:
    """
    Add a new user to the database.

    :param session: The asynchronous database session used for the operation.
    :param user: A `SuperUserRequestCreate` or `UserRequestCreate` object
        containing the user data.
    :return: The created `User` object with the hashed password.
    """
    hashed_password = get_password_hash(user.password)
    del user.password

    user_attrs = user.model_dump()
    user_attrs['password_hash'] = hashed_password
    new_user = User(**user_attrs)

    async with session.begin():
        session.add(new_user)

    return new_user


async def get_user(
    session: AsyncSession,
    user_email: str | None = None,
    username: str | None = None,
) -> User | None:
    """
    Retrieve a user from the database by username or email.

    :param session: The asynchronous database session used for the query.
    :param user_email: The email of the user to retrieve.
    :param username: The username of the user to retrieve.
    :return: The User object if found, otherwise None.
    """
    async with session:
        user_db = await session.scalar(
            select(User).where(
                (User.username == username) | (User.email == user_email)
            )
        )

    return user_db


async def get_user_by_id(session: AsyncSession, user_id: int) -> User | None:
    """
    Retrieve a user from the database by their ID.

    :param session: The asynchronous database session used for the query.
    :param user_id: The ID of the user to retrieve.
    :return: The User object if found, otherwise None.
    """
    async with session:
        user = await session.scalar(select(User).where(User.id == user_id))

    return user


async def get_users_list(
    session: AsyncSession, limit: int, offset: int
) -> list[User]:
    """
    Retrieve a paginated list of users from the database.

    :param session: The asynchronous database session used for the query.
    :param limit: The maximum number of users to retrieve.
    :param offset: The number of users to skip before starting to retrieve
        results.
    :return: A list of User objects.
    """
    async with session:
        users_db = await session.scalars(
            select(User).offset(offset).limit(limit)
        )
        all_users = list(users_db.all())

    return all_users


async def update_user_info(
    session: AsyncSession,
    user_info: SuperUserRequestUpdate | UserRequestUpdate,
    user_to_update: User,
) -> User:
    """
    Update the information of an existing user.

    :param session: The asynchronous database session used for the operation.
    :param user_info: A `SuperUserRequestUpdate` or `UserRequestUpdate` object
        containing the updated user data.
    :param user_to_update: The `User` object to be updated with the new
        information.
    :return: The updated `User` object after the changes are committed.
    """
    for key, value in user_info.model_dump(exclude_unset=True).items():
        setattr(user_to_update, key, value)

    async with session.begin():
        session.add(user_to_update)

    return user_to_update


async def change_password(
    session: AsyncSession, user_to_update: User, password: str
) -> User:
    """
    Update the password of an existing user.

    Hashes the provided password and updates the `password_hash` field of the
    user identified by `user_to_update`. The change is then committed to the
    database.

    :param session: The asynchronous database session used for the operation.
    :param user_to_update: The `User` object whose password is being updated.
    :param password: The new password to set for the user.
    :return: The updated `User` object with the new password hash.
    """
    hashed_password = get_password_hash(password)
    user_to_update.password_hash = hashed_password

    async with session.begin():
        session.add(user_to_update)

    return user_to_update
