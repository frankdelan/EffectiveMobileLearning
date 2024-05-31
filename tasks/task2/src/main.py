import asyncio
import itertools

from tasks.task2.src.database import async_session_factory
from tasks.task2.src.scraping.parser import AsyncController


async def fill_database():
    async_controller = AsyncController()
    objects = await async_controller.get_objects()
    for item in itertools.chain.from_iterable(objects):
        async with async_session_factory() as session:
            session.add(item)
            await session.commit()

asyncio.run(fill_database())
