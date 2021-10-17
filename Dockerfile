FROM python:3.9-slim

RUN python -m pip install -U pip poetry

WORKDIR /var/www/app

COPY poetry.lock ./poetry.lock
COPY pyproject.toml ./pyproject.toml

RUN poetry install --no-dev

COPY . .

RUN chmod +x ./wait-for-pg.sh

ENTRYPOINT poetry run aerich upgrade && \
    poetry run sanic user_api.main:app -H 0.0.0.0 -p 8000 -w 4
