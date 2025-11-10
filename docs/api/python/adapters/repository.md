# Репозиторий портфеля

Модуль `repository` предоставляет реализацию паттерна Repository для работы с данными портфеля, используя SQLAlchemy в качестве ORM.

## Обзор

Модуль содержит:

- Абстрактный класс `AbstractPortfolioRepository` с определением интерфейса
- Конкретную реализацию `SqlAlchemyPortfolioRepository` для работы с PostgreSQL

## AbstractPortfolioRepository

Базовый абстрактный класс, определяющий контракт для работы с хранилищем портфелей.

::: src.adapters.repository.AbstractPortfolioRepository
    :docstring:
    :members: add get_by_id get_by_user_id update delete add_transaction

## SqlAlchemyPortfolioRepository

Реализация репозитория для работы с PostgreSQL через SQLAlchemy.

::: src.adapters.repository.SqlAlchemyPortfolioRepository
    :docstring:
    :members: __init__

## Детали реализации

### Работа с портфелями

- **Добавление портфеля**
  - Создаёт запись о портфеле
  - Сохраняет все связанные активы

- **Получение портфеля**
  - Поддерживает поиск по ID портфеля и ID пользователя
  - Возвращает агрегат `Portfolio` с вложенными сущностями

- **Обновление портфеля**
  - Атомарно обновляет данные портфеля
  - Удаляет и заново создаёт связанные активы

### Работа с транзакциями

- **Добавление транзакции**
  - Сохраняет историю операций с активами
  - Поддерживает различные типы транзакций

## Пример использования

```python
from uuid import UUID
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from src.adapters.factory import SQLAlchemyPortfolioRepositoryFactory
from src.domain.domain import Portfolio, Holding

# Инициализация
engine = create_async_engine("postgresql+asyncpg://user:password@localhost/db")
async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

# Создание репозитория
async with async_session() as session:
    factory = SQLAlchemyPortfolioRepositoryFactory()
    repo = factory.create(session)
    
    # Создание портфеля
    portfolio = Portfolio(
        user_id=UUID("..."),
        name="Мой портфель",
        currency="USD",
        holdings=[
            Holding(asset_id="AAPL", quantity=10, average_cost=150.5)
        ]
    )
    await repo.add(portfolio)
    
    # Получение портфеля
    portfolio = await repo.get_by_id(portfolio.id)
```

## Особенности реализации

- **Атомарность операций**
  - Все изменения в рамках одной сессии
  - Явное управление транзакциями

- **Производительность**
  - Пакетная вставка данных
  - Эффективные запросы с JOIN

- **Безопасность**
  - Валидация на уровне доменной модели
  - Обработка конкурентного доступа

## Ограничения

- Требуется активная асинхронная сессия SQLAlchemy
- Нет встроенной пагинации для больших выборок
- Оптимизировано под реляционную модель данных

## Связанные компоненты

- [Фабрика репозиториев](./factory.md)
- [ORM-модели](./orm.md)
- [Доменные модели](../domain/domain.md)
