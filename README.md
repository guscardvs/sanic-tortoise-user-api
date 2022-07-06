# Sanic Tortoise User API

> A simple user API to learn how to use [Sanic](https://sanic.dev/en/guide/getting-started.html) and [Tortoise-ORM](https://tortoise-orm.readthedocs.io/en/latest/)


## Enviroment Variables

> To run this project, you will need to add the following
> variables to your environment or .env

`PROJECT_KEY` -> Secret to make JWTs and other security related features, you can use:

```bash
  openssl rand -hex 32
```

`DATABASE_URI` -> URI with schema to connect to db, Ex: sqlite://db.sqlite3


## Authors

- [@guscardvs](https://www.github.com/guscardvs)


## Features

- Register
- Login
- Logout
- Profile CRUD


## Setup

Install sanic-tortoise-user-api with [poetry](https://python-poetry.org)

```bash
  cd sanic-tortoise-user-api
  poetry install
```

Or

```bash
  cd sanic-tortoise-user-api
  docker compose up -d
```
## Roadmap

- Add unit tests


## Project Stack

**Back-end:** Python, Sanic, TortoiseORM


## Deploy

To build project:

```bash
  docker build -t sanic-tortoise-user-api:latest .
```

- Docker exposes port 8000

## Run locally

Clone the project

```bash
  git clone https://github.com/guscardvs/sanic-tortoise-user-api
```

Enter project directory

```bash
  cd sanic-tortoise-user-api
```

Install packages

```bash
  poetry install
```

Start the Server (Port 5000)

```bash
  make run-dev
```

