from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import QueuePool

from utils.env_vars import get_env_var


class DatabaseConnection:
    """
    A class responsible for instantiating an asynchronous connection pool to the database.
    """

    def __init__(self):
        self._db_host_ = get_env_var("DB_HOST")
        self._db_port_ = get_env_var("DB_PORT")
        self._db_name_ = get_env_var("DB_NAME")
        self._db_user_ = get_env_var("DB_USER")
        self._db_password_ = get_env_var("DB_PASSWORD")

        self._engine_ = create_async_engine(
            f"postgresql+asyncpg://{self._db_user_}:{self._db_password_}@{self._db_host_}:{self._db_port_}/{self._db_name_}",
            poolclass=QueuePool,
            pool_size=5,
            max_overflow=10,
            pool_timeout=30,
            pool_recycle=1800,
            pool_pre_ping=True,
        )

        self.async_session = sessionmaker(
            bind=self._engine_,
            class_=AsyncSession,
            expire_on_commit=False,
            autocommit=False,
            autoflush=False
        )

    async def __aenter__(self):
        """
        Async context manager entry point to enable the async with clause

        :return: async database session
        """
        self.db_session = self.async_session()
        return self.db_session

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """
        Async context manager exit point that terminates the session

        :param exc_type: Exception type if an exception was raised
        :param exc_val: Exception value if an exception was raised
        :param exc_tb: Exception traceback if an exception was raised
        """
        await self.db_session.close()

    async def close(self):
        """
        Close the engine and connection pool
        """
        await self._engine_.dispose()