FROM python:3.12-bookworm

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV POETRY_VIRTUALENVS_CREATE=0

RUN pip install --no-cache-dir -U pip setuptools wheel
RUN pip install --no-cache-dir poetry

WORKDIR /app

RUN --mount=type=bind,source=./pyproject.toml,target=/app/pyproject.toml \
    --mount=type=bind,source=./poetry.lock,target=/app/poetry.lock \
    poetry install --no-root
