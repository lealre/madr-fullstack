# MADR - A simplified version of a digital book collection - FastAPI + React

This project consists of a web application for a simplified version of a digital book collection. It is an extension of [this repo](https://github.com/lealre/madr-fastapi).

- 💻 **Backend**
  - [FastAPI](https://fastapi.tiangolo.com/){:target="\_blank"} for the Python backend API, with asynchronous routes.
  - [SQLAlchemy](https://www.sqlalchemy.org/){:target="\_blank"} for Python SQL database interactions (ORM).
  - [Pydantic](https://docs.pydantic.dev/latest/){:target="\_blank"}, used by FastAPI, for data validation and settings management.
  - PostgreSQL as the SQL database, using the [Asyncpg](https://magicstack.github.io/asyncpg/current/){:target="\_blank"} driver.
  - Tests with [Pytest](https://docs.pytest.org/en/stable/){:target="\_blank"} and [Testcontainers](https://testcontainers-python.readthedocs.io/en/latest/){:target="\_blank"}.
  - [Pre-commit](https://pre-commit.com/){:target="\_blank"} with [Ruff](https://docs.astral.sh/ruff/){:target="\_blank"} for linting.
  - CI (Continuous Integration) based on GitHub Actions.
- 🌐 **Frontend**
  - [React](https://react.dev/){:target="\_blank"} using TypeScript and Vite.
  - [Chakra UI](https://www.chakra-ui.com/){:target="\_blank"} for frontend components.
- 🔒 Secure password hashing by default.
- 🔑 JWT (JSON Web Token) authentication.
- 🐋 Docker Compose for running all services together, including the PostgreSQL database.

## About the Project

- Login
- SignUp
- Create and Delete Authors
- Create and Delte Books based on the Auhtors list

The idea is to gradually adding more features as they are listed in the Further Improvemets section

#### Folder Structure

```
.
├── README.md
├── backend
│   ├── Dockerfile
│   ├── README.md
│   ├── alembic.ini
│   ├── poetry.lock
│   ├── pyproject.toml
│   ├── scripts
│   │   ├── init_db.sh
│   │   └── init_db_dev.sh
│   ├── src
│   │   ├── __init__.py
│   │   ├── api
│   │   ├── app.py
│   │   ├── core
│   │   ├── migrations
│   │   ├── models.py
│   │   ├── schemas
│   │   ├── services
│   │   └── utils
│   └── tests
│       ├── __init__.py
│       ├── conftest.py
│       ├── routes
│       ├── services
│       └── test_superuser_creation.py
├── docker-compose.yaml
└── frontend
    ├── Dockerfile
    ├── README.md
    ├── eslint.config.js
    ├── index.html
    ├── nginx.conf
    ├── package-lock.json
    ├── package.json
    ├── public
    │   └── logo.svg
    ├── src
    │   ├── App.tsx
    │   ├── api
    │   ├── components
    │   ├── dto
    │   ├── main.tsx
    │   ├── pages
    │   ├── routes
    │   ├── theme.ts
    │   └── vite-env.d.ts
    ├── tsconfig.app.json
    ├── tsconfig.json
    ├── tsconfig.node.json
    └── vite.config.ts
```

## How to Run This Project

## Further Improvements
