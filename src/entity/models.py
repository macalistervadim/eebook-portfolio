import datetime
from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel

from src.domain.enums import TransactionType


class CreatePortfolio(BaseModel):
    user_id: UUID
    name: str
    currency: str


class UpdatePortfolio(BaseModel):
    portfolio_id: UUID
    name: str
    currency: str


class AddTransaction(BaseModel):
    portfolio_id: UUID
    asset_id: str
    transaction_type: TransactionType
    quantity: Decimal
    price_per_unit: Decimal
    total_amount: Decimal
    executed_at: datetime.datetime
    currency: str
