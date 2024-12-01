from unittest.mock import Mock, patch

import pytest
from customer_service import CustomerService


@pytest.fixture
def mock_supabase():
    return Mock()


@pytest.fixture
def customer_service(mock_supabase):
    with patch("customer_service.get_supabase_client", return_value=mock_supabase):
        service = CustomerService()
        return service


def test_register_customer_success(customer_service, mock_supabase):
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
    # Arrange
    customer_data = {"username": "existinguser", "password": "password123"}
    mock_supabase.table().select().eq().execute.return_value.data = [
        {"username": "existinguser"}
    ]

    # Act & Assert
    with pytest.raises(ValueError, match="Username already exists"):
        customer_service.register_customer(customer_data)


def test_get_customer_by_username_success(customer_service, mock_supabase):
    # Arrange
    expected_customer = {"username": "testuser", "email": "test@test.com"}
    mock_supabase.table().select().eq().execute.return_value.data = [expected_customer]

    # Act
    result = customer_service.get_customer_by_username("testuser")

    # Assert
    assert result == expected_customer


def test_update_customer_success(customer_service, mock_supabase):
    # Arrange
    update_data = {"email": "newemail@test.com"}
    mock_supabase.table().update().eq().execute.return_value.data = [update_data]

    # Act
    result = customer_service.update_customer("testuser", update_data)

    # Assert
    assert result == update_data


def test_delete_customer_success(customer_service, mock_supabase):
    # Arrange
    mock_supabase.table().delete().eq().execute.return_value.data = []

    # Act
    result = customer_service.delete_customer("testuser")

    # Assert
    assert result == True


def test_charge_wallet_success(customer_service, mock_supabase):
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
    # Arrange
    mock_supabase.table().select().eq().execute.return_value.data = [
        {"wallet_balance": 10}
    ]

    # Act & Assert
    with pytest.raises(ValueError, match="Insufficient funds"):
        customer_service.deduct_wallet("testuser", 20)
