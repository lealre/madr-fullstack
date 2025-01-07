from sqlalchemy.ext.asyncio import AsyncSession

from src.core.database import create_superuser
from src.core.settings import settings
from src.services import user_service


async def test_create_superuser(async_session: AsyncSession) -> None:
    await create_superuser(async_session)

    superuser = await user_service.get_user(
        session=async_session, user_email=settings.FIRST_SUPERUSER_EMAIL
    )

    assert superuser
    assert superuser.is_superuser
    assert superuser.is_verified
    assert superuser.username == settings.FIRST_SUPERUSER_USERNAME
