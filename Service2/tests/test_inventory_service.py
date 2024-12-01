from unittest.mock import MagicMock, patch

import pytest
from inventory_service import InventoryService


@pytest.fixture
def inventory_service():
    """
    Fixture for setting up the InventoryService with a mocked Supabase client.

    This fixture patches the `get_supabase_client` method of the `inventory_service` module
    to return a mocked Supabase client. It then initializes an instance of `InventoryService`
    and yields it for use in tests.

    Yields:
        InventoryService: An instance of the InventoryService with a mocked Supabase client.
    """
    with patch("inventory_service.get_supabase_client") as mock_get_supabase_client:
        mock_client = MagicMock()
        mock_get_supabase_client.return_value = mock_client
        service = InventoryService()
        yield service


def test_add_goods_success(inventory_service):
    """
    Test the successful addition of goods to the inventory service.
    This test verifies that the `add_goods` method of the `inventory_service` correctly adds a product to the inventory
    and returns the expected product data.
    Args:
        inventory_service (InventoryService): The inventory service instance being tested.
    Setup:
        - Mocks the `supabase.table().insert().execute` method to return a MagicMock with the expected product data.
    Test Steps:
        1. Define the product data to be added.
        2. Mock the `supabase.table().insert().execute` method to return the product data.
        3. Call the `add_goods` method with the product data.
        4. Assert that the result of the `add_goods` method matches the expected product data.
    Asserts:
        - The result of the `add_goods` method should be equal to the product data.
    """
    product_data = {"product_id": 1, "name": "Test Product", "stock_count": 10}
    inventory_service.supabase.table().insert().execute.return_value = MagicMock(
        data=[product_data]
    )

    result = inventory_service.add_goods(product_data)

    assert result == product_data


def test_add_goods_failure(inventory_service):
    """
    Test case for the `add_goods` method in the `inventory_service` when the insertion of goods fails.
    This test simulates a failure scenario where the insertion of a product into the inventory
    raises an exception. It verifies that the `add_goods` method properly handles the exception
    and raises a `ValueError` with an appropriate error message.
    Args:
        inventory_service (InventoryService): The inventory service instance to be tested.
    Setup:
        - Mocks the `supabase.table().insert().execute` method to raise an `Exception` with the message "Insert error".
    Test:
        - Calls the `add_goods` method with a sample product data dictionary.
        - Asserts that a `ValueError` is raised with the message "Error adding product: Insert error".
    """
    product_data = {"product_id": 1, "name": "Test Product", "stock_count": 10}
    inventory_service.supabase.table().insert().execute.side_effect = Exception(
        "Insert error"
    )

    with pytest.raises(ValueError, match="Error adding product: Insert error"):
        inventory_service.add_goods(product_data)


def test_deduct_goods_success(inventory_service):
    """
    Test the deduct_goods method of the inventory_service to ensure it successfully deducts goods from the inventory.
    This test mocks the get_product_by_id method to return a product with a stock count of 10.
    It also mocks the update method of the supabase table to return the updated product data with a stock count of 9.
    The test then calls the deduct_goods method with the product_id and asserts that the result matches the updated product data.
    Args:
        inventory_service (InventoryService): The inventory service instance to be tested.
    Asserts:
        The result of deduct_goods matches the updated product data with the decremented stock count.
    """
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
    """
    Test case for deducting goods from inventory when the product does not exist.
    This test verifies that the `deduct_goods` method of the `inventory_service`
    raises a `ValueError` with the message "Product not found" when attempting to
    deduct goods for a product ID that does not exist in the inventory.
    Args:
        inventory_service (InventoryService): The inventory service instance being tested.
    Setup:
        - Mocks the `get_product_by_id` method of the `inventory_service` to return `None`,
          simulating a non-existent product.
    Test Steps:
        1. Define a product ID that does not exist in the inventory.
        2. Mock the `get_product_by_id` method to return `None` for the given product ID.
        3. Use `pytest.raises` to assert that calling `deduct_goods` with the non-existent
           product ID raises a `ValueError` with the expected error message.
    """
    product_id = 1
    inventory_service.get_product_by_id = MagicMock(return_value=None)

    with pytest.raises(ValueError, match="Product not found"):
        inventory_service.deduct_goods(product_id)


