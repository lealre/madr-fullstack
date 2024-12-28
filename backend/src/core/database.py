from sqlalchemy import select
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from src.core.security import get_password_hash
from src.core.settings import settings
from src.models import User

engine = create_async_engine(settings.DATABASE_URL, echo=True)

AsyncSessionLocal = async_sessionmaker(
    expire_on_commit=False,
    bind=engine,
    class_=AsyncSession,
)


async def init_db(session: AsyncSession) -> None:
    user = await session.scalar(
        select(User).where(User.email == settings.FIRST_SUPERUSER_EMAIL)
    )

    if not user:
        hashed_password = get_password_hash(settings.FIRST_SUPERUSER_PASSWORD)

        user_db = User(  # type: ignore[call-arg]
            username=settings.FIRST_SUPERUSER_USERNAME,
            email=settings.FIRST_SUPERUSER_EMAIL,
            password_hash=hashed_password,
            is_superuser=True,
            is_verified=True,
        )

        session.add(user_db)
        await session.commit()

        print('Superuser created')
        return

    print('Superuser with these credentials already exists')
