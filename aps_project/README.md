# Advanced Planning and Scheduling (APS) System

## Структура проекта

```
aps_project/
├── src/                      # Основной исходный код
│   ├── __init__.py
│   ├── core/                 # Ядро системы APS
│   │   └── __init__.py
│   ├── schedulers/           # Планировщики и алгоритмы планирования
│   │   └── __init__.py
│   ├── optimizers/           # Оптимизаторы и решатели задач
│   │   └── __init__.py
│   ├── integrations/         # Интеграции с внешними системами (ERP, MES)
│   │   └── __init__.py
│   └── models/               # Модели данных (производство, ресурсы, заказы)
│       └── __init__.py
├── api/                      # REST API слой
│   ├── __init__.py
│   ├── routes/               # Маршруты API
│   │   └── __init__.py
│   └── schemas/              # Pydantic схемы для валидации данных
│       └── __init__.py
├── web/                      # Веб-интерфейс
│   ├── static/               # Статические файлы
│   │   ├── css/              # Стили
│   │   └── js/               # JavaScript
│   └── templates/            # HTML шаблоны
├── config/                   # Конфигурация приложения
│   └── __init__.py
├── tests/                    # Тесты
│   ├── __init__.py
│   ├── unit/                 # Юнит-тесты
│   │   └── __init__.py
│   └── integration/          # Интеграционные тесты
│       └── __init__.py
├── scripts/                  # Скрипты для развертывания и утилиты
├── docs/                     # Документация
├── requirements.txt          # Зависимости Python
├── .gitignore
└── README.md
```

## Описание компонентов

### Core (src/core/)
- Основной движок APS
- Управление состоянием системы
- Координация между планировщиками и оптимизаторами

### Schedulers (src/schedulers/)
- Алгоритмы планирования производства
- Дискретное планирование
- Планирование с ограничениями

### Optimizers (src/optimizers/)
- Математические оптимизаторы
- Генетические алгоритмы
- Линейное программирование

### Integrations (src/integrations/)
- Коннекторы к ERP системам
- Интеграция с MES
- Импорт/экспорт данных

### Models (src/models/)
- Модели производственных ресурсов
- Модели заказов и операций
- Модели ограничений

### API (api/)
- RESTful API для взаимодействия с системой
- Endpoints для управления планированием
- Схемы данных для валидации

### Web (web/)
- Веб-интерфейс пользователя
- Дашборды и визуализация планов
- Интерактивные Gantt диаграммы

## Технологии

- **Backend**: Python 3.9+
- **Web Framework**: FastAPI / Flask
- **Database**: PostgreSQL / SQLite
- **ORM**: SQLAlchemy
- **Validation**: Pydantic
- **Frontend**: HTML/CSS/JavaScript (возможно React/Vue.js)
- **Testing**: pytest

## Быстрый старт

```bash
cd aps_project
pip install -r requirements.txt
python -m src.main
```

## Лицензия

MIT
