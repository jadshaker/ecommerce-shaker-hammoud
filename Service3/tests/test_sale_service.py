from unittest.mock import MagicMock, patch

import pytest
from sale_service import SaleService


@pytest.fixture
def sale_service():
    with patch("sale_service.get_supabase_client") as mock_get_supabase_client:
        mock_supabase_client = MagicMock()
        mock_get_supabase_client.return_value = mock_supabase_client
        service = SaleService()
        yield service


def test_submit_sale(sale_service):
    sale_data = {"item": "book", "price": 10}
    sale_service.supabase.table().insert().execute.return_value = MagicMock(
        data=[sale_data]
    )

    result = sale_service.submit_sale(sale_data)

    assert result == sale_data


def test_update_sale(sale_service):
    sale_id = 1
    update_data = {"price": 15}
    sale_service.supabase.table().update().eq().execute.return_value = MagicMock(
        data=[update_data]
    )

    result = sale_service.update_sale(sale_id, update_data)

    assert result == update_data


def test_delete_sale(sale_service):
    sale_id = 1
    sale_service.supabase.table().delete().eq().execute.return_value = MagicMock(
        data=[{"sale_id": sale_id}]
    )

    result = sale_service.delete_sale(sale_id)

    assert result == [{"sale_id": sale_id}]


def test_get_customer_sales(sale_service):
    customer_id = 1
    sales_data = [{"sale_id": 1, "customer_id": customer_id, "item": "book"}]
    sale_service.supabase.table().select().eq().execute.return_value = MagicMock(
        data=sales_data
    )

    result = sale_service.get_customer_sales(customer_id)

    assert result == sales_data


def test_get_available_goods(sale_service):
    goods_data = [{"item": "book", "price": 10}]
    sale_service.supabase.table().select().execute.return_value = MagicMock(
        data=goods_data
    )

    result = sale_service.get_available_goods()

    assert result == goods_data
