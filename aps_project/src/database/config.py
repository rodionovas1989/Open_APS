"""
Конфигурация подключения к базе данных
"""
import os
from pydantic_settings import BaseSettings


class DatabaseSettings(BaseSettings):
    """Настройки подключения к БД"""
    
    # Тип БД: sqlite, postgresql, mysql
    DB_TYPE: str = "sqlite"
    
    # Для SQLite
    SQLITE_DB_PATH: str = "aps_database.db"
    
    # Для PostgreSQL/MySQL
    DB_HOST: str = "localhost"
    DB_PORT: int = 5432
    DB_NAME: str = "aps_db"
    DB_USER: str = "postgres"
    DB_PASSWORD: str = "postgres"
    
    @property
    def database_url(self) -> str:
        """Формирует URL подключения к БД"""
        if self.DB_TYPE == "sqlite":
            return f"sqlite:///{self.SQLITE_DB_PATH}"
        elif self.DB_TYPE == "postgresql":
            return f"postgresql://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        elif self.DB_TYPE == "mysql":
            return f"mysql+pymysql://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        else:
            raise ValueError(f"Неподдерживаемый тип БД: {self.DB_TYPE}")
    
    @property
    def async_database_url(self) -> str:
        """Формирует асинхронный URL подключения к БД"""
        if self.DB_TYPE == "sqlite":
            return f"sqlite+aiosqlite:///{self.SQLITE_DB_PATH}"
        elif self.DB_TYPE == "postgresql":
            return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        elif self.DB_TYPE == "mysql":
            return f"mysql+aiomysql://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        else:
            raise ValueError(f"Неподдерживаемый тип БД: {self.DB_TYPE}")
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


# Глобальный экземпляр настроек
db_settings = DatabaseSettings()
