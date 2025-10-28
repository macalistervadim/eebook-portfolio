import datetime
import uuid
from decimal import Decimal

from src.domain.enums import TransactionType
from src.domain.exceptions import (
    InsufficientHoldingsError,
    InvalidPortfolioOperationError,
    InvalidTransactionDataError,
    TransactionMismatchError,
)


class Holding:
    """Позиция по финансовому активу в портфеле.

    Представляет совокупность единиц одного актива (акции, облигации и т.д.),
    приобретённых в разное время, но объединённых в одну запись
    с усреднённой стоимостью покупки.

    Attributes:
        asset_id (str): уникальный идентификатор актива (например, "MOEX:SBER" или ISIN).
        quantity (Decimal): текущее количество единиц актива в портфеле.
        average_cost (Decimal): средняя цена покупки одной единицы в валюте портфеля.

    Note:
        Объект является частью агрегата Portfolio и не должен создаваться
        или изменяться напрямую извне.

    """

    __slots__ = ('asset_id', 'quantity', 'average_cost')

    def __init__(self, asset_id: str, quantity: Decimal, average_cost: Decimal) -> None:
        if quantity < 0:
            raise InvalidTransactionDataError('Количество актива не может быть отрицательным')
        if average_cost < 0:
            raise InvalidTransactionDataError('Средняя стоимость не может быть отрицательной')

        self.asset_id = asset_id
        self.quantity = quantity
        self.average_cost = average_cost

    def __repr__(self) -> str:
        return (
            f"Holding(asset_id='{self.asset_id}', "
            f'quantity={self.quantity}, '
            f'average_cost={self.average_cost})'
        )


class Transaction:
    """Финансовая операция — зафиксированный факт взаимодействия с активом.

    Является командой для агрегата Portfolio и не входит в его состав.
    Примеры: покупка акций, продажа облигаций, получение дивидендов.

    Attributes:
        id (UUID): уникальный идентификатор транзакции (генерируется автоматически).
        portfolio_id (UUID): идентификатор портфеля, к которому относится операция.
        asset_id (str): идентификатор актива (например, "NASDAQ:AAPL").
        type (TransactionType): тип операции (BUY, SELL, DIVIDEND и др.).
        quantity (Decimal): количество единиц актива.
        price_per_unit (Decimal): цена за единицу в валюте операции.
        total_amount (Decimal): общая сумма операции.
        executed_at (datetime): дата и время исполнения.
        currency (str): валюта операции (например, "USD", "RUB").

    Note:
        После применения транзакции к Portfolio она сохраняется отдельно
        как неизменяемый факт для аудита и расчётов.

    """

    __slots__ = (
        'id',
        'portfolio_id',
        'asset_id',
        'type',
        'quantity',
        'price_per_unit',
        'total_amount',
        'executed_at',
        'currency',
    )

    def __init__(
        self,
        portfolio_id: uuid.UUID,
        asset_id: str,
        transaction_type: TransactionType,
        quantity: Decimal,
        price_per_unit: Decimal,
        total_amount: Decimal,
        executed_at: datetime.datetime,
        currency: str,
    ) -> None:
        if quantity <= 0:
            raise InvalidTransactionDataError('Количество в транзакции должно быть положительным')
        if price_per_unit < 0:
            raise InvalidTransactionDataError('Цена за единицу не может быть отрицательной')
        if total_amount < 0:
            raise InvalidTransactionDataError('Общая сумма не может быть отрицательной')

        self.id = uuid.uuid4()
        self.portfolio_id = portfolio_id
        self.asset_id = asset_id
        self.type = transaction_type
        self.quantity = quantity
        self.price_per_unit = price_per_unit
        self.total_amount = total_amount
        self.executed_at = executed_at
        self.currency = currency

    def __repr__(self) -> str:
        return (
            f"Transaction(id={self.id}, type={self.type.name}, asset='{self.asset_id}', "
            f'qty={self.quantity}, price={self.price_per_unit})'
        )


