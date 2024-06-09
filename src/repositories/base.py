import datetime
from abc import ABC, abstractmethod

from sqlalchemy import and_, select

from database import async_session_factory


class AbstractRepository(ABC):
    @abstractmethod
    async def get_list_by_period(self, *args, **kwargs):
        raise NotImplementedError

    @abstractmethod
    async def get_last_by_count(self, *args, **kwargs):
        raise NotImplementedError

    @abstractmethod
    async def get_last(self, *args, **kwargs):
        raise NotImplementedError


class DatabaseRepository(AbstractRepository):
    model = None
    LIMIT = 100

    async def get_last_by_count(self, count: int):
        """Метод для получения последних n записей"""
        async with async_session_factory() as session:
            limit = self.LIMIT if count > self.LIMIT else count
            query = select(self.model.trading_date).distinct().order_by(self.model.trading_date.desc()).limit(limit)
            result = await session.execute(query)
            return result.scalars().all()

    async def get_last(self, data: dict[str, str]):
        """Метод для получения записей по фильтрам"""
        async with async_session_factory() as session:
            filters = {k: v for k, v in data.items() if v is not None}
            query = select(self.model).filter_by(**filters).limit(self.LIMIT)
            result = await session.execute(query)
            return result.scalars().all()

    async def get_list_by_period(self, data: dict[str, str]):
        """Метод для получения записей за определенный период"""
        async with (async_session_factory() as session):
            filters = {k: v for k, v in data.items() if v is not None}
            query = select(self.model).where(and_(
                self.model.trading_date >= filters.pop('start_date'),
                self.model.trading_date < filters.pop('end_date'))
            ).filter_by(**filters).limit(self.LIMIT)
            result = await session.execute(query)
            return result.scalars().all()
