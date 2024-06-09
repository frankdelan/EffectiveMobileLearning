import datetime
from typing import Optional

from pydantic import BaseModel


class LastTradingSchema(BaseModel):
    oil_id: Optional[str] = None
    delivery_type_id: Optional[str] = None
    delivery_basis_id: Optional[str] = None


class LastPeriodTradingSchema(LastTradingSchema):
    start_date: datetime.date
    end_date: datetime.date
