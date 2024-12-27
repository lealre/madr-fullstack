import asyncio

from src.core.database import AsyncSessionLocal, init_db


async def main() -> None:
    async with AsyncSessionLocal() as session:
        await init_db(session)


if __name__ == '__main__':
    asyncio.run(main())
