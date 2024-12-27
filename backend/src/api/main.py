from fastapi import APIRouter

from src.api.routes import auth, author, books, supersuser, users

api_router = APIRouter()
api_router.include_router(auth.router, prefix='/auth', tags=['auth'])
api_router.include_router(
    supersuser.router, prefix='/supersuser', tags=['supersuser']
)
api_router.include_router(users.router, prefix='/users', tags=['users'])
api_router.include_router(author.router, prefix='/author', tags=['author'])
api_router.include_router(books.router, prefix='/book', tags=['book'])
