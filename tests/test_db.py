import datetime

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from repositories.trading import TradingRepository
from tests.conftest import TEST_DEAL, engine_test


@pytest.mark.asyncio
class TestSuccessDatabase:
    @pytest.fixture(autouse=True)
    async def setup_class(self, event_loop):
        self.session = AsyncSession(bind=engine_test)
        self.repository = TradingRepository()

    @pytest.mark.parametrize('count', [
        1,
    ])
    async def test_get_last_by_count(self, count):
        """Тест успешных запросов к БД на получения n кол-ва последних сделок"""
        data = await self.repository.get_last_by_count(count)
        assert data == [datetime.date.today()]

    @pytest.mark.parametrize('data', [
        ({'oil_id': 'A100', 'delivery_type_id': None, 'delivery_basis_id': None}),
    ])
    async def test_get_last(self, data):
        """Тест успешных запросов к БД на получение сделок по параметрам"""
        data = await self.repository.get_last(data)
        assert data[0].id == TEST_DEAL['id']

    @pytest.mark.parametrize('data', [
        {'start_date': datetime.date(2024, 6, 1),
         'end_date': datetime.date(2025, 6, 1)}
    ])
    async def test_get_list_by_period(self, data):
        """Тест успешных запросов к БД на получение сделок за период"""
        data = await self.repository.get_list_by_period(data)
        assert data[0].id == TEST_DEAL['id']


@pytest.mark.asyncio
class TestErrorDatabase:
    @pytest.fixture(autouse=True)
    async def setup_class(self, event_loop):
        self.session = AsyncSession(bind=engine_test)
        self.repository = TradingRepository()

    @pytest.mark.parametrize('count', [
        0,
    ])
    async def test_get_last_by_count(self, count):
        """Тест ошибочных запросов к БД на получения n кол-ва последних сделок"""
        data = await self.repository.get_last_by_count(count)
        assert data == []

    @pytest.mark.parametrize('data', [
        ({'oil_id': 'A1000', 'delivery_type_id': None, 'delivery_basis_id': None}),
    ])
    async def test_get_last(self, data):
        """Тест успешных запросов к БД на получение сделок по параметрам"""
        data = await self.repository.get_last(data)
        assert data == []

    @pytest.mark.parametrize('data', [
        {'start_date': datetime.date(2025, 6, 1),
         'end_date': datetime.date(2024, 6, 1)}
    ])
    async def test_get_list_by_period(self, data):
        """Тест успешных запросов к БД на получение сделок за период"""
        data = await self.repository.get_list_by_period(data)
        assert data == []
