import asyncio
from typing import Callable, Optional

from aiohttp import ClientConnectorError, ClientPayloadError


def handle_client_exception(default_return: Optional[list]):
    """Декоратор для огранчиения количества запросов и обработки исключений"""
    def decorator(func):
        async def wrapper(*args, **kwargs):
            async with asyncio.Semaphore(10):
                try:
                    return await func(*args, **kwargs)
                except (ClientConnectorError, ClientPayloadError):
                    return default_return
        return wrapper
    return decorator
