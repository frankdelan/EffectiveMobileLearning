from models import SpimexTradingResults
from repositories.base import DatabaseRepository


class TradingRepository(DatabaseRepository):
    model = SpimexTradingResults
