from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from src.core.settings import settings

engine = create_async_engine(settings.DATABASE_URL, future=True, echo=True)

AsyncSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=True,
    expire_on_commit=False,
    bind=engine,
    class_=AsyncSession,
)


async def get_session():  # pragma: no cover
    async with AsyncSessionLocal() as session:
        yield session


T_Session = Annotated[AsyncSession, Depends(get_session)]
