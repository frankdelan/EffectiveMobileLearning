import asyncio
import itertools

from database import async_session_factory
from scraping.parser import AsyncController


async def fill_database():
    """Функция для заполнения базы данных"""
    async_controller = AsyncController()
    objects = await async_controller.get_objects()
    async with async_session_factory() as session:
        session.add_all(itertools.chain.from_iterable(objects))
        await session.commit()

asyncio.run(fill_database())
