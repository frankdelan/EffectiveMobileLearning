import asyncio
import datetime

import pytest
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from httpx import AsyncClient
from unittest.mock import AsyncMock

from pytest_mock import MockFixture
from sqlalchemy import text, NullPool
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from main import app
from models import Base
from config import settings

engine_test = create_async_engine(settings.DB_URL, poolclass=NullPool)
test_session_factory = async_sessionmaker(bind=engine_test, class_=AsyncSession, expire_on_commit=False)

TEST_DEAL = {'id': 1, 'exchange_product_id': 'A100PTK005A',
             'exchange_product_name': 'ДТ ЕВРО сорт C (ДТ-Л-К5) минус 5, РФ БП (ст. назначения)',
             'oil_id': 'A100', 'delivery_basis_id': 'PTK', 'delivery_basis_name': 'НБ Протокская',
             'delivery_type_id': 'F',
             'volume': 75, 'total': 10545240, 'count': 2, 'trading_date': datetime.date.today(),
             'created_on': datetime.datetime.now(), 'updated_on': None}


@pytest.fixture(scope='session', autouse=True)
async def setup_database():
    async with engine_test.begin() as conn:
        assert settings.MODE == 'TEST'
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
        await conn.execute(text("INSERT INTO public.spimex_trading_results VALUES "
                                "(:id, :exchange_product_id, :exchange_product_name, :oil_id, "
                                ":delivery_basis_id, :delivery_basis_name, :delivery_type_id, :volume,"
                                ":total, :count, :trading_date, :created_on, :updated_on)"), [TEST_DEAL])
    yield


@pytest.fixture
def mock_redis_backend(mocker: MockFixture) -> RedisBackend:
    redis_backend = mocker.Mock(spec=RedisBackend)
    redis_backend.get = AsyncMock()
    redis_backend.set = AsyncMock()
    return redis_backend


@pytest.fixture
async def get_client(mock_redis_backend):
    FastAPICache.init(mock_redis_backend, prefix="fastapi-cache")

    async with AsyncClient(app=app, base_url="http://127.0.0.1:8000") as client:
        yield client


@pytest.fixture(scope="module")
def event_loop():
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()