def test_deduct_goods_failure_stock_zero(inventory_service):
    """
    Test the `deduct_goods` method of the `inventory_service` when the stock count is zero.
    This test verifies that the `deduct_goods` method raises a `ValueError` with the appropriate
    error message when attempting to deduct goods from a product whose stock count is already zero.
    Args:
        inventory_service (InventoryService): The inventory service instance to be tested.
    Setup:
        - Mocks the `get_product_by_id` method of the `inventory_service` to return a product
          with a stock count of zero.
    Test:
        - Calls the `deduct_goods` method with a product ID.
        - Asserts that a `ValueError` is raised with the message "Stock count is already zero".
    """
    product_id = 1
    product_data = {"product_id": 1, "name": "Test Product", "stock_count": 0}

    inventory_service.get_product_by_id = MagicMock(return_value=product_data)

    with pytest.raises(ValueError, match="Stock count is already zero"):
        inventory_service.deduct_goods(product_id)


def test_update_goods_success(inventory_service):
    """
    Test the successful update of goods in the inventory service.
    This test verifies that the `update_goods` method of the `inventory_service`
    correctly updates a product's information and returns the updated product data.
    Args:
        inventory_service (InventoryService): The inventory service instance to be tested.
    Setup:
        - Mocks the `supabase.table().update().eq().execute` method to return a MagicMock
          with the updated product data.
    Test Steps:
        1. Define the product ID and the update data.
        2. Mock the `execute` method to return the updated product data.
        3. Call the `update_goods` method with the product ID and update data.
        4. Assert that the result of the `update_goods` method matches the expected updated product data.
    Asserts:
        - The result of the `update_goods` method should be equal to the mocked updated product data.
    """
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
    """
    Test case for the `update_goods` method in the `inventory_service` when the update operation fails.
    This test simulates a failure scenario where an exception is raised during the update operation.
    It verifies that the `update_goods` method raises a `ValueError` with the appropriate error message.
    Args:
        inventory_service (InventoryService): The inventory service instance to be tested.
    Raises:
        ValueError: If the `update_goods` method raises a `ValueError` with the message "Error updating product: Update error".
    """
    product_id = 1
    update_data = {"name": "Updated Product"}
    inventory_service.supabase.table().update().eq().execute.side_effect = Exception(
        "Update error"
    )

    with pytest.raises(ValueError, match="Error updating product: Update error"):
        inventory_service.update_goods(product_id, update_data)


def test_get_product_by_id_success(inventory_service):
    """
    Test the `get_product_by_id` method of the `inventory_service` for a successful case.
    This test verifies that the `get_product_by_id` method correctly retrieves a product
    by its ID when the product exists in the inventory.
    Args:
        inventory_service (InventoryService): The inventory service instance to be tested.
    Setup:
        - Mocks the `supabase.table().select().eq().execute` method to return a predefined
          product data when called.
    Test Steps:
        1. Define a product ID and corresponding product data.
        2. Mock the `execute` method of the `supabase` query to return the predefined product data.
        3. Call the `get_product_by_id` method with the product ID.
        4. Assert that the result matches the predefined product data.
    Asserts:
        - The result returned by `get_product_by_id` should match the predefined product data.
    """
    product_id = 1
    product_data = {"product_id": 1, "name": "Test Product", "stock_count": 10}

    inventory_service.supabase.table().select().eq().execute.return_value = MagicMock(
        data=[product_data]
    )

    result = inventory_service.get_product_by_id(product_id)

    assert result == product_data


def test_get_product_by_id_failure(inventory_service):
    """
    Test case for the failure scenario of the `get_product_by_id` method in the `inventory_service`.
    This test verifies that the `get_product_by_id` method returns `None` when the product with the specified ID does not exist in the inventory.
    Args:
        inventory_service (InventoryService): The inventory service instance to be tested.
    Test Steps:
    1. Set up the `inventory_service` mock to return an empty list when querying for the product by ID.
    2. Call the `get_product_by_id` method with a non-existent product ID.
    3. Assert that the result is `None`, indicating that the product was not found.
    Expected Result:
    The `get_product_by_id` method should return `None` when the product with the specified ID is not found in the inventory.
    """
    product_id = 1
    inventory_service.supabase.table().select().eq().execute.return_value = MagicMock(
        data=[]
    )

    result = inventory_service.get_product_by_id(product_id)

    assert result is None
