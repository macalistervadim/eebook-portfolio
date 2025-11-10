# Модели данных

Модуль `models` содержит Pydantic-модели для валидации и сериализации данных, используемые в API и сервисном слое приложения.

## Обзор

Модуль включает модели для:

- Создания портфеля
- Обновления портфеля
- Добавления транзакции

## Модели

### CreatePortfolio

Модель для создания нового портфеля.

### UpdatePortfolio


Модель для обновления существующего портфеля.

### AddTransaction

Модель для добавления транзакции в портфель.


## Особенности валидации

1. **Типы данных**
   - `UUID` для идентификаторов
   - `Decimal` для финансовых величин
   - `datetime` для временных меток

2. **Встроенные валидаторы**
   - Проверка формата UUID
   - Валидация числовых значений
   - Проверка типов транзакций

## Примеры использования

### Создание портфеля

```python
from uuid import uuid4
from src.entity.models import CreatePortfolio

# Валидация при создании
portfolio_data = CreatePortfolio(
    user_id=uuid4(),
    name="Мой инвестиционный портфель",
    currency="USD"
)
```

### Добавление транзакции

```python
from decimal import Decimal
from datetime import datetime, timezone
from src.entity.models import AddTransaction
from src.domain.enums import TransactionType

transaction = AddTransaction(
    portfolio_id=uuid4(),
    asset_id="AAPL",
    transaction_type=TransactionType.BUY,
    quantity=Decimal("10"),
    price_per_unit=Decimal("150.50"),
    total_amount=Decimal("1505.00"),
    executed_at=datetime.now(timezone.utc),
    currency="USD"
)
```

## Ограничения

- Максимальная длина строковых полей не определена
- Нет валидации бизнес-правил (например, допустимые валюты)
- Отсутствует проверка связанных сущностей

## Рекомендации

1. **Для расширения валидации** можно использовать `@validator` декоратор Pydantic
2. **Для документирования полей** используйте `Field` с описанием
3. **Для работы с БД** преобразуйте в соответствующие модели

## Связанные компоненты

- [Доменные модели](../domain/domain.md)
- [Репозиторий портфеля](../adapters/repository.md)
- [Сервисный слой](../service_layer/services.md)
