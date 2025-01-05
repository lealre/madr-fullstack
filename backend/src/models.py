from datetime import datetime
from typing import Any

from sqlalchemy import ForeignKey, func
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase, AsyncAttrs):
    __abstract__ = True

    def to_dict(self) -> dict[str, Any]:
        return {
            field.name: getattr(self, field.name) for field in self.__table__.c
        }


class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(unique=True)
    password_hash: Mapped[str]
    email: Mapped[str] = mapped_column(unique=True)
    first_name: Mapped[str] = mapped_column(default=None, nullable=True)
    last_name: Mapped[str] = mapped_column(default=None, nullable=True)
    is_superuser: Mapped[bool] = mapped_column(default=False)
    is_active: Mapped[bool] = mapped_column(default=True)
    is_verified: Mapped[bool] = mapped_column(default=False)
    google_sub: Mapped[str] = mapped_column(default=None, nullable=True)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        onupdate=func.now(), nullable=True
    )


class Book(Base):
    __tablename__ = 'books'

    id: Mapped[int] = mapped_column(primary_key=True)
    year: Mapped[int]
    title: Mapped[str] = mapped_column(unique=True)
    author_id: Mapped[int] = mapped_column(
        ForeignKey('authors.id', ondelete='CASCADE')
    )
    author: Mapped['Author'] = relationship(
        back_populates='books',
    )


class Author(Base):
    __tablename__ = 'authors'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique=True)
    books: Mapped[list[Book]] = relationship(
        back_populates='author',
        cascade='all, delete-orphan',
        passive_deletes=True,
    )
