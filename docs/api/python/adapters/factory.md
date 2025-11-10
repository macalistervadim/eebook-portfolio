# Фабрика репозиториев портфеля

Модуль `factory` предоставляет абстракции для создания репозиториев портфеля, следуя принципам DDD и паттерну "Абстрактная фабрика".

## Обзор

Модуль содержит:

- Абстрактную фабрику `ABCPortfolioRepositoryFactory`
- Её реализацию `SQLAlchemyPortfolioRepositoryFactory`

## ABCPortfolioRepositoryFactory

Базовый абстрактный класс, определяющий интерфейс для создания репозиториев портфеля.

::: src.adapters.factory.ABCPortfolioRepositoryFactory
    :docstring:
    :members: create

## SQLAlchemyPortfolioRepositoryFactory

Конкретная реализация фабрики, создающая экземпляры `SqlAlchemyPortfolioRepository`.

::: src.adapters.factory.SQLAlchemyPortfolioRepositoryFactory
    :docstring:
    :members: create

## Пример использования

```python
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from src.adapters.factory import SQLAlchemyPortfolioRepositoryFactory

# Инициализация сессии
engine = create_async_engine("postgresql+asyncpg://user:password@localhost/db")
async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

# Создание фабрики
factory = SQLAlchemyPortfolioRepositoryFactory()

# Получение репозитория
async with async_session() as session:
    repository = factory.create(session)
    # Использование репозитория...
```

## Детали реализации

- Фабрика инкапсулирует логику создания репозиториев
- Позволяет легко заменить реализацию репозитория
- Поддерживает асинхронную работу с БД через SQLAlchemy

## Примечания

- Для работы с репозиторием требуется активная асинхронная сессия SQLAlchemy
- Фабрика не управляет жизненным циклом сессии
- Рекомендуется использовать фабрику в рамках единицы работы (Unit of Work)

## Связанные компоненты

- [Репозиторий портфеля](./repository.md)
- [Интерфейсы адаптеров](./interfaces.md)
- [ORM-модели](./orm.md)
