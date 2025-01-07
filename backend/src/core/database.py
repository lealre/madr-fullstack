from typing import Any

from sqlalchemy import event, select
from sqlalchemy.dialects.sqlite.aiosqlite import (
    AsyncAdapt_aiosqlite_connection,
)
from sqlalchemy.engine import Engine
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from src.core.security import get_password_hash
from src.core.settings import settings
from src.models import User


# To allow cascading delete from parent to child (sqlite)
# The PRAGMA foreign_keys = ON statement must be emitted on all
# connections before use
# https://docs.sqlalchemy.org/en/20/dialects/sqlite.html#foreign-key-support
# https://docs.sqlalchemy.org/en/20/core/event.html
# https://docs.sqlalchemy.org/en/20/core/events.html#sqlalchemy.events.PoolEvents.connect
@event.listens_for(Engine, 'connect', named=True)
def set_sqlite_pragma(**kw: dict[str, Any]) -> None:  # pragma: no cover
    dbapi_connection = kw.get('dbapi_connection')
    if isinstance(dbapi_connection, AsyncAdapt_aiosqlite_connection):
        cursor = dbapi_connection.cursor()
        cursor.execute('PRAGMA foreign_keys=ON')
        cursor.close()


engine = create_async_engine(settings.DATABASE_URL, echo=True)

AsyncSessionLocal = async_sessionmaker(
    expire_on_commit=False,
    bind=engine,
    class_=AsyncSession,
)


async def create_superuser(session: AsyncSession) -> None:
    async with session.begin():
        user = await session.scalar(
            select(User).where(User.email == settings.FIRST_SUPERUSER_EMAIL)
        )

        if not user:
            hashed_password = get_password_hash(
                settings.FIRST_SUPERUSER_PASSWORD
            )

            user_db = User(
                username=settings.FIRST_SUPERUSER_USERNAME,
                email=settings.FIRST_SUPERUSER_EMAIL,
                password_hash=hashed_password,
                is_superuser=True,
                is_verified=True,
            )

            session.add(user_db)

        print('Superuser created')

    print('Superuser with these credentials already exists')
