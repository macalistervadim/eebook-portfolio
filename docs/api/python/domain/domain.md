# Доменный слой портфолио

## Обзор

Доменный слой представляет собой ядро приложения, содержащее бизнес-логику и правила работы с инвестиционным портфелем. Этот слой не зависит от внешних систем и фреймворков, что делает его изолированным и легко тестируемым.

## Основные концепции

### 1. Агрегаты

Агрегаты — это основные строительные блоки домена, которые обеспечивают целостность данных и инкапсулируют бизнес-правила.

#### 1.1. Портфель (Portfolio)

Центральный агрегат, представляющий инвестиционный портфель пользователя.

::: src.domain.domain.Portfolio
    options:
      show_source: true
      show_signature_annotations: true
      show_docstring: true
      show_bases: true
      show_root_heading: false
      show_root_toc_entry: false

### 2. Сущности

#### 2.1. Транзакция (Transaction)

Представляет финансовую операцию с активом.

::: src.domain.domain.Transaction
    options:
      show_source: true
      show_signature_annotations: true
      show_docstring: true
      show_bases: true
      show_root_heading: false
      show_root_toc_entry: false

#### 2.2. Позиция (Holding)

Представляет текущую позицию по активу в портфеле.

::: src.domain.domain.Holding
    options:
      show_source: true
      show_signature_annotations: true
      show_docstring: true
      show_bases: true
      show_root_heading: false
      show_root_toc_entry: false

## Бизнес-правила

### Обработка транзакций

Все изменения состояния портфеля происходят через метод `execute_transaction`, который гарантирует соблюдение бизнес-правил:

1. **Покупка актива (BUY)**

   - Создаёт новую или обновляет существующую позицию
   - Пересчитывает среднюю стоимость актива
   - Увеличивает общее количество активов

2. **Продажа актива (SELL)**

   - Проверяет достаточность количества активов
   - Уменьшает количество активов в позиции
   - Удаляет позицию при достижении нуля

3. **Дивиденды (DIVIDEND)**
   - Фиксируются как факт
   - Не влияют на состав портфеля

### Валидация

Все операции валидируются на соответствие бизнес-правилам:

- Количество активов не может быть отрицательным
- Цена за единицу не может быть отрицательной
- Невозможно продать больше активов, чем есть в портфеле
- Транзакция должна относиться к тому же портфелю, к которому применяется

## Примеры использования

### Создание портфеля

```python
user_id = uuid.uuid4()
portfolio = Portfolio(
    user_id=user_id,
    name="Мой первый портфель",
    currency="RUB"
)
```

### Выполнение транзакции

```python
try:
    transaction = Transaction(
        portfolio_id=portfolio.id,
        asset_id="MOEX:SBER",
        transaction_type=TransactionType.BUY,
        quantity=Decimal("10"),
        price_per_unit=Decimal("250.50"),
        total_amount=Decimal("2505.00"),
        executed_at=datetime.utcnow(),
        currency="RUB"
    )
    
    portfolio.execute_transaction(transaction)
except InvalidTransactionDataError as e:
    print(f"Ошибка выполнения транзакции: {e}")
```

## Исключения

Доменный слой использует специализированные исключения для обработки ошибок бизнес-логики:

::: src.domain.exceptions
    options:
      show_source: true
      show_signature_annotations: true
      show_docstring: true
      show_bases: true
      show_root_heading: false
      show_root_toc_entry: false
