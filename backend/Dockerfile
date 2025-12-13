# Backend service Dockerfile
FROM python:3.10-slim AS base

ENV PYTHONUNBUFFERED=1 \
    POETRY_VERSION=1.8.3 \
    POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_CREATE=false \
    PATH="/root/.local/bin:${PATH}"

RUN apt-get update && \
    apt-get install -y --no-install-recommends build-essential && \
    rm -rf /var/lib/apt/lists/* && \
    pip install --no-cache-dir "poetry==${POETRY_VERSION}"

WORKDIR /app

COPY pyproject.toml ./pyproject.toml
COPY backend ./backend

RUN poetry install --only main

EXPOSE 8000

CMD ["poetry", "run", "uvicorn", "backend.app:app", "--host", "0.0.0.0", "--port", "8000"]
