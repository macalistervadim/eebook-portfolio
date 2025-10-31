import abc

from sqlalchemy.ext.asyncio import AsyncSession

from src.adapters.repository import AbstractPortfolioRepository, SqlAlchemyPortfolioRepository


class ABCPortfolioRepositoryFactory(abc.ABC):
    """Абстрактная фабрика для создания репозитория портфеля."""

    @abc.abstractmethod
    def create(self, session: AsyncSession) -> AbstractPortfolioRepository:
        """Создаёт экземпляр репозитория портфеля."""
        raise NotImplementedError


class SQLAlchemyPortfolioRepositoryFactory(ABCPortfolioRepositoryFactory):
    def create(self, session: AsyncSession) -> SqlAlchemyPortfolioRepository:
        return SqlAlchemyPortfolioRepository(session)
