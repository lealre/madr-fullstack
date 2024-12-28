import typing

import factory
import factory.fuzzy
import pytest
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from testcontainers.postgres import PostgresContainer

from src.api.dependencies import get_session
from src.app import app
from src.core.security import get_password_hash
from src.core.settings import settings
from src.models import Author, Book, User, table_registry
from src.schemas.token import Token
from src.schemas.users import UserResponse


class UserFactory(factory.Factory):  # type: ignore[misc]
    class Meta:
        model = User

    username = factory.Sequence(lambda n: f'test_name_{n}')
    email = factory.LazyAttribute(lambda user: f'{user.username}@test.com')
    password_hash = factory.LazyAttribute(lambda user: f'{user.username}_pass')
    is_superuser = False


class BookFactory(factory.Factory):  # type: ignore[misc]
    class Meta:
        model = Book

    year = factory.fuzzy.FuzzyInteger(1700, 2000)
    title = factory.Sequence(lambda n: f'book_{n}')
    author_id = 1


class AuthorFactory(factory.Factory):  # type: ignore[misc]
    class Meta:
        model = Author

    name = factory.Sequence(lambda n: f'author_{n}')


class MockedUser(UserResponse):
    id: int
    clean_password: str


@pytest.fixture(scope='session')
def anyio_backend() -> str:
    return 'asyncio'


@pytest.fixture(scope='session')
def postgres_container(
    anyio_backend: typing.Literal['asyncio'],
) -> typing.Generator[PostgresContainer, None, None]:
    with PostgresContainer('postgres:16', driver='asyncpg') as postgres:
        yield postgres


BASE_URL = 'http://test'


@pytest.fixture
async def async_session(
    postgres_container: PostgresContainer,
) -> typing.AsyncGenerator[AsyncSession, None]:
    async_db_url = postgres_container.get_connection_url()
    async_engine = create_async_engine(async_db_url, pool_pre_ping=True)

    async with async_engine.begin() as conn:
        await conn.run_sync(table_registry.metadata.drop_all)
        await conn.run_sync(table_registry.metadata.create_all)

    async_session = async_sessionmaker(
        bind=async_engine,
        expire_on_commit=False,
        class_=AsyncSession,
    )

    async with async_session() as as_session:
        yield as_session


@pytest.fixture
async def async_client(
    async_session: AsyncSession,
) -> typing.AsyncGenerator[AsyncClient, None]:
    app.dependency_overrides[get_session] = lambda: async_session
    _transport = ASGITransport(app=app)

    async with AsyncClient(
        transport=_transport, base_url=BASE_URL, follow_redirects=True
    ) as client:
        yield client

    app.dependency_overrides.clear()


@pytest.fixture
async def superuser_token(
    async_client: AsyncClient, superuser: MockedUser
) -> str:
    response = await async_client.post(
        '/auth/token',
        data={
            'username': superuser.email,
            'password': superuser.clean_password,
        },
    )

    json_response = Token.model_validate(response.json())
    return json_response.access_token


@pytest.fixture
async def user_token(async_client: AsyncClient, user: MockedUser) -> str:
    response = await async_client.post(
        '/auth/token',
        data={'username': user.email, 'password': user.clean_password},
    )

    json_response = Token.model_validate(response.json())
    return json_response.access_token


@pytest.fixture
async def superuser(async_session: AsyncSession) -> MockedUser:
    pwd = settings.FIRST_SUPERUSER_PASSWORD

    superuser = User(  # type: ignore[call-arg]
        username=settings.FIRST_SUPERUSER_USERNAME,
        email=settings.FIRST_SUPERUSER_EMAIL,
        password_hash=get_password_hash(pwd),
        is_superuser=True,
    )

    async with async_session.begin():
        async_session.add(superuser)

    superuser_attrs = superuser.__dict__
    superuser_attrs['clean_password'] = settings.FIRST_SUPERUSER_PASSWORD
    superuser_attrs['password'] = superuser.password_hash
    mocked_superuser = MockedUser(**superuser_attrs)

    return mocked_superuser


@pytest.fixture
async def user(async_session: AsyncSession) -> MockedUser:
    pwd = 'testest'

    user = UserFactory(password_hash=get_password_hash(pwd))

    async with async_session.begin():
        async_session.add(user)

    user_attrs = user.__dict__
    user_attrs['clean_password'] = pwd
    user_attrs['password'] = user.password_hash
    mocked_user = MockedUser(**user_attrs)

    return mocked_user


@pytest.fixture
async def other_user(async_session: AsyncSession) -> User:
    user = UserFactory()

    async with async_session.begin():
        async_session.add(user)

    return user


@pytest.fixture
async def author(async_session: AsyncSession) -> Author:
    author = AuthorFactory()

    async with async_session.begin():
        async_session.add(author)

    return author


@pytest.fixture
async def book(async_session: AsyncSession, author: Author) -> Book:
    book = BookFactory()

    async with async_session.begin():
        async_session.add(book)

    return book
