from fastapi import FastAPI

from src.routers import auth, author, books, users
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.include_router(users.router)
app.include_router(auth.router)
app.include_router(books.router)
app.include_router(author.router)

origins = ['http://localhost:5173']

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

@app.get('/')
def home_root():
    return {'message': 'Root Endpoint!'}
