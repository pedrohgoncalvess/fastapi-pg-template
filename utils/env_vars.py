import os

from dotenv import load_dotenv

from utils.project_dir import rootDir


if os.path.isfile(f'{rootDir}/.env'):
    load_dotenv(f'{rootDir}/.env')
else:
    load_dotenv(f'{rootDir}/.env.docker')


def get_env_var(key: str) -> str | None:
    return os.getenv(key)
