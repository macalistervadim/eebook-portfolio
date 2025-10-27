class PortfolioDomainError(Exception):
    """Базовое исключение для ошибок в домене портфеля."""

    pass


class InvalidPortfolioOperationError(PortfolioDomainError):
    """Операция над портфелем невозможна из-за нарушения бизнес-правил."""

    def __init__(self, message: str, asset_id: str | None = None):
        self.asset_id = asset_id
        super().__init__(message)


class InsufficientHoldingsError(InvalidPortfolioOperationError):
    """Недостаточно акций для выполнения операции продажи."""

    def __init__(self, asset_id: str, requested: float, available: float):
        message = (
            f"Недостаточно акций для продажи актива '{asset_id}'. "
            f'Запрошено: {requested}, доступно: {available}'
        )
        super().__init__(message, asset_id=asset_id)
        self.requested = requested
        self.available = available


class TransactionMismatchError(PortfolioDomainError):
    """Транзакция не принадлежит указанному портфелю."""

    pass


class InvalidTransactionDataError(PortfolioDomainError):
    """Некорректные данные в транзакции (отрицательная цена, нулевое количество и т.д.)."""

    pass
