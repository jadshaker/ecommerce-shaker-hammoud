from unittest.mock import Mock, patch

import pytest
from customer_service import CustomerService


@pytest.fixture
def mock_supabase():
    """
    Fixture that provides a mock object for Supabase.

    This fixture returns a mock object that can be used to simulate interactions
    with the Supabase service in tests. It uses the `Mock` class from the `unittest.mock`
    module to create the mock object.

    Returns:
        Mock: A mock object for Supabase.
    """
    return Mock()


@pytest.fixture
def customer_service(mock_supabase):
    """
    Fixture for creating a CustomerService instance with a mocked Supabase client.

    Args:
        mock_supabase (Mock): A mock object for the Supabase client.

    Returns:
        CustomerService: An instance of the CustomerService class with the mocked Supabase client.
    """
    with patch("customer_service.get_supabase_client", return_value=mock_supabase):
        service = CustomerService()
        return service


def test_register_customer_success(customer_service, mock_supabase):
    """
    Test the successful registration of a customer.
    This test verifies that the `register_customer` method of the `customer_service`
    correctly registers a new customer when provided with valid customer data.
    Args:
        customer_service (CustomerService): The customer service instance to be tested.
        mock_supabase (Mock): A mock instance of the Supabase client.
    Setup:
        - Mocks the Supabase client's `insert` method to return the provided customer data.
        - Mocks the Supabase client's `select` method to return an empty list, indicating no existing customer.
    Test Steps:
        1. Arrange: Prepare the customer data and mock the Supabase client's responses.
        2. Act: Call the `register_customer` method with the prepared customer data.
        3. Assert: Verify that the result of the method call matches the provided customer data.
    Asserts:
        - The result of the `register_customer` method should be equal to the provided customer data.
    """
    # Arrange
    customer_data = {
        "username": "testuser",
        "password": "password123",
        "email": "test@test.com",
    }
    mock_supabase.table().insert().execute.return_value.data = [customer_data]
    mock_supabase.table().select().eq().execute.return_value.data = []

    # Act
    result = customer_service.register_customer(customer_data)

    # Assert
    assert result == customer_data


def test_register_customer_existing_username(customer_service, mock_supabase):
    """
    Test the `register_customer` method of `customer_service` when the username already exists.
    This test verifies that the `register_customer` method raises a `ValueError` with the message
    "Username already exists" when attempting to register a customer with a username that is already
    present in the database.
    Args:
        customer_service: The customer service instance to be tested.
        mock_supabase: A mock instance of the Supabase client.
    Test Steps:
    1. Arrange:
        - Create a dictionary `customer_data` containing the username and password of the customer to be registered.
        - Configure the mock Supabase client to return a list containing an existing user with the same username.
    2. Act & Assert:
        - Use `pytest.raises` to assert that calling `register_customer` with `customer_data` raises a `ValueError`
          with the message "Username already exists".
    """
    # Arrange
    customer_data = {"username": "existinguser", "password": "password123"}
    mock_supabase.table().select().eq().execute.return_value.data = [
        {"username": "existinguser"}
    ]

    # Act & Assert
    with pytest.raises(ValueError, match="Username already exists"):
        customer_service.register_customer(customer_data)


def test_get_customer_by_username_success(customer_service, mock_supabase):
    """
    Test the `get_customer_by_username` method of the `customer_service` for a successful case.
    This test verifies that the `get_customer_by_username` method returns the expected customer
    data when a valid username is provided.
    Args:
        customer_service (CustomerService): The customer service instance to be tested.
        mock_supabase (Mock): A mock instance of the Supabase client.
    Setup:
        - Mocks the Supabase client's `table().select().eq().execute()` method to return
          a predefined customer data.
    Test Steps:
        1. Arrange: Set up the expected customer data and mock the Supabase client's response.
        2. Act: Call the `get_customer_by_username` method with a test username.
        3. Assert: Verify that the returned result matches the expected customer data.
    Expected Result:
        The method should return the expected customer data for the given username.
    """
    # Arrange
    expected_customer = {"username": "testuser", "email": "test@test.com"}
    mock_supabase.table().select().eq().execute.return_value.data = [expected_customer]

    # Act
    result = customer_service.get_customer_by_username("testuser")

    # Assert
    assert result == expected_customer


