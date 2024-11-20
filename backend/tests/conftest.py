import factory
import factory.fuzzy
import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from testcontainers.postgres import PostgresContainer

from src.app import app
from src.core.database import get_session
from src.core.security import get_password_hash
from src.models import Author, Book, User, table_registry


class UserFactory(factory.Factory):
    class Meta:
        model = User

    username = factory.Sequence(lambda n: f'test_name_{n}')
    email = factory.LazyAttribute(lambda user: f'{user.username}@test.com')
    password = factory.LazyAttribute(lambda user: f'{user.username}_pass')


class BookFactory(factory.Factory):
    class Meta:
        model = Book

    year = factory.fuzzy.FuzzyInteger(1700, 2000)
    title = factory.Sequence(lambda n: f'book_{n}')
    author_id = 1


class AuthorFactory(factory.Factory):
    class Meta:
        model = Author

    name = factory.Sequence(lambda n: f'author_{n}')


@pytest_asyncio.fixture(scope='session')
def postgres_container():
    with PostgresContainer('postgres:16', driver='asyncpg') as postgres:
        yield postgres


BASE_URL = 'http://test'


@pytest_asyncio.fixture
async def async_session(postgres_container):
    async_db_url = postgres_container.get_connection_url().replace(
        'postgresql://', 'postgresql+asyncpg://'
    )
    async_engine = create_async_engine(
        async_db_url, pool_pre_ping=True, echo=True
    )

    async with async_engine.begin() as conn:
        await conn.run_sync(table_registry.metadata.drop_all)
        await conn.run_sync(table_registry.metadata.create_all)

    async_session = sessionmaker(
        autoflush=False,
        bind=async_engine,
        class_=AsyncSession,
        expire_on_commit=False,
    )

    async with async_session() as as_session:
        yield as_session


@pytest_asyncio.fixture
async def async_client(async_session):
    app.dependency_overrides[get_session] = lambda: async_session
    _transport = ASGITransport(app=app)

    async with AsyncClient(
        transport=_transport, base_url=BASE_URL, follow_redirects=True
    ) as client:
        yield client

    app.dependency_overrides.clear()


@pytest_asyncio.fixture
async def token(async_client, user):
    response = await async_client.post(
        '/auth/token',
        data={'username': user.email, 'password': user.clean_password},
    )
    return response.json()['access_token']


@pytest_asyncio.fixture
async def user(async_session):
    pwd = 'testest'

    user = UserFactory(password=get_password_hash(pwd))

    async_session.add(user)
    await async_session.commit()
    await async_session.refresh(user)

    user.clean_password = pwd  # Monkey Patch

    return user


@pytest_asyncio.fixture
async def other_user(async_session):
    user = UserFactory()

    async_session.add(user)
    await async_session.commit()
    await async_session.refresh(user)

    return user


@pytest_asyncio.fixture
async def author(async_session):
    author = AuthorFactory()

    async_session.add(author)
    await async_session.commit()
    await async_session.refresh(author)

    return author


@pytest_asyncio.fixture
async def book(async_session, author):
    book = BookFactory()

    async_session.add(book)
    await async_session.commit()
    await async_session.refresh(book)

    return book
