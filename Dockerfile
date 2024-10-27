FROM python:3.12-bookworm

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV POETRY_VIRTUALENVS_CREATE=0

RUN apt-get update && apt-get install -y --no-install-recommends \
    watchman \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir -U pip setuptools wheel
RUN pip install --no-cache-dir poetry

# Install pyenv for testing with different python versions
ENV PYENV_ROOT="$HOME/.pyenv"
ENV PATH="$PYENV_ROOT/bin:$PATH"
RUN curl https://pyenv.run | bash
RUN eval "$(pyenv init -)"
RUN pyenv install 3.13
RUN pyenv local 3.13

WORKDIR /app

RUN --mount=type=bind,source=./pyproject.toml,target=/app/pyproject.toml \
    --mount=type=bind,source=./poetry.lock,target=/app/poetry.lock \
    poetry install --no-root