def test_update_customer_success(customer_service, mock_supabase):
    """
    Test the successful update of a customer.
    This test verifies that the `update_customer` method of the `customer_service`
    correctly updates a customer's information when provided with valid data.
    Args:
        customer_service: An instance of the customer service to be tested.
        mock_supabase: A mock instance of the Supabase client.
    Arrange:
        - Prepare the update data with a new email.
        - Mock the Supabase client's response to return the update data.
    Act:
        - Call the `update_customer` method with a test username and the update data.
    Assert:
        - Check that the result of the update operation matches the update data.
    """
    # Arrange
    update_data = {"email": "newemail@test.com"}
    mock_supabase.table().update().eq().execute.return_value.data = [update_data]

    # Act
    result = customer_service.update_customer("testuser", update_data)

    # Assert
    assert result == update_data


def test_delete_customer_success(customer_service, mock_supabase):
    """
    Test the successful deletion of a customer.
    This test verifies that the `delete_customer` method of the `customer_service`
    correctly deletes a customer when provided with a valid username.
    Args:
        customer_service (CustomerService): The customer service instance to be tested.
        mock_supabase (Mock): A mock instance of the Supabase client.
    Setup:
        - Mocks the Supabase client's delete operation to return an empty list,
          simulating a successful deletion.
    Test Steps:
        1. Call the `delete_customer` method with the username "testuser".
        2. Assert that the result is True, indicating a successful deletion.
    """
    # Arrange
    mock_supabase.table().delete().eq().execute.return_value.data = []

    # Act
    result = customer_service.delete_customer("testuser")

    # Assert
    assert result == True


def test_charge_wallet_success(customer_service, mock_supabase):
    """
    Test the successful charging of a customer's wallet.
    This test verifies that the `charge_wallet` method of the `customer_service`
    correctly updates the wallet balance when a valid amount is charged.
    Args:
        customer_service (CustomerService): The customer service instance to be tested.
        mock_supabase (Mock): A mock instance of the Supabase client.
    Arrange:
        - Set the current wallet balance to 100.
        - Set the amount to be charged to 50.
        - Mock the Supabase `select` method to return the current wallet balance.
        - Mock the Supabase `update` method to return the updated wallet balance.
    Act:
        - Call the `charge_wallet` method with the test user and the amount to be charged.
    Assert:
        - Verify that the result of the `charge_wallet` method is the updated wallet balance.
    """
    # Arrange
    current_balance = 100
    amount = 50
    mock_supabase.table().select().eq().execute.return_value.data = [
        {"wallet_balance": current_balance}
    ]
    mock_supabase.table().update().eq().execute.return_value.data = [
        {"wallet_balance": current_balance + amount}
    ]

    # Act
    result = customer_service.charge_wallet("testuser", amount)

    # Assert
    assert result == current_balance + amount


def test_deduct_wallet_insufficient_funds(customer_service, mock_supabase):
    """
    Test case for deducting an amount from the customer's wallet when there are insufficient funds.
    This test verifies that the `deduct_wallet` method of the `customer_service` raises a `ValueError`
    with the message "Insufficient funds" when attempting to deduct an amount greater than the available
    wallet balance.
    Args:
        customer_service: An instance of the customer service being tested.
        mock_supabase: A mock object for the Supabase client.
    Setup:
        - Mocks the Supabase client's response to return a wallet balance of 10 for the user.
    Test Steps:
        1. Attempt to deduct 20 from the wallet balance of the user "testuser".
        2. Assert that a `ValueError` is raised with the message "Insufficient funds".
    Raises:
        ValueError: If the wallet balance is insufficient to cover the deduction amount.
    """
    # Arrange
    mock_supabase.table().select().eq().execute.return_value.data = [
        {"wallet_balance": 10}
    ]

    # Act & Assert
    with pytest.raises(ValueError, match="Insufficient funds"):
        customer_service.deduct_wallet("testuser", 20)
