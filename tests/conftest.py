import uuid
from decimal import Decimal

import pytest

from src.domain.domain import Portfolio, Holding


@pytest.fixture
def sber_holding():
    return Holding(
        asset_id='MOEX:SBER',
        quantity=Decimal('280.2'),
        average_cost=Decimal('281.43'),
    )


@pytest.fixture
def empty_portfolio():
    return Portfolio(
        user_id=uuid.uuid4(),
        name='Test Portfolio',
        currency='USD',
    )


@pytest.fixture
def portfolio_with_sber(sber_holding):
    return Portfolio(
        user_id=uuid.uuid4(),
        name='Test Portfolio',
        currency='USD',
        holdings=[sber_holding],
    )
