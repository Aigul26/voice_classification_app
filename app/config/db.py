import logging
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from abc import ABC, abstractmethod
from app.config.config import settings

class DatabaseConnection(ABC):
    @abstractmethod
    def get_engine(self):
        pass

    @abstractmethod
    def get_sessionmaker(self):
        pass


class PostgresConnection(DatabaseConnection):
    def __init__(self, database_url: str):
        self.database_url = database_url

    def get_engine(self):
        return create_engine(self.database_url)

    def get_sessionmaker(self):
        return sessionmaker(bind=self.get_engine(), expire_on_commit=False, autoflush=False)
    

def get_database_connection(database_url: str, db_type: str) -> DatabaseConnection:
    if db_type == "postgres":
        return PostgresConnection(database_url)
    else:
        raise ValueError(f"Unsupported database type: {db_type}")

    
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

logger.info(f'Database URL: {settings.database_url}')

db_type = "postgres"
db_connection = get_database_connection(settings.database_url, db_type)
    
engine = db_connection.get_engine()
SessionLocal = db_connection.get_sessionmaker()

logger.info(f"Connected to {db_type} database at {settings.database_url}")