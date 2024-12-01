import pytest
from marshmallow import ValidationError

from models.product import Product
from serializers.product_serializer import ProductSchema


@pytest.fixture
def valid_product_data():
    return {
        "name": "Test Product",
        "category": "Test Category",
        "price": 19.99,
        "description": "A test product",
        "stock_count": 10,
    }


@pytest.fixture
def invalid_product_data():
    return {
        "name": "",
        "category": "Test Category",
        "price": -1,
        "description": "A test product",
        "stock_count": -5,
    }


def test_product_schema_valid_data(valid_product_data):
    schema = ProductSchema()
    result = schema.load(valid_product_data)
    assert isinstance(result, Product)
    assert result.name == valid_product_data["name"]
    assert result.category == valid_product_data["category"]
    assert result.price == valid_product_data["price"]
    assert result.description == valid_product_data["description"]
    assert result.stock_count == valid_product_data["stock_count"]


def test_product_schema_invalid_data(invalid_product_data):
    schema = ProductSchema()
    with pytest.raises(ValidationError) as excinfo:
        schema.load(invalid_product_data)
    errors = excinfo.value.messages
    assert "name" in errors
    assert "price" in errors
    assert "stock_count" in errors


def test_product_schema_missing_required_fields():
    schema = ProductSchema()
    with pytest.raises(ValidationError) as excinfo:
        schema.load({})
    errors = excinfo.value.messages
    assert "name" in errors
    assert "category" in errors
    assert "price" in errors
    assert "stock_count" in errors


def test_product_schema_optional_description(valid_product_data):
    valid_product_data.pop("description")
    schema = ProductSchema()
    result = schema.load(valid_product_data)
    assert isinstance(result, Product)
    assert result.description is None
