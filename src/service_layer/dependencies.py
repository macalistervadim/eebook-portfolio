import logging

from src.adapters.factory import ABCPortfolioRepositoryFactory, SQLAlchemyPortfolioRepositoryFactory
from src.infrastructure.database.engine import get_session_factory
from src.service_layer.uow import AbstractUnitOfWork, SqlAlchemyUnitOfWork
from src.service_layer.users_service import ABCUserService, UserSerivce

logger = logging.getLogger(__name__)


def get_repo_factory() -> ABCPortfolioRepositoryFactory:
    return SQLAlchemyPortfolioRepositoryFactory()


def get_uow() -> AbstractUnitOfWork:
    return SqlAlchemyUnitOfWork(
        session_factory=get_session_factory(),
        repo_factory=get_repo_factory(),
    )


def get_user_service() -> ABCUserService:
    return UserSerivce(base_url='http://eebook-users-app-1:8000')
