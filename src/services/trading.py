from fastapi import Depends

from services.base import BaseService
from repositories.trading import TradingRepository


class TradingService(BaseService):
    def __init__(self, repository: TradingRepository = Depends(TradingRepository)):
        super().__init__(repository)
