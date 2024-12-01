from unittest.mock import MagicMock, patch

import pytest

from database_utils.connect import DatabaseConnection, get_supabase_client


@pytest.fixture
def mock_create_client():
    with patch("database_utils.connect.create_client") as mock:
        yield mock


def test_get_instance_creates_client(mock_create_client):
    mock_create_client.return_value = MagicMock()
    client = DatabaseConnection.get_instance()
    assert client is not None


def test_get_instance_returns_existing_client(mock_create_client):
    mock_create_client.return_value = MagicMock()
    first_client = DatabaseConnection.get_instance()
    second_client = DatabaseConnection.get_instance()
    assert first_client is second_client


def test_get_supabase_client(mock_create_client):
    mock_create_client.return_value = MagicMock()
    client = get_supabase_client()
    assert client is not None
