import anyio
from sqlalchemy.exc import IntegrityError

from src.core.database import AsyncSessionLocal
from src.models import Author, Book
from src.utils import DATA


async def populate_authors() -> None:
    try:  # noqa: PLR1702
        async with AsyncSessionLocal() as session:
            for author, books in DATA.items():
                new_author = Author(name=author)  # type: ignore[call-arg]
                try:
                    async with session.begin():
                        session.add(new_author)
                except IntegrityError:
                    pass

                for title, year in books.items():
                    new_book = Book(  # type: ignore[call-arg]
                        title=title, year=year, author_id=new_author.id
                    )
                    try:
                        async with session.begin():
                            session.add(new_book)
                    except IntegrityError:
                        pass
    except Exception as e:
        print('It was not possible to populate the database ', e)


if __name__ == '__main__':
    anyio.run(populate_authors)
