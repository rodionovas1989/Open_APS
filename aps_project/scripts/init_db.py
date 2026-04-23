"""
Скрипт для инициализации базы данных и создания таблиц

Запуск:
    python -m scripts.init_db
"""

import asyncio
import sys
from pathlib import Path

# Добавляем корень проекта в путь
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.database.connection import init_db, engine
from src.database.config import db_settings


async def main():
    """Инициализация базы данных"""
    print("=" * 60)
    print("Инициализация базы данных APS")
    print("=" * 60)
    print(f"\nТип БД: {db_settings.DB_TYPE}")
    print(f"URL подключения: {db_settings.database_url}\n")
    
    try:
        print("Создание таблиц в базе данных...")
        await init_db()
        print("✓ Таблицы успешно созданы!\n")
        
        # Вывод списка созданных таблиц
        async with engine.begin() as conn:
            from sqlalchemy import text
            result = await conn.execute(text("""
                SELECT name FROM sqlite_master 
                WHERE type='table' AND name NOT LIKE 'sqlite_%'
                ORDER BY name
            """))
            tables = result.fetchall()
            
            print("Созданные таблицы:")
            print("-" * 40)
            for table in tables:
                print(f"  • {table[0]}")
            print("-" * 40)
            print(f"Всего таблиц: {len(tables)}\n")
        
        print("=" * 60)
        print("База данных готова к работе!")
        print("=" * 60)
        
    except Exception as e:
        print(f"✗ Ошибка при инициализации БД: {e}")
        raise


if __name__ == "__main__":
    asyncio.run(main())
