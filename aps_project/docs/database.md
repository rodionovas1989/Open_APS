# База данных APS

## Настройки подключения

По умолчанию используется SQLite для разработки. Для переключения на PostgreSQL или MySQL измените переменные окружения в файле `.env`.

### Переменные окружения

```env
# Тип БД: sqlite, postgresql, mysql
DB_TYPE=sqlite

# Для SQLite
SQLITE_DB_PATH=aps_database.db

# Для PostgreSQL/MySQL (раскомментировать при использовании)
# DB_HOST=localhost
# DB_PORT=5432
# DB_NAME=aps_db
# DB_USER=postgres
# DB_PASSWORD=postgres
```

## Структура базы данных

База данных APS содержит 18 таблиц, организованных по следующим категориям:

### 1. Предприятия (Enterprise)
- **enterprises** - Предприятия/Компании
- **work_centers** - Рабочие центры (производственные единицы)

### 2. Ресурсы (Resources)
- **resources** - Ресурсы (оборудование, персонал, инструменты)
- **calendars** - Производственные календари
- **calendar_exceptions** - Исключения из календаря (праздники, простои)
- **working_periods** - Периоды работы в календаре

### 3. Продукты (Products)
- **products** - Продукты/Изделия
- **bill_of_materials** - Спецификации изделий (BOM)
- **routings** - Маршрутные карты
- **routing_operations** - Операции в маршрутных картах

### 4. Заказы (Orders)
- **orders** - Заказы на производство
- **order_items** - Позиции заказов
- **operations** - Производственные операции
- **operation_resources** - Назначение ресурсов на операции

### 5. Склады (Warehouses)
- **warehouses** - Склады
- **inventory** - Запасы материалов/продуктов

### 6. Планирование (Planning)
- **production_plans** - Производственные планы
- **planned_operations** - Запланированные операции

## Инициализация базы данных

Для создания всех таблиц выполните:

```bash
python -m scripts.init_db
```

## Подключение к БД в коде

```python
from src.database import get_db, AsyncSessionLocal
from sqlalchemy.ext.asyncio import AsyncSession

# Использование зависимости FastAPI
async def my_endpoint(db: AsyncSession = Depends(get_db)):
    # Работа с БД
    pass

# Или прямое создание сессии
async with AsyncSessionLocal() as session:
    # Работа с сессией
    pass
```

## Модели данных

Все модели определены в `src/models/metadata.py` и включают:

- **Enums**: OrderStatus, OperationStatus, ResourceType
- Полную систему связей между таблицами
- Индексы для оптимизации запросов
- Временные метки created_at/updated_at
- Каскадное удаление связанных записей

## Переход на PostgreSQL/MySQL

1. Установите дополнительные зависимости:
```bash
pip install asyncpg        # для PostgreSQL
# или
pip install aiomysql       # для MySQL
```

2. Измените `.env`:
```env
DB_TYPE=postgresql
DB_HOST=localhost
DB_PORT=5432
DB_NAME=aps_db
DB_USER=postgres
DB_PASSWORD=your_password
```

3. Перезапустите приложение
