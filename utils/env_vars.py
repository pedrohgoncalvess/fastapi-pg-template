import os

from dotenv import load_dotenv

from utils.project_dir import root_dir


if os.path.isfile(f'{root_dir}/.env'):
    load_dotenv(f'{root_dir}/.env')
else:
    load_dotenv(f'{root_dir}/.env.docker')


def get_env_var(key: str) -> str | None:
    return os.getenv(key)
