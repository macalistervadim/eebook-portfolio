import abc
import uuid
from uuid import UUID

from sqlalchemy import delete as sa_delete
from sqlalchemy import insert, select
from sqlalchemy import update as sa_update

from src.adapters.orm import (
    holding_table,
    portfolio_table,
    transaction_table,
)
from src.domain.domain import Holding, Portfolio, Transaction


class AbstractPortfolioRepository(abc.ABC):
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


class SqlAlchemyPortfolioRepository(AbstractPortfolioRepository):
    def __init__(self, session):
        self.session = session

    async def add(self, portfolio: Portfolio) -> None:
        stmt = insert(portfolio_table).values(
            id=portfolio.id,
            user_id=portfolio.user_id,
            name=portfolio.name,
            currency=portfolio.currency,
            created_at=portfolio.created_at,
        )
        await self.session.execute(stmt)

        for h in portfolio.holdings:
            stmt_h = insert(holding_table).values(
                id=uuid.uuid4(),
                portfolio_id=portfolio.id,
                asset_id=h.asset_id,
                quantity=h.quantity,
                average_cost=h.average_cost,
            )
            await self.session.execute(stmt_h)

    async def get_by_id(self, portfolio_id):
        row = await self.session.execute(
            select(portfolio_table).where(portfolio_table.c.id == portfolio_id),
        )
        p_data = row.first()
        if not p_data:
            return None

        row_h = await self.session.execute(
            select(holding_table).where(holding_table.c.portfolio_id == portfolio_id),
        )
        holdings = [Holding(h.asset_id, h.quantity, h.average_cost) for h in row_h.fetchall()]

        return Portfolio(
            user_id=p_data.user_id,
            name=p_data.name,
            currency=p_data.currency,
            holdings=holdings,
            created_at=p_data.created_at,
        )

    async def get_by_user_id(self, user_id):
        row = await self.session.execute(
            select(portfolio_table).where(portfolio_table.c.user_id == user_id),
        )
        portfolios_data = row.fetchall()
        portfolios = []

        for p_data in portfolios_data:
            row_h = await self.session.execute(
                select(holding_table).where(holding_table.c.portfolio_id == p_data.id),
            )
            holdings = [Holding(h.asset_id, h.quantity, h.average_cost) for h in row_h.fetchall()]
            portfolios.append(
                Portfolio(
                    user_id=p_data.user_id,
                    name=p_data.name,
                    currency=p_data.currency,
                    holdings=holdings,
                    created_at=p_data.created_at,
                ),
            )
        return portfolios

    async def update(self, portfolio: Portfolio) -> None:
        stmt = (
            sa_update(portfolio_table)
            .where(portfolio_table.c.id == portfolio.id)
            .values(
                name=portfolio.name,
                currency=portfolio.currency,
            )
        )
        await self.session.execute(stmt)

        stmt_del = sa_delete(holding_table).where(holding_table.c.portfolio_id == portfolio.id)
        await self.session.execute(stmt_del)

        for h in portfolio.holdings:
            stmt_h = insert(holding_table).values(
                id=uuid.uuid4(),
                portfolio_id=portfolio.id,
                asset_id=h.asset_id,
                quantity=h.quantity,
                average_cost=h.average_cost,
            )
            await self.session.execute(stmt_h)

    async def delete(self, portfolio_id) -> None:
        stmt_h = sa_delete(holding_table).where(holding_table.c.portfolio_id == portfolio_id)
        await self.session.execute(stmt_h)

        stmt = sa_delete(portfolio_table).where(portfolio_table.c.id == portfolio_id)
        await self.session.execute(stmt)

    async def add_transaction(self, transaction: Transaction) -> None:
        stmt = insert(transaction_table).values(
            id=transaction.id,
            portfolio_id=transaction.portfolio_id,
            asset_id=transaction.asset_id,
            transaction_type=transaction.transaction_type,  # type: ignore
            quantity=transaction.quantity,
            price_per_unit=transaction.price_per_unit,
            total_amount=transaction.total_amount,
            executed_at=transaction.executed_at,
            currency=transaction.currency,
        )
        await self.session.execute(stmt)
