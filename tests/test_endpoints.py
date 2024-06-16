import pytest


@pytest.mark.asyncio
class TestSuccessEndpoint:
    @pytest.mark.parametrize('count', [1])
    async def test_last_trading_dates(self, get_client, count):
        """Тест успешных запросов к API на получения n кол-ва последних сделок"""
        response = await get_client.get(f"/api/trading/list/{count}")
        assert response.json()['status'] == 200
        assert len(response.json()['data']) == abs(count)

    @pytest.mark.parametrize('oil_id, delivery_type_id, delivery_basis_id', [
        (None, None, None), ('A100', None, None), ('A100', 'F', 'PTK')
    ])
    async def test_trading_results(self, get_client, oil_id, delivery_type_id, delivery_basis_id):
        """Тест успешных запросов к API на получение сделок по параметрам"""
        response = await get_client.get(f"/api/trading/list", params={'oil_id': oil_id,
                                                                      'delivery_type_id': delivery_type_id,
                                                                      'delivery_basis_id': delivery_basis_id})
        assert response.json()['status'] == 200

    @pytest.mark.parametrize('start_date, end_date', [
        ('2024-06-01', '2025-06-01')
    ])
    async def test_dynamics(self, get_client, start_date, end_date):
        """Тест успешных запросов к API на получение сделок за период"""
        response = await get_client.get(f"/api/trading/period?start_date={start_date}&end_date={end_date}")
        assert response.json()['status'] == 200


class TestErrorEndpoint:
    @pytest.mark.parametrize('count', [0])
    async def test_last_trading_dates(self, get_client, count):
        """Тест ошибочных запросов к API на получение n кол-ва последних сделок"""
        response = await get_client.get(f"/api/trading/list/{count}")
        data = response.json()
        assert data['status'] == 404
        assert data['detail'] == 'Deals not found'

    @pytest.mark.parametrize('oil_id, delivery_type_id, delivery_basis_id', [
        ('TEST_ID', 'TEST_TYPE_ID', 'TEST_BASIS_ID')
    ])
    async def test_trading_results(self, get_client, oil_id, delivery_type_id, delivery_basis_id):
        """Тест ошибочных запросов к API на получение сделок по параметрам"""
        response = await get_client.get(f"/api/trading/list", params={'oil_id': oil_id,
                                                                      'delivery_type_id': delivery_type_id,
                                                                      'delivery_basis_id': delivery_basis_id})
        assert response.json()['status'] == 404
        assert response.json()['detail'] == 'Deals not found'

    @pytest.mark.parametrize('start_date, end_date', [
        ('2026-01-01', '2024-05-29'), (0, 0)
    ])
    async def test_dynamics(self, get_client, start_date, end_date):
        """Тест ошибочных запросов к API на получение сделок за период"""
        response = await get_client.get(f"/api/trading/period?start_date={start_date}&end_date={end_date}")

        assert response.json()['status'] == 404
        assert response.json()['detail'] == 'Deals not found'