class Portfolio:
    """Агрегат-корень инвестиционного портфеля.

    Управляет всеми операциями с активами и гарантирует соблюдение бизнес-правил:

    - корректность средней стоимости,
    - невозможность продажи без достаточного объёма,
    - целостность состава позиций.

    Все изменения состояния должны происходить **только** через метод `execute_transaction`.

    Attributes:
        id (UUID): уникальный идентификатор портфеля.
        user_id (UUID): владелец портфеля.
        name (str): название портфеля (например, "Пенсионный", "Технологии").
        currency (str): базовая валюта портфеля (все расчёты приводятся к ней).
        created_at (datetime): дата создания.
        holdings (List[Holding]): текущие позиции по активам.

    Example:
        portfolio = Portfolio(user_id, "Рост", "RUB")
        tx = Transaction(...)
        portfolio.execute_transaction(tx)

    """

    __slots__ = ('id', 'user_id', 'name', 'currency', 'created_at', 'holdings')

    def __init__(
        self,
        user_id: uuid.UUID,
        name: str,
        currency: str,
        portfolio_id: uuid.UUID | None = None,
        created_at: datetime.datetime | None = None,
        holdings: list[Holding] | None = None,
    ) -> None:
        self.id = portfolio_id or uuid.uuid4()
        self.user_id = user_id
        self.name = name.strip()
        self.currency = currency
        self.created_at = created_at or datetime.datetime.now(datetime.UTC)
        self.holdings = holdings or []

    def get_holding(self, asset_id: str) -> Holding | None:
        """Возвращает существующую позицию по активу или None, если её нет."""
        return next((h for h in self.holdings if h.asset_id == asset_id), None)

    def execute_transaction(self, transaction: 'Transaction') -> None:
        """Применяет финансовую операцию к портфелю и обновляет его состояние.

        Поддерживаемые типы транзакций:

        - BUY: увеличивает позицию, пересчитывает среднюю стоимость.
        - SELL: уменьшает позицию; при обнулении — удаляет запись.
        - DIVIDEND: фиксируется как факт, но не влияет на состав портфеля.

        Raises:
            TransactionMismatchError: если transaction.portfolio_id != self.id.
            InsufficientHoldingsError: при попытке продать больше, чем есть.
            InvalidPortfolioOperationError: при других нарушениях бизнес-логики.

        Note:
            После успешного выполнения рекомендуется сохранить транзакцию
            в отдельном хранилище для аудита.

        """
        if transaction.portfolio_id != self.id:
            raise TransactionMismatchError(
                f'Транзакция {transaction.id} относится к портфелю {transaction.portfolio_id}, '
                f'но применена к портфелю {self.id}',
            )

        if transaction.type == TransactionType.BUY:
            self._handle_buy(transaction)
        elif transaction.type == TransactionType.SELL:
            self._handle_sell(transaction)
        elif transaction.type == TransactionType.DIVIDEND:
            # Дивиденды не изменяют состав портфеля — только фиксируются как факт.
            # Подробный анализ — в сервисе metrics.
            pass
        else:
            raise InvalidPortfolioOperationError(
                f'Неподдерживаемый тип транзакции: {transaction.type.name}',
            )

    def _handle_buy(self, transaction: 'Transaction') -> None:
        """Обрабатывает покупку актива."""
        holding = self.get_holding(transaction.asset_id)
        if holding is None:
            self.holdings.append(
                Holding(
                    asset_id=transaction.asset_id,
                    quantity=transaction.quantity,
                    average_cost=transaction.price_per_unit,
                ),
            )
        else:
            total_cost = (
                holding.quantity * holding.average_cost
                + transaction.quantity * transaction.price_per_unit
            )
            total_quantity = holding.quantity + transaction.quantity
            holding.average_cost = total_cost / total_quantity
            holding.quantity = total_quantity

    def _handle_sell(self, transaction: 'Transaction') -> None:
        """Обрабатывает продажу актива."""
        holding = self.get_holding(transaction.asset_id)
        if holding is None:
            raise InsufficientHoldingsError(
                asset_id=transaction.asset_id,
                requested=float(transaction.quantity),
                available=0.0,
            )
        if holding.quantity < transaction.quantity:
            raise InsufficientHoldingsError(
                asset_id=transaction.asset_id,
                requested=float(transaction.quantity),
                available=float(holding.quantity),
            )

        holding.quantity -= transaction.quantity
        if holding.quantity == 0:
            self.holdings.remove(holding)

    def __repr__(self) -> str:
        return f"Portfolio(id={self.id}, name='{self.name}', holdings={len(self.holdings)} assets)"
