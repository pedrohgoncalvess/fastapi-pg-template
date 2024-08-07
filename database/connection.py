import os

from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

from utils.env_vars import get_env_var
from utils.project_dir import rootDir


class DatabaseConnection:
    """
    A class responsible for instantiating a connection to the database.
    """
    def __init__(self):
        self.__dbHost__ = get_env_var("DB_HOST")
        self.__dbPort__ = get_env_var("DB_PORT")
        self.__dbName_ = get_env_var("DB_NAME")
        self.__dbUser__ = get_env_var("DB_USER")
        self.__dbPassword__ = get_env_var("DB_PASSWORD")

        self._engine_ = create_engine(
            f"postgresql+psycopg2://{self.__dbUser__}:{self.__dbPassword__}@{self.__dbHost__}:{self.__dbPort__}/{self.__dbName_}")

        """
        Transform all dirs at database/models/ in a list  
        """
        self.schemas = [schemaName for schemaName in os.listdir(f"{rootDir}/database/models/") if
                        os.path.isdir(os.path.join(f"{rootDir}/database/models/", schemaName))]

        def buildSchemas():
            for schema in self.schemas:
                dbConn = sessionmaker(autocommit=False, autoflush=False, bind=self._engine_, expire_on_commit=False)()
                dbConn.execute(text(f"CREATE SCHEMA IF NOT EXISTS {schema}"))
                dbConn.commit()
                dbConn.close()

        buildSchemas() #Transform all itens on self.schemas in a schema at database

    def __enter__(self):
        """
        A method to enable the with clause and chain operations with the cursor

        :return: database cursor
        """
        self.dbConn = sessionmaker(autocommit=False, autoflush=False, bind=self._engine_, expire_on_commit=False)()
        return self.dbConn

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        The method that terminates the method that enables the with clause
        :param exc_type: It doesn't need to be passed.
        :param exc_val: It doesn't need to be passed.
        :param exc_tb: It doesn't need to be passed.
        :return: nothing.
        """
        self.dbConn.close()


"""
This is a singleton of connection
"""
dbConnection = DatabaseConnection()
