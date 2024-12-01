from unittest.mock import MagicMock, patch

import pytest
from inventory_service import InventoryService


@pytest.fixture
def inventory_service():
    with patch("inventory_service.get_supabase_client") as mock_get_supabase_client:
        mock_client = MagicMock()
        mock_get_supabase_client.return_value = mock_client
        service = InventoryService()
        yield service


def test_add_goods_success(inventory_service):
    product_data = {"product_id": 1, "name": "Test Product", "stock_count": 10}
    inventory_service.supabase.table().insert().execute.return_value = MagicMock(
        data=[product_data]
    )

    result = inventory_service.add_goods(product_data)

    assert result == product_data


def test_add_goods_failure(inventory_service):
    product_data = {"product_id": 1, "name": "Test Product", "stock_count": 10}
    inventory_service.supabase.table().insert().execute.side_effect = Exception(
        "Insert error"
    )

    with pytest.raises(ValueError, match="Error adding product: Insert error"):
        inventory_service.add_goods(product_data)


def test_deduct_goods_success(inventory_service):
    product_id = 1
    product_data = {"product_id": 1, "name": "Test Product", "stock_count": 10}
    updated_product_data = {"product_id": 1, "name": "Test Product", "stock_count": 9}

    inventory_service.get_product_by_id = MagicMock(return_value=product_data)
    inventory_service.supabase.table().update().eq().execute.return_value = MagicMock(
        data=[updated_product_data]
    )

    result = inventory_service.deduct_goods(product_id)

    assert result == updated_product_data


def test_deduct_goods_failure_no_product(inventory_service):
    product_id = 1
    inventory_service.get_product_by_id = MagicMock(return_value=None)

    with pytest.raises(ValueError, match="Product not found"):
        inventory_service.deduct_goods(product_id)


def test_deduct_goods_failure_stock_zero(inventory_service):
    product_id = 1
    product_data = {"product_id": 1, "name": "Test Product", "stock_count": 0}

    inventory_service.get_product_by_id = MagicMock(return_value=product_data)

    with pytest.raises(ValueError, match="Stock count is already zero"):
        inventory_service.deduct_goods(product_id)


def test_update_goods_success(inventory_service):
    product_id = 1
    update_data = {"name": "Updated Product"}
    updated_product_data = {
        "product_id": 1,
        "name": "Updated Product",
        "stock_count": 10,
    }

    inventory_service.supabase.table().update().eq().execute.return_value = MagicMock(
        data=[updated_product_data]
    )

    result = inventory_service.update_goods(product_id, update_data)

    assert result == updated_product_data


def test_update_goods_failure(inventory_service):
    product_id = 1
    update_data = {"name": "Updated Product"}
    inventory_service.supabase.table().update().eq().execute.side_effect = Exception(
        "Update error"
    )

    with pytest.raises(ValueError, match="Error updating product: Update error"):
        inventory_service.update_goods(product_id, update_data)


def test_get_product_by_id_success(inventory_service):
    product_id = 1
    product_data = {"product_id": 1, "name": "Test Product", "stock_count": 10}

    inventory_service.supabase.table().select().eq().execute.return_value = MagicMock(
        data=[product_data]
    )

    result = inventory_service.get_product_by_id(product_id)

    assert result == product_data


def test_get_product_by_id_failure(inventory_service):
    product_id = 1
    inventory_service.supabase.table().select().eq().execute.return_value = MagicMock(
        data=[]
    )

    result = inventory_service.get_product_by_id(product_id)

    assert result is None
