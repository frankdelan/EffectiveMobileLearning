from fastapi import Depends

from repositories.base import DatabaseRepository


class BaseService:
    def __init__(self, repository: DatabaseRepository = Depends(DatabaseRepository)):
        self.repository: DatabaseRepository = repository

    async def get_last_trading_dates(self, count: int):
        return await self.repository.get_last_by_count(count)

    async def get_dynamics(self, data: dict[str, str]):
        return await self.repository.get_list_by_period(data)

    async def get_trading_results(self, data: dict[str, str]):
        return await self.repository.get_last(data)
