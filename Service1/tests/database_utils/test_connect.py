from unittest.mock import MagicMock, patch

import pytest

from database_utils.connect import DatabaseConnection, get_supabase_client


@pytest.fixture
def mock_create_client():
    """
    Fixture to mock the `create_client` function from the `database_utils.connect` module.

    This fixture uses the `patch` function from the `unittest.mock` module to replace the
    `create_client` function with a mock object for the duration of the test. The mock object
    is yielded to the test function, allowing it to be used and inspected within the test.

    Yields:
        unittest.mock.MagicMock: A mock object that replaces the `create_client` function.
    """
    with patch("database_utils.connect.create_client") as mock:
        yield mock


def test_get_instance_creates_client(mock_create_client):
    """
    Test that `get_instance` method of `DatabaseConnection` creates and returns a client instance.

    Args:
        mock_create_client (MagicMock): Mock object for the client creation method.

    Asserts:
        The client instance created by `get_instance` is not None.
    """
    mock_create_client.return_value = MagicMock()
    client = DatabaseConnection.get_instance()
    assert client is not None


def test_get_instance_returns_existing_client(mock_create_client):
    """
    Test that `DatabaseConnection.get_instance` returns the same client instance
    when called multiple times.

    Args:
        mock_create_client (MagicMock): A mock object for the client creation method.

    Setup:
        - Mocks the client creation method to return a MagicMock instance.

    Test:
        - Calls `DatabaseConnection.get_instance` twice.
        - Asserts that both calls return the same client instance.
    """
    mock_create_client.return_value = MagicMock()
    first_client = DatabaseConnection.get_instance()
    second_client = DatabaseConnection.get_instance()
    assert first_client is second_client


def test_get_supabase_client(mock_create_client):
    """
    Test the `get_supabase_client` function.

    This test ensures that the `get_supabase_client` function returns a non-None client object.
    It uses a mock for the `create_client` function to simulate the creation of the client.

    Args:
        mock_create_client (MagicMock): A mock object for the `create_client` function.

    Asserts:
        The client returned by `get_supabase_client` is not None.
    """
    mock_create_client.return_value = MagicMock()
    client = get_supabase_client()
    assert client is not None
