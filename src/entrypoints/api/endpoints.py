import logging
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from starlette.responses import JSONResponse

from src.config.settings import Settings, get_settings
from src.domain.domain import Portfolio, Transaction
from src.entity.models import AddTransaction, CreatePortfolio, UpdatePortfolio
from src.service_layer.dependencies import get_uow, get_user_service
from src.service_layer.portfolio_service import ABCUserService, PortfolioService
from src.service_layer.uow import AbstractUnitOfWork

router = APIRouter(prefix='/api/v1/portfolio', tags=['users'])

logger = logging.getLogger(__name__)


@router.get('/health')
async def health(settings: Settings = Depends(get_settings)) -> JSONResponse:
    content = {
        'status': 'ok',
        'database': 'connected' if settings.POSTGRES_HOST else 'disconnected',
    }
    return JSONResponse(content=content, status_code=status.HTTP_200_OK)


@router.post('/portfolios')
async def create_portfolio(
    portfolio_create_entity: CreatePortfolio,
    uow: AbstractUnitOfWork = Depends(get_uow),
    user_service: ABCUserService = Depends(get_user_service),
):
    portfolio = Portfolio(
        user_id=portfolio_create_entity.user_id,
        name=portfolio_create_entity.name,
        currency=portfolio_create_entity.currency,
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
async def get_portfolio(
    portfolio_id: UUID,
    uow: AbstractUnitOfWork = Depends(get_uow),
    user_service: ABCUserService = Depends(get_user_service),
):
    async with uow as u:
        service = PortfolioService(u.users, user_service)
        portfolio = await service.get_by_id(portfolio_id)
        if not portfolio:
            raise HTTPException(status_code=404, detail='Portfolio not found')
    return portfolio.__dict__


@router.get('/users/{user_id}/portfolios')
async def get_user_portfolios(
    user_id: UUID,
    uow: AbstractUnitOfWork = Depends(get_uow),
    user_service: ABCUserService = Depends(get_user_service),
):
    async with uow as u:
        service = PortfolioService(u.users, user_service)
        portfolios = await service.get_by_user_id(user_id)
    return [p.__dict__ for p in portfolios]


@router.put('/portfolios/{portfolio_id}')
async def update_portfolio(
    update_portfolio_entity: UpdatePortfolio,
    uow: AbstractUnitOfWork = Depends(get_uow),
    user_service: ABCUserService = Depends(get_user_service),
):
    async with uow as u:
        service = PortfolioService(u.users, user_service)
        portfolio = await service.get_by_id(update_portfolio_entity.portfolio_id)
        if not portfolio:
            raise HTTPException(status_code=404, detail='Portfolio not found')
        portfolio.name = update_portfolio_entity.name
        portfolio.currency = update_portfolio_entity.currency
        await service.update(portfolio)
        await u.commit()
    return {'status': 'updated'}


@router.delete('/portfolios/{portfolio_id}')
async def delete_portfolio(
    portfolio_id: UUID,
    uow: AbstractUnitOfWork = Depends(get_uow),
    user_service: ABCUserService = Depends(get_user_service),
):
    async with uow as u:
        service = PortfolioService(u.users, user_service)
        await service.delete(portfolio_id)
        await u.commit()
    return {'status': 'deleted'}


@router.post('/transactions')
async def add_transaction(
    add_transaction_entity: AddTransaction,
    uow: AbstractUnitOfWork = Depends(get_uow),
    user_service: ABCUserService = Depends(get_user_service),
):
    transaction = Transaction(
        portfolio_id=add_transaction_entity.portfolio_id,
        asset_id=add_transaction_entity.asset_id,
        transaction_type=add_transaction_entity.transaction_type,
        quantity=add_transaction_entity.quantity,
        price_per_unit=add_transaction_entity.price_per_unit,
        total_amount=add_transaction_entity.total_amount,
        executed_at=add_transaction_entity.executed_at,
        currency=add_transaction_entity.currency,
    )
    async with uow as u:
        service = PortfolioService(u.users, user_service)
        await service.add_transaction(transaction)
        await u.commit()
    return {'id': str(transaction.id)}
