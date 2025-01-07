import asyncio

from src.core.database import AsyncSessionLocal, create_superuser


async def main() -> None:
    async with AsyncSessionLocal() as session:
        await create_superuser(session)


if __name__ == '__main__':
    asyncio.run(main())
