from contextlib import asynccontextmanager
from typing import AsyncIterator

from fastapi import FastAPI
from routers.trading import router as trading_router

from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from redis import asyncio as aioredis

from config import settings

app = FastAPI()

app.include_router(trading_router)


@app.on_event("startup")
async def startup():
    redis = aioredis.from_url(settings.REDIS_URL, encoding="utf8", decode_responses=True)
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")
