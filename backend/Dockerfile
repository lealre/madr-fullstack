FROM python:3.12-slim
ENV POETRY_VIRTUALENVS_CREATE=false

WORKDIR /app/
COPY . .

RUN pip install poetry

RUN poetry config installer.max-workers 10
RUN poetry install --without dev --no-interaction --no-ansi

EXPOSE 8000