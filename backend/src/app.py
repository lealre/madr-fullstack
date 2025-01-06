from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.api.main import api_router
from src.schemas.base import Message

app = FastAPI()

origins = ['*']  # ['http://localhost:5173']

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

app.include_router(api_router)


@app.get('/')
def home_root() -> Message:  # pragma: no cover
    return Message(message='Root Endpoint!')
