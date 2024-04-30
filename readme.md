# Readme structure.

## Title

### Short description

### Explain the folder architecture

### Configurations to run tests/project

Use this default, modify with your needs:

<b>Create a .env file with necessary values. Keys in .env.example<b>

Create a virtual env.
```
python -m venv {venv_name}
```

Starts venv (windows).
```
{venv_name}\Scripts\activate
```

Install necessary dependencies.
```
pip install -r requirements.txt
```

## Alembic.

Autogenerate models basing on SQLAlchemy models.

Generate new migration.
```
alembic revision --autogenerate -m 'message'
```

Run migration.
```
alembic upgrade head
```

## Running application

Install docker and docker-compose.
```
docker-compose up -d
```