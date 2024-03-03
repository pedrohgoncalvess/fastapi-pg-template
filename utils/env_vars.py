import os
from dotenv import load_dotenv

if os.path.isfile('../.env'):
    load_dotenv('../.env')
else:
    load_dotenv('../.env.docker')


def get_env_var(key: str):
    return os.getenv(key)
