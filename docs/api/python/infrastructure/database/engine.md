# Движок базы данных

Модуль `engine` предоставляет функционал для работы с асинхронным подключением к базе данных с использованием SQLAlchemy.

## Особенности

- Ленивая инициализация движка БД
- Управление пулом соединений
- Обработка ошибок подключения
- Кэширование фабрики сессий
- Асинхронный API

## Документация API

### get_engine

Фабричная функция для создания и кэширования асинхронного движка SQLAlchemy.

::: src.infrastructure.database.engine.get_engine
    options:
      show_source: true
      show_signature_annotations: true
      show_docstring: true
      show_bases: true
      show_root_heading: false
      show_root_toc_entry: false

### get_session_factory

Фабрика для создания асинхронных сессий с настройками по умолчанию.

::: src.infrastructure.database.engine.get_session_factory
    options:
      show_source: true
      show_signature_annotations: true
      show_docstring: true
      show_bases: true
      show_root_heading: false
      show_root_toc_entry: false

## Примеры использования

### Получение движка и создание сессии

```python
from src.infrastructure.database.engine import get_engine, get_session_factory

# Получение движка (кэшируется при первом вызове)
engine = get_engine()

# Получение фабрики сессий (кэшируется при первом вызове)
session_factory = get_session_factory()

# Создание сессии
async with session_factory() as session:
    # Работа с базой данных
    result = await session.execute("SELECT 1")
    print(await result.scalar())
```
