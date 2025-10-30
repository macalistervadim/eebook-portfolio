import uuid

from sqlalchemy import UUID, Column, DateTime, ForeignKey, MetaData, Numeric, String, Table, func

metadata = MetaData()

portfolio_table = Table(
    'portfolios',
    metadata,
    Column('id', UUID(as_uuid=True), primary_key=True),
    Column('user_id', UUID(as_uuid=True), nullable=False, index=True),
    Column('name', String(100), nullable=False),
    Column('currency', String(10), nullable=False),
    Column('created_at', DateTime(timezone=True), nullable=False, server_default=func.now()),
)

holding_table = Table(
    'holdings',
    metadata,
    Column('id', UUID(as_uuid=True), primary_key=True, default=uuid.uuid4),
    Column(
        'portfolio_id',
        UUID(as_uuid=True),
        ForeignKey('portfolios.id', ondelete='CASCADE'),
        nullable=False,
        index=True,
    ),
    Column('asset_id', String(100), nullable=False),
    Column('quantity', Numeric(precision=20, scale=10), nullable=False),
    Column('average_cost', Numeric(precision=20, scale=10), nullable=False),
)

transaction_table = Table(
    'transactions',
    metadata,
    Column('id', UUID(as_uuid=True), primary_key=True, default=uuid.uuid4),
    Column(
        'portfolio_id',
        UUID(as_uuid=True),
        ForeignKey('portfolios.id'),
        nullable=False,
        index=True,
    ),
    Column('asset_id', String(100), nullable=False),
    Column('transaction_type', String(20), nullable=False),  # "BUY", "SELL" и т.д.
    Column('quantity', Numeric(precision=20, scale=10), nullable=False),
    Column('price_per_unit', Numeric(precision=20, scale=10), nullable=False),
    Column('total_amount', Numeric(precision=20, scale=10), nullable=False),
    Column('executed_at', DateTime(timezone=True), nullable=False),
    Column('currency', String(10), nullable=False),
)
