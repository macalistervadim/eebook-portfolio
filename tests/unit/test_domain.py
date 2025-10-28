import datetime
import uuid

import pytest
from decimal import Decimal

from src.domain.domain import Portfolio, Holding, Transaction
from src.domain.enums import TransactionType
from src.domain.exceptions import (
    InsufficientHoldingsError,
    TransactionMismatchError,
    InvalidTransactionDataError,
)


def create_transaction(
    portfolio: Portfolio,
    asset_id: str,
    tx_type: TransactionType,
    qty: str,
    price: str,
    currency: str = 'USD',
):
    """Вспомогательная функция для создания транзакции, привязанной к портфелю."""
    total = Decimal(qty) * Decimal(price)
    return Transaction(
        portfolio_id=portfolio.id,
        asset_id=asset_id,
        transaction_type=tx_type,
        quantity=Decimal(qty),
        price_per_unit=Decimal(price),
        total_amount=total,
        executed_at=datetime.datetime.now(),
        currency=currency,
    )


def test_holding_negative_quantity_raises():
    with pytest.raises(
        InvalidTransactionDataError, match='Количество актива не может быть отрицательным'
    ):
        Holding(asset_id='TEST', quantity=Decimal('-1'), average_cost=Decimal('10'))


def test_holding_negative_avg_cost_raises():
    with pytest.raises(
        InvalidTransactionDataError, match='Средняя стоимость не может быть отрицательной'
    ):
        Holding(asset_id='TEST', quantity=Decimal('1'), average_cost=Decimal('-1'))


def test_transaction_zero_quantity_raises():
    with pytest.raises(
        InvalidTransactionDataError, match='Количество в транзакции должно быть положительным'
    ):
        Transaction(
            portfolio_id=uuid.uuid4(),
            asset_id='TEST',
            transaction_type=TransactionType.BUY,
            quantity=Decimal('0'),
            price_per_unit=Decimal('10'),
            total_amount=Decimal('0'),
            executed_at=datetime.datetime.now(),
            currency='USD',
        )


def create_transaction(
    portfolio: Portfolio,
    asset_id: str,
    tx_type: TransactionType,
    qty: str,
    price: str,
    currency: str = 'USD',
):
    """Вспомогательная функция для создания транзакции, привязанной к портфелю."""
    total = Decimal(qty) * Decimal(price)
    return Transaction(
        portfolio_id=portfolio.id,
        asset_id=asset_id,
        transaction_type=tx_type,
        quantity=Decimal(qty),
        price_per_unit=Decimal(price),
        total_amount=total,
        executed_at=datetime.datetime.now(),
        currency=currency,
    )


class TestPortfolioModel:
    def test_empty_portfolio_has_no_holdings(self, empty_portfolio):
        assert empty_portfolio.holdings == []

    def test_portfolio_with_holding(self, portfolio_with_sber, sber_holding):
        assert len(portfolio_with_sber.holdings) == 1
        assert portfolio_with_sber.get_holding('MOEX:SBER') == sber_holding

    def test_buy_new_asset_creates_holding(self, empty_portfolio):
        tx = create_transaction(
            empty_portfolio, 'NASDAQ:AAPL', TransactionType.BUY, '10.0', '150.0'
        )
        empty_portfolio.execute_transaction(tx)
        holding = empty_portfolio.get_holding('NASDAQ:AAPL')
        assert holding is not None
        assert holding.quantity == Decimal('10.0')
        assert holding.average_cost == Decimal('150.0')

    def test_buy_existing_asset_updates_average_cost(self, portfolio_with_sber):
        tx = create_transaction(
            portfolio_with_sber, 'MOEX:SBER', TransactionType.BUY, '100.0', '300.0'
        )
        portfolio_with_sber.execute_transaction(tx)

        updated = portfolio_with_sber.get_holding('MOEX:SBER')
        expected_total_cost = Decimal('280.2') * Decimal('281.43') + Decimal('100.0') * Decimal(
            '300.0'
        )
        expected_qty = Decimal('380.2')
        expected_avg = expected_total_cost / expected_qty

        assert updated.quantity == expected_qty
        assert updated.average_cost == expected_avg

    def test_sell_existing_asset_reduces_quantity(self, portfolio_with_sber):
        tx = create_transaction(
            portfolio_with_sber, 'MOEX:SBER', TransactionType.SELL, '80.2', '300.0'
        )
        portfolio_with_sber.execute_transaction(tx)
        holding = portfolio_with_sber.get_holding('MOEX:SBER')
        assert holding.quantity == Decimal('200.0')  # 280.2 - 80.2 = 200

    def test_sell_entire_holding_removes_it(self, portfolio_with_sber):
        tx = create_transaction(
            portfolio_with_sber, 'MOEX:SBER', TransactionType.SELL, '280.2', '300.0'
        )
        portfolio_with_sber.execute_transaction(tx)
        assert portfolio_with_sber.get_holding('MOEX:SBER') is None
        assert len(portfolio_with_sber.holdings) == 0

    def test_sell_nonexistent_asset_raises(self, empty_portfolio):
        tx = create_transaction(
            empty_portfolio, 'NASDAQ:AAPL', TransactionType.SELL, '5.0', '160.0'
        )
        with pytest.raises(InsufficientHoldingsError):
            empty_portfolio.execute_transaction(tx)

    def test_sell_more_than_available_raises(self, portfolio_with_sber):
        tx = create_transaction(
            portfolio_with_sber, 'MOEX:SBER', TransactionType.SELL, '300.0', '300.0'
        )
        with pytest.raises(InsufficientHoldingsError):
            portfolio_with_sber.execute_transaction(tx)

    def test_dividend_transaction_does_not_change_holdings(self, portfolio_with_sber):
        tx = create_transaction(
            portfolio_with_sber, 'MOEX:SBER', TransactionType.DIVIDEND, '1.0', '10.0', 'RUB'
        )
        initial_qty = portfolio_with_sber.get_holding('MOEX:SBER').quantity
        portfolio_with_sber.execute_transaction(tx)
        assert portfolio_with_sber.get_holding('MOEX:SBER').quantity == initial_qty

    def test_transaction_with_wrong_portfolio_id_raises(self, empty_portfolio):
        tx = create_transaction(empty_portfolio, 'TEST', TransactionType.BUY, '1.0', '10.0')
        tx.portfolio_id = uuid.uuid4()  # подменяем на чужой ID
        with pytest.raises(TransactionMismatchError):
            empty_portfolio.execute_transaction(tx)

    def test_sell_after_buy_same_asset(self, empty_portfolio):
        buy_tx = create_transaction(
            empty_portfolio, 'NASDAQ:AAPL', TransactionType.BUY, '10.0', '150.0'
        )
        sell_tx = create_transaction(
            empty_portfolio, 'NASDAQ:AAPL', TransactionType.SELL, '5.0', '160.0'
        )

        empty_portfolio.execute_transaction(buy_tx)
        assert empty_portfolio.get_holding('NASDAQ:AAPL').quantity == Decimal('10.0')

        empty_portfolio.execute_transaction(sell_tx)
        assert empty_portfolio.get_holding('NASDAQ:AAPL').quantity == Decimal('5.0')
