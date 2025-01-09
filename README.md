# MADR - A Digital Book Collection: FastAPI + React

This project consists of a web application for a simplified version of a digital book collection.

It is an extension of [this repo](https://github.com/lealre/madr-fastapi).

- 💻 **Backend**
  - [FastAPI](https://fastapi.tiangolo.com/) for the Python backend API, with asynchronous routes.
  - [SQLAlchemy](https://www.sqlalchemy.org/) for Python SQL database interactions (ORM).
  - [Pydantic](https://docs.pydantic.dev/latest/), used by FastAPI, for data validation and settings management.
  - PostgreSQL as the SQL database, using the [Asyncpg](https://magicstack.github.io/asyncpg/current/) driver.
  - Tests with [Pytest](https://docs.pytest.org/en/stable/) and [Testcontainers](https://testcontainers-python.readthedocs.io/en/latest/).
  - [Pre-commit](https://pre-commit.com/) with [Ruff](https://docs.astral.sh/ruff/) for linting.
  - CI (Continuous Integration) based on GitHub Actions.
- 🌐 **Frontend**

  - [React](https://react.dev/) using TypeScript and Vite.
  - [Chakra UI](https://www.chakra-ui.com/) for frontend components.
  - [Axios](https://axios-http.com/docs/intro) to handle the backend API requests.
  - [React Hook Form](https://react-hook-form.com/) to handle the submission of data in forms.

- 🔒 Secure password hashing by default.
- 🔑 JWT (JSON Web Token) authentication.
- 🐋 Docker Compose for running all services together, including the PostgreSQL database.

Below is a quick demonstration of the app working in a local Docker environment.

![](media/full-demo.gif)

## Table of Contents

- [About the Project](#about-the-project)
  - [Folder Structure](#folder-structure)
- [How to Run This Project](#how-to-run-this-project)
- [Further Improvements](#further-improvements)

## About the Project

The app serves as a simple catalog of authors and books, where you can only register a book if an author is already registered. The dashboard area allows users to switch between author and book tabs, select records to delete in batch, add new records by opening a modal, and search for specific records. The search functionality enables searching by book or author name, based on the currently active tab.

On the frontend, the JWT is stored in local storage. The dashboard area is a protected page requiring authentication, where users must log in to manage the collection records.

Below is a demonstration of a user trying to access the `/dashboard` endpoint. Since the user is not authenticated, the app redirects them to the `/login` page and displays a message in a toast component.

![](media/auth-demo.gif)

Although the backend API allows role-based functionality between admin and user, this distinction has not yet been implemented in the frontend.

The idea is to gradually add more features and improve the code as they are listed in the Further Improvements section.

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

All the steps here are intended for a `bash` terminal.

This section shows how to run the project using Docker by building all three services together: Backend, Frontend, and the PostgreSQL database.

[How to install Docker Compose](https://docs.docker.com/compose/install/)

1 - Clone the repo locally:

```bash
git clone https://github.com/lealre/madr-fullstack.git
```

2 - Access the project directory:

```bash
cd madr-fullstack
```

Once inside the folder, it is possible to set the environment variables in the `.env` file for both the backend and frontend. In both the `backend` and `frontend` folders, there is an `.env-example` file that simulates the `.env` variables.

In the root directory, run the commands below to use them as `.env`:

- Backend

  ```bash
  mv backend/.env-example backend/.env
  ```

- Frontend

  ```bash
  mv frontend/.env-example frontend/.env
  ```

The `.env` file is not strictly necessary, as the `docker-compose.yaml` will use defautl values in case the files are not set in the folders, but if the `DATABASE_URL` is set, its necessary to switch the value depending on whether it will use the PostgreSQL database in the Docker environment or the local SQLite. By default, the `DATABASE_URL` is set to use SQLite.

Below are the examples of the `.env` variables:

- Backend

  ```
  DATABASE_URL=postgresql+asyncpg://user:password@postgres:5432/madr_db

  SECRET_KEY=your-secret-key
  ALGORITHM=HS256
  ACCESS_TOKEN_EXPIRE_MINUTES=60

  FIRST_SUPERUSER_USERNAME=admin
  FIRST_SUPERUSER_EMAIL=admin@admin.com'
  FIRST_SUPERUSER_PASSWORD=admin
  ```

- Frontend

  ```
  VITE_API_URL=http://localhost:8000
  ```

Once the variables in the `.env` file are defined, the following command will build and start the application:

```bash
docker compose up
```

After the container is ready, it will automatically populate the database with some example data, as shown in the video demo, and also create the user based on the `.env` variables set. The default user credentials are:

`email: admin@admin.com`
`password: admin`

You can access the application via the link below:

```bash
http://localhost:3000
```

## Further Improvements

Some additional functionalities that could be implemented in the app:

- Add more fields to the books and authors tables.
- Implement token refresh.
- Improve the search system by:
  - Applying more filters and allowing searches for authors in the books tab.
  - Creating more filter and sorting options.
- Add the option to edit records.
- Utilize the role-based system, where:
  - Only the admin role can manage the collection.
  - Provide a user area where regular users can star books, leave reviews, and rank them.
  - Allow users to verify their accounts via email and recover access if needed.
  - Enable users to submit requests for new books to be added.

Regarding the code, the frontend still lacks tests, linter checks, and integration into the CI routine.
