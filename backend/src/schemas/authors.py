import re

from pydantic import BaseModel, field_validator


class AuthorSchema(BaseModel):
    name: str

    @field_validator('name')
    def validate_name(cls, v: str) -> str:
        v = v.lower().strip()
        return re.sub(r'\s+', ' ', v)


class AuthorPublic(AuthorSchema):
    id: int


class AuthorList(BaseModel):
    authors: list[AuthorPublic]
    total_results: int


class DeteleAuthosBulk(BaseModel):
    ids: list[int]
