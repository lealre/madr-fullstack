from typing import List

from pydantic import BaseModel


class Message(BaseModel):
    message: str


class Email(BaseModel):
    addresses: List[str]
