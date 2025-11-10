# Unit of Work (Единица работы)

Модуль `uow` реализует паттерн Unit of Work для управления транзакциями и координации операций с репозиториями.

## Обзор

Unit of Work (UoW) обеспечивает:

- Управление жизненным циклом транзакций
- Координацию работы репозиториев
- Автоматический откат изменений при ошибках
- Единую точку сохранения изменений

## Абстракции

### AbstractUnitOfWork

Базовый абстрактный класс, определяющий интерфейс Unit of Work.

::: src.service_layer.uow.AbstractUnitOfWork
    :docstring:
    :members: commit rollback

## Реализации

### SqlAlchemyUnitOfWork

Реализация UoW для работы с SQLAlchemy.

::: src.service_layer.uow.SqlAlchemyUnitOfWork
    :docstring:
    :members: __init__

## Принцип работы

### Жизненный цикл транзакции

```mermaid
sequenceDiagram
    participant Client
    participant UoW
    participant Session
    
    Client->>UoW: Создание UoW
    UoW->>Session: Создание сессии
    Client->>UoW: Работа с репозиториями
    alt Успешное выполнение
        Client->>UoW: commit()
        UoW->>Session: commit()
    else Ошибка
        UoW->>Session: rollback()
    end
    UoW->>Session: Закрытие сессии
```

## Пример использования

```python
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from src.service_layer.uow import SqlAlchemyUnitOfWork
from src.adapters.factory import SQLAlchemyPortfolioRepositoryFactory

# Настройка подключения
engine = create_async_engine("postgresql+asyncpg://user:pass@localhost/db")
session_factory = async_sessionmaker(engine, expire_on_commit=False)
repo_factory = SQLAlchemyPortfolioRepositoryFactory()

# Использование UoW
async with SqlAlchemyUnitOfWork(session_factory, repo_factory) as uow:
    # Работа с репозиториями через uow.portfolio
    portfolio = await uow.portfolio.get_by_id(portfolio_id)
    
    # Внесение изменений
    portfolio.name = "Обновлённый портфель"
    
    # Фиксация изменений
    await uow.commit()
```

## Особенности реализации

### Управление сессиями
- Каждый UoW создаёт новую сессию
- Сессия автоматически закрывается при выходе из контекста
- Поддержка вложенных транзакций

### Обработка ошибок
- Автоматический откат при возникновении исключения
- Возможность явного вызова rollback()
- Логирование ошибок транзакций

### Производительность
- Ленивая инициализация репозиториев
- Эффективное управление подключениями
- Поддержка пулинга соединений

## Рекомендации

1. **Область видимости**
   - Создавайте новый UoW для каждой бизнес-операции
   - Не передавайте UoW между запросами

2. **Обработка исключений**
   ```python
   try:
       async with uow:
           # ... операции с репозиториями
           await uow.commit()
   except Exception as e:
       logger.error(f"Ошибка при выполнении операции: {e}")
       raise
   ```

3. **Тестирование**
   - Используйте моки для изоляции тестов
   - Применяйте фикстуры для настройки UoW
   - Проверяйте откат транзакций

## Расширение функциональности

Для добавления новых репозиториев:

1. Добавьте атрибут в `AbstractUnitOfWork`
2. Реализуйте инициализацию в конкретной реализации UoW
3. Обновите документацию

## Связанные компоненты

- [Репозиторий портфеля](../../adapters/repository.md)
- [Фабрика репозиториев](../../adapters/factory.md)
- [Сервис портфеля](./portfolio_service.md)
