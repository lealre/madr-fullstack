from pydantic import BaseModel


class ErrorResponse(BaseModel):
    detail: str


response_model = {'model': ErrorResponse}
