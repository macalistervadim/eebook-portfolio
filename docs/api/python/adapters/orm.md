# ORM-модели портфеля

Модуль `orm` определяет структуру базы данных для управления портфелями, используя SQLAlchemy Core.

## Обзор схемы данных

Модуль содержит определения таблиц для хранения:

- Портфелей пользователей
- Активов в портфелях
- Транзакций по активам

## Основные таблицы

### Портфели (`portfolios`)

Хранит основные данные о портфелях пользователей.

::: src.adapters.orm.portfolio_table
    :docstring:
    :members:

### Активы (`holdings`)

Содержит информацию об активах в портфелях.

::: src.adapters.orm.holding_table
    :docstring:
    :members:

### Транзакции (`transactions`)

Записывает историю всех операций с активами.

::: src.adapters.orm.transaction_table
    :docstring:
    :members:

## Особенности реализации

- **Идентификаторы** - Используются UUID для уникальной идентификации записей
- **Индексация** - Оптимизированы запросы по часто используемым полям
- **Целостность данных** - Внешние ключи с каскадным удалением
- **Точность вычислений** - Высокая точность для финансовых операций (20 цифр, 10 знаков после запятой)

## Примеры использования

### Создание таблиц

```python
from sqlalchemy import create_engine
from src.adapters.orm import metadata

# Создание движка
engine = create_engine("postgresql://user:password@localhost/dbname")

# Создание всех таблиц
metadata.create_all(engine)
```

### Работа с транзакциями

```python
from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from src.adapters.orm import transaction_table

async def add_transaction(session: AsyncSession, transaction_data: dict):
    stmt = insert(transaction_table).values(transaction_data)
    await session.execute(stmt)
    await session.commit()
```

## Примечания по производительности

- Для ускорения запросов добавлены индексы на часто используемые поля
- Использование `ondelete='CASCADE'` для автоматического удаления связанных записей
- Рекомендуется использовать пулы соединений для продакшн-среды

## Связанные компоненты

- [Фабрика репозиториев](./factory.md)
- [Репозиторий портфеля](./repository.md)
- [Интерфейсы адаптеров](./interfaces.md)
