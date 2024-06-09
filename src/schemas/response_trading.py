import datetime
from typing import Optional

from pydantic import BaseModel


class TradingDateSchema(BaseModel):
    trading_date: datetime.date

    class Config:
        from_attributes = True


class TradingDealSchema(TradingDateSchema):
    exchange_product_id: str
    exchange_product_name: str
    oil_id: str
    delivery_basis_id: str
    delivery_basis_name: str
    delivery_type_id: str
    volume: int
    total: int
    count: int
    created_on: datetime.datetime
    updated_on: Optional[datetime.datetime]

    class Config:
        from_attributes = True
