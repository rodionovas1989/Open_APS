"""
Модуль подключения к базе данных
"""
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase
from src.database.config import db_settings


# Создание асинхронного движка
engine = create_async_engine(
    db_settings.async_database_url,
    echo=True,  # Логирование SQL-запросов (отключить в production)
    pool_pre_ping=True,  # Проверка соединения перед использованием
)

# Фабрика сессий
AsyncSessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
)


# Базовый класс для моделей
class Base(DeclarativeBase):
    """Базовый класс для всех моделей данных"""
    pass


async def get_db() -> AsyncSession:
    """
    Зависимость FastAPI для получения сессии БД.
    Используется в эндпоинтах API.
    """
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


async def init_db():
    """
    Инициализация базы данных - создание всех таблиц.
    Вызывается при старте приложения.
    """
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def close_db():
    """
    Закрытие подключения к базе данных.
    Вызывается при остановке приложения.
    """
    await engine.dispose()
