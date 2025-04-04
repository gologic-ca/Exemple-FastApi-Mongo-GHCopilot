# ![RealWorld FastAPI + SQLAlchemy App](logo.png)

<div align="center">

<!---
[![CircleCI](https://circleci.com/gh/......)](https://circleci.com/gh/...)
[![codecov](https://codecov.io/gh/.../........)](https://codecov.io/gh/.....)
[![Maintainability](https://api.codeclimate.com/v1/badges/......)](https://codeclimate.com/repos/....)
-->

![Python: 3.10](https://img.shields.io/badge/python-3.10-informational.svg)
[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/pre-commit/pre-commit)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/python/black)
[![mypy: checked](https://img.shields.io/badge/mypy-checked-informational.svg)](http://mypy-lang.org/)
[![Manager: poetry](https://img.shields.io/badge/manager-poetry-blueviolet.svg)](https://poetry.eustace.io/)

</div>

> ### [FastAPI](https://github.com/tiangolo/fastapi) + [SQLAlchemy](https://www.sqlalchemy.org/) codebase containing real world examples (CRUD, auth, advanced patterns, etc) that adheres to the [RealWorld](https://github.com/gothinkster/realworld) spec and API.

[![CI](https://github.com/art049/fastapi-sqlalchemy-realworld-example/actions/workflows/ci.yml/badge.svg)](https://github.com/art049/fastapi-sqlalchemy-realworld-example/actions/workflows/ci.yml)
[![Realworld Tests](https://github.com/art049/fastapi-sqlalchemy-realworld-example/actions/workflows/realworld-tests.yml/badge.svg)](https://github.com/art049/fastapi-sqlalchemy-realworld-example/actions/workflows/realworld-tests.yml)

# Getting started

You can view a live demo at [https://demo.realworld.io/](https://demo.realworld.io/)

## Prerequisites

- Python 3.9+
- pip

## Installation

1. Clone the repository:

```bash
git clone https://github.com/yourusername/fastapi-sqlalchemy-realworld-example.git
cd fastapi-sqlalchemy-realworld-example
```

2. Create a virtual environment and activate it:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:

```bash
pip install -e .
```

4. Initialize the database:

```bash
alembic upgrade head
```

5. Run the application:

```bash
uvicorn src.api:app --reload
```

The API will be available at [http://localhost:8000](http://localhost:8000)

## Features

- User authentication (JWT)
- User registration and login
- Profile management
- Article CRUD operations
- Comments on articles
- Favorite articles
- Follow/unfollow users
- Tags management

## API Documentation

Once the application is running, you can access:

- Swagger UI documentation at [http://localhost:8000/docs](http://localhost:8000/docs)
- ReDoc documentation at [http://localhost:8000/redoc](http://localhost:8000/redoc)

## Testing

Run the tests with:

```bash
pytest
```

## License

MIT
