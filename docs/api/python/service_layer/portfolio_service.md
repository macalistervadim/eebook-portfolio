# Сервис управления портфелями

Сервис `PortfolioService` предоставляет бизнес-логику для работы с инвестиционными портфелями пользователей.

## Обзор

Сервис реализует следующие возможности:

- Создание и управление портфелями
- Работа с транзакциями активов
- Валидация бизнес-правил
- Интеграция с пользовательским сервисом

## Интерфейсы

### ABCPortfolioService

Абстрактный базовый класс, определяющий контракт для работы с портфелями.

::: src.service_layer.portfolio_service.ABCPortfolioService
    :docstring:
    :members: add get_by_id get_by_user_id update delete add_transaction

## Реализация

### PortfolioService

Основная реализация сервиса портфелей.

::: src.service_layer.portfolio_service.PortfolioService
    :docstring:
    :members: __init__

## Бизнес-логика

### Создание портфеля

1. Проверяет существование пользователя
2. Создаёт новый портфель
3. Возвращает результат операции

### Управление транзакциями

- Добавление операций купли/продажи активов
- Валидация доступных средств
- Обновление средней цены актива

### Валидация

- Проверка прав доступа
- Валидация валютных операций
- Проверка достаточности средств

## Примеры использования

```python
from uuid import UUID
from src.domain.domain import Portfolio, Transaction
from src.service_layer.portfolio_service import PortfolioService

# Инициализация сервиса
portfolio_service = PortfolioService(repo, user_service)

# Создание портфеля
portfolio = Portfolio(
    user_id=UUID("..."),
    name="Мой портфель",
    currency="USD"
)
await portfolio_service.add(portfolio)

# Добавление транзакции
transaction = Transaction(
    portfolio_id=portfolio.id,
    asset_id="AAPL",
    transaction_type="BUY",
    quantity=10,
    price_per_unit=150.50,
    total_amount=1505.00
)
await portfolio_service.add_transaction(transaction)
```

## Обработка ошибок

Сервис может генерировать следующие исключения:

- `ValueError` - при попытке создать портфель для несуществующего пользователя
- `InsufficientFundsError` - при недостатке средств для операции
- `ValidationError` - при нарушении бизнес-правил

## Кэширование

Для повышения производительности рекомендуется использовать кэширование:

- Часто запрашиваемых портфелей
- Текущих котировок активов
- Результатов расчётов

## Рекомендации по использованию

1. **Транзакционность**
   Используйте Unit of Work для обеспечения атомарности операций:
   ```python
   async with uow:
       await portfolio_service.add(portfolio)
       await uow.commit()
   ```

2. **Валидация**
   - Проверяйте входные данные перед передачей в сервис
   - Обрабатывайте исключения на уровне API

3. **Производительность**
   - Используйте пагинацию для больших списков
   - Применяйте select_related для связанных сущностей

## Связанные компоненты

- [Репозиторий портфеля](../../adapters/repository.md)
- [Сервис пользователей](./users_service.md)
- [Unit of Work](./uow.md)
- [Доменные модели](../../domain/domain.md)
