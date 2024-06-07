import asyncio
import datetime
from typing import Optional

from sqlalchemy import BigInteger
from sqlalchemy.orm import Mapped, mapped_column

from database import Base, async_engine


class SpimexTradingResults(Base):
    __tablename__ = 'spimex_trading_results'

    id: Mapped[int] = mapped_column(autoincrement=True, primary_key=True)
    exchange_product_id: Mapped[str]
    exchange_product_name: Mapped[str]
    oil_id: Mapped[str]
    delivery_basis_id: Mapped[str]
    delivery_basis_name: Mapped[str]
    delivery_type_id: Mapped[str]
    volume: Mapped[Optional[int]]
    total: Mapped[Optional[int]] = mapped_column(BigInteger)
    count: Mapped[int]
    trading_date: Mapped[datetime.date]
    created_on: Mapped[datetime.datetime] = mapped_column(default=datetime.datetime.now())
    updated_on: Mapped[Optional[datetime.datetime]]
