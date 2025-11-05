import uuid
from decimal import Decimal
from unittest.mock import patch, mock_open, AsyncMock

import pytest

from src.adapters.factory import ABCPortfolioRepositoryFactory
from src.adapters.repository import AbstractPortfolioRepository
from src.adapters.vault_client import VaultClient
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


@pytest.fixture
def mock_vault_client():
    with (
        patch('builtins.open', mock_open(read_data='fake-token')),
        patch('src.adapters.vault_client.hvac.Client') as MockClient,
    ):
        mock_client = MockClient.return_value
        mock_client.is_authenticated.return_value = True
        mock_client.secrets.kv.v2.read_secret_version.return_value = {
            'data': {'data': {'username': 'admin', 'password': '123'}}
        }

        vc = VaultClient(addr='http://fake', token_file='/fake/token')
        yield vc


@pytest.fixture
def fake_uow():
    uow = AsyncMock()
    uow.users = AsyncMock()
    uow.commit = AsyncMock()
    # Настраиваем все методы репозитория как асинхронные
    uow.users.add = AsyncMock()
    uow.users.remove = AsyncMock()
    uow.users.activate = AsyncMock()
    uow.users.deactivate = AsyncMock()
    uow.users.get_by_email = AsyncMock()
    uow.users.get_by_id = AsyncMock()
    uow.users.update = AsyncMock()
    uow.users.update_login_time = AsyncMock()
    uow.users.list_all = AsyncMock()
    uow.users.verify_email = AsyncMock()
    uow.__aenter__.return_value = uow
    uow.__aexit__.return_value = None
    return uow


class FakeRepoFactory(ABCPortfolioRepositoryFactory):
    def create(self, session):
        return 'fake_repo'
