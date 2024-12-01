from unittest.mock import MagicMock, patch

import pytest
from sale_service import SaleService


@pytest.fixture
def sale_service():
    """
    Fixture for creating a SaleService instance with a mocked Supabase client.

    This fixture patches the `get_supabase_client` method to return a mocked
    Supabase client. It then creates an instance of `SaleService` and yields it
    for use in tests.

    Yields:
        SaleService: An instance of the SaleService class with a mocked Supabase client.
    """
    with patch("sale_service.get_supabase_client") as mock_get_supabase_client:
        mock_supabase_client = MagicMock()
        mock_get_supabase_client.return_value = mock_supabase_client
        service = SaleService()
        yield service


def test_submit_sale(sale_service):
    """
    Test the submit_sale method of the sale_service.
    This test verifies that the submit_sale method correctly inserts sale data
    into the database and returns the inserted data.
    Args:
        sale_service (SaleService): An instance of the SaleService class.
    Setup:
        - Mocks the return value of the supabase table insert execute method to return the sale_data.
    Test Steps:
        1. Define sale_data with item and price.
        2. Mock the supabase table insert execute method to return sale_data.
        3. Call the submit_sale method with sale_data.
        4. Assert that the result of submit_sale is equal to sale_data.
    Asserts:
        - The result of submit_sale is equal to the sale_data.
    """
    sale_data = {"item": "book", "price": 10}
    sale_service.supabase.table().insert().execute.return_value = MagicMock(
        data=[sale_data]
    )

    result = sale_service.submit_sale(sale_data)

    assert result == sale_data


def test_update_sale(sale_service):
    """
    Test the update_sale method of the sale_service.
    This test verifies that the update_sale method correctly updates a sale with the given data.
    Args:
        sale_service (SaleService): An instance of the SaleService class.
    Setup:
        - Mocks the return value of the supabase table update method to return the updated data.
    Test Steps:
        1. Define a sale_id and update_data.
        2. Mock the supabase table update method to return the update_data.
        3. Call the update_sale method with the sale_id and update_data.
        4. Assert that the result of the update_sale method is equal to the update_data.
    """
    sale_id = 1
    update_data = {"price": 15}
    sale_service.supabase.table().update().eq().execute.return_value = MagicMock(
        data=[update_data]
    )

    result = sale_service.update_sale(sale_id, update_data)

    assert result == update_data


def test_delete_sale(sale_service):
    """
    Test the delete_sale method of the sale_service.
    This test verifies that the delete_sale method correctly deletes a sale
    with the given sale_id and returns the expected result.
    Args:
        sale_service (SaleService): An instance of the SaleService class.
    Setup:
        - Mocks the return value of the supabase table delete operation to
          simulate the deletion of a sale with the specified sale_id.
    Test Steps:
        1. Define a sale_id to be deleted.
        2. Mock the supabase table delete operation to return a MagicMock
           object with the expected data.
        3. Call the delete_sale method with the sale_id.
        4. Assert that the result of the delete_sale method matches the
           expected data.
    Asserts:
        - The result of the delete_sale method should be a list containing
          a dictionary with the sale_id.
    """
    sale_id = 1
    sale_service.supabase.table().delete().eq().execute.return_value = MagicMock(
        data=[{"sale_id": sale_id}]
    )

    result = sale_service.delete_sale(sale_id)

    assert result == [{"sale_id": sale_id}]


def test_get_customer_sales(sale_service):
    """
    Test the `get_customer_sales` method of the `sale_service`.
    This test verifies that the `get_customer_sales` method correctly retrieves
    sales data for a given customer ID.
    Args:
        sale_service (SaleService): An instance of the SaleService class.
    Setup:
        - Mocks the return value of the `execute` method of the `supabase.table().select().eq()` chain
          to return a predefined sales data list.
    Test Steps:
        1. Define a customer ID and corresponding sales data.
        2. Mock the `execute` method to return the predefined sales data.
        3. Call the `get_customer_sales` method with the customer ID.
        4. Assert that the result matches the predefined sales data.
    """
    customer_id = 1
    sales_data = [{"sale_id": 1, "customer_id": customer_id, "item": "book"}]
    sale_service.supabase.table().select().eq().execute.return_value = MagicMock(
        data=sales_data
    )

    result = sale_service.get_customer_sales(customer_id)

    assert result == sales_data


def test_get_available_goods(sale_service):
    """
    Test the `get_available_goods` method of the `sale_service`.
    This test mocks the response from the `supabase` table select query to return a predefined list of goods data.
    It then calls the `get_available_goods` method and asserts that the returned result matches the predefined goods data.
    Args:
        sale_service (SaleService): An instance of the SaleService class.
    Assertions:
        The result from `get_available_goods` should match the predefined goods data.
    """
    goods_data = [{"item": "book", "price": 10}]
    sale_service.supabase.table().select().execute.return_value = MagicMock(
        data=goods_data
    )

    result = sale_service.get_available_goods()

    assert result == goods_data
