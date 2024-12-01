import pytest
from marshmallow import ValidationError

from serializers.customer_serializer import CustomerSchema


@pytest.fixture
def valid_customer_data():
    return {
        "full_name": "John Doe",
        "username": "johndoe",
        "password": "securepassword123",
        "age": 30,
        "address": "123 Main St",
        "gender": "Male",
        "marital_status": "Single",
    }


@pytest.fixture
def invalid_customer_data():
    return {
        "full_name": "J",
        "username": "jd",
        "password": "123",
        "age": 17,
        "address": "A" * 201,
        "gender": "Unknown",
        "marital_status": "Complicated",
    }


def test_valid_customer_data(valid_customer_data):
    schema = CustomerSchema()
    result = schema.load(valid_customer_data)
    assert result.full_name == valid_customer_data["full_name"]
    assert result.username == valid_customer_data["username"]
    assert result.password == valid_customer_data["password"]
    assert result.age == valid_customer_data["age"]
    assert result.address == valid_customer_data["address"]
    assert result.gender == valid_customer_data["gender"]
    assert result.marital_status == valid_customer_data["marital_status"]


def test_invalid_customer_data(invalid_customer_data):
    schema = CustomerSchema()
    with pytest.raises(ValidationError) as excinfo:
        schema.load(invalid_customer_data)
    errors = excinfo.value.messages
    assert "full_name" in errors
    assert "username" in errors
    assert "password" in errors
    assert "age" in errors
    assert "address" in errors
    assert "gender" in errors
    assert "marital_status" in errors


def test_missing_required_fields():
    schema = CustomerSchema()
    with pytest.raises(ValidationError) as excinfo:
        schema.load({})
    errors = excinfo.value.messages
    assert "full_name" in errors
    assert "username" in errors
    assert "password" in errors
    assert "age" in errors


def test_optional_fields(valid_customer_data):
    valid_customer_data.pop("address")
    valid_customer_data.pop("gender")
    valid_customer_data.pop("marital_status")
    schema = CustomerSchema()
    result = schema.load(valid_customer_data)
    assert result.address is None
    assert result.gender is None
    assert result.marital_status is None
