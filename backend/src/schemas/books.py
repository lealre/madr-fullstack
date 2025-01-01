import re

from pydantic import BaseModel, Field, field_validator


class BookSchema(BaseModel):
    title: str
    year: int = Field(gt=0, lt=2025)
    author_id: int = Field(gt=0)

    @field_validator('title')
    def validate_name(cls, v: str) -> str:
        v = v.lower().strip()
        return re.sub(r'\s+', ' ', v)


class BookPublic(BaseModel):
    id: int
    title: str
    year: int = Field(gt=0, lt=2025)
    author: str


class BookResponseCreate(BookPublic):
    author_id: int


class BookUpdate(BaseModel):
    year: int = Field(gt=0, lt=2025)


class BookList(BaseModel):
    books: list[BookPublic]
    total_results: int


class DeteleBooksBulk(BaseModel):
    ids: list[int]
