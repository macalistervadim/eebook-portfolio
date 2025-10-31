import logging
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import async_sessionmaker
from starlette.responses import JSONResponse

from src.adapters.factory import SQLAlchemyPortfolioRepositoryFactory
from src.config.settings import Settings
from src.domain.domain import Portfolio, Transaction
from src.service_layer.dependencies import get_settings
from src.service_layer.portfolio_service import PortfolioService, UserSerivce
from src.service_layer.uow import SqlAlchemyUnitOfWork

router = APIRouter(tags=['users'])

logger = logging.getLogger(__name__)


settings_dependency = Depends(get_settings)


@router.get('/health')
async def health(settings: Settings = settings_dependency) -> JSONResponse:
    content = {
        'status': 'ok',
        'database': 'connected' if settings.POSTGRES_HOST else 'disconnected',
    }
    return JSONResponse(content=content, status_code=status.HTTP_200_OK)


repo_factory = SQLAlchemyPortfolioRepositoryFactory()
uow = SqlAlchemyUnitOfWork(session_factory=async_sessionmaker, repo_factory=repo_factory)  # type: ignore
user_service = UserSerivce()


@router.post('/portfolios')
async def create_portfolio(payload: dict):
    portfolio = Portfolio(
        user_id=UUID(payload['user_id']),
        name=payload['name'],
        currency=payload['currency'],
    )
    async with uow as u:
        service = PortfolioService(u.users, user_service)
        try:
            await service.add(portfolio)
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e)) from e
        await u.commit()
    return {'id': str(portfolio.id)}


@router.get('/portfolios/{portfolio_id}')
async def get_portfolio(portfolio_id: UUID):
    async with uow as u:
        service = PortfolioService(u.users, user_service)
        portfolio = await service.get_by_id(portfolio_id)
        if not portfolio:
            raise HTTPException(status_code=404, detail='Portfolio not found')
    return portfolio.__dict__


@router.get('/users/{user_id}/portfolios')
async def get_user_portfolios(user_id: UUID):
    async with uow as u:
        service = PortfolioService(u.users, user_service)
        portfolios = await service.get_by_user_id(user_id)
    return [p.__dict__ for p in portfolios]


@router.put('/portfolios/{portfolio_id}')
async def update_portfolio(portfolio_id: UUID, payload: dict):
    async with uow as u:
        service = PortfolioService(u.users, user_service)
        portfolio = await service.get_by_id(portfolio_id)
        if not portfolio:
            raise HTTPException(status_code=404, detail='Portfolio not found')
        portfolio.name = payload.get('name', portfolio.name)
        portfolio.currency = payload.get('currency', portfolio.currency)
        await service.update(portfolio)
        await u.commit()
    return {'status': 'updated'}


@router.delete('/portfolios/{portfolio_id}')
async def delete_portfolio(portfolio_id: UUID):
    async with uow as u:
        service = PortfolioService(u.users, user_service)
        await service.delete(portfolio_id)
        await u.commit()
    return {'status': 'deleted'}


@router.post('/transactions')
async def add_transaction(payload: dict):
    transaction = Transaction(
        portfolio_id=UUID(payload['portfolio_id']),
        asset_id=payload['asset_id'],
        transaction_type=payload['transaction_type'],
        quantity=payload['quantity'],
        price_per_unit=payload['price_per_unit'],
        total_amount=payload['total_amount'],
        executed_at=payload['executed_at'],
        currency=payload['currency'],
    )
    async with uow as u:
        service = PortfolioService(u.users, user_service)
        await service.add_transaction(transaction)
        await u.commit()
    return {'id': str(transaction.id)}
