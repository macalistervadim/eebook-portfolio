import abc
from uuid import UUID

from src.adapters.repository import AbstractPortfolioRepository
from src.domain.domain import Portfolio, Transaction


class ABCPortfolioService(abc.ABC):
    @abc.abstractmethod
    async def add(self, portfolio: Portfolio) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    async def get_by_id(self, portfolio_id: UUID) -> Portfolio | None:
        raise NotImplementedError

    @abc.abstractmethod
    async def get_by_user_id(self, user_id: UUID) -> list[Portfolio]:
        raise NotImplementedError

    @abc.abstractmethod
    async def update(self, portfolio: Portfolio) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    async def delete(self, portfolio_id: UUID) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    async def add_transaction(self, transaction: Transaction) -> None:
        raise NotImplementedError


class ABCUserService(abc.ABC):
    @abc.abstractmethod
    async def get_by_id(self, user_id: UUID) -> dict | None:
        raise NotImplementedError


class UserSerivce(ABCUserService):
    async def get_by_id(self, user_id: UUID) -> dict | None:
        return {
            'id': user_id,
            'name': 'John Doe',
            'email': 'john.doe@example.com',
        }


class PortfolioService(ABCPortfolioService):
    def __init__(self, repo: AbstractPortfolioRepository, user_service: ABCUserService) -> None:
        self._repo = repo
        self._user_service = user_service

    async def add(self, portfolio: Portfolio) -> None:
        user = await self._user_service.get_by_id(portfolio.user_id)
        if user is None:
            raise ValueError('User not found')

        await self._repo.add(portfolio)

    async def get_by_id(self, portfolio_id: UUID) -> Portfolio | None:
        return await self._repo.get_by_id(portfolio_id)

    async def get_by_user_id(self, user_id: UUID) -> list[Portfolio]:
        return await self._repo.get_by_user_id(user_id)

    async def update(self, portfolio: Portfolio) -> None:
        await self._repo.update(portfolio)

    async def delete(self, portfolio_id: UUID) -> None:
        await self._repo.delete(portfolio_id)

    async def add_transaction(self, transaction: Transaction) -> None:
        await self._repo.add_transaction(transaction)
