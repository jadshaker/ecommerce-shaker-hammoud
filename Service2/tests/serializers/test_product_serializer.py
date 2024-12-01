import pytest
from marshmallow import ValidationError

from models.product import Product
from serializers.product_serializer import ProductSchema


@pytest.fixture
def valid_product_data():
    """
    Generates a dictionary containing valid product data for testing purposes.

    Returns:
        dict: A dictionary with the following keys:
            - name (str): The name of the product.
            - category (str): The category of the product.
            - price (float): The price of the product.
            - description (str): A brief description of the product.
            - stock_count (int): The number of items in stock.
    """
    return {
        "name": "Test Product",
        "category": "Test Category",
        "price": 19.99,
        "description": "A test product",
        "stock_count": 10,
    }


@pytest.fixture
def invalid_product_data():
    """
    Generates a dictionary containing invalid product data for testing purposes.

    Returns:
        dict: A dictionary with the following invalid product fields:
            - name (str): An empty string representing an invalid product name.
            - category (str): A string representing the product category.
            - price (int): A negative integer representing an invalid product price.
            - description (str): A string representing the product description.
            - stock_count (int): A negative integer representing an invalid stock count.
    """
    return {
        "name": "",
        "category": "Test Category",
        "price": -1,
        "description": "A test product",
        "stock_count": -5,
    }


def test_product_schema_valid_data(valid_product_data):
    """
    Test the ProductSchema with valid product data.

    This test ensures that the ProductSchema correctly deserializes valid product data
    into a Product object and that all fields are accurately populated.

    Args:
        valid_product_data (dict): A dictionary containing valid product data.

    Asserts:
        - The result is an instance of the Product class.
        - The name field of the result matches the name in valid_product_data.
        - The category field of the result matches the category in valid_product_data.
        - The price field of the result matches the price in valid_product_data.
        - The description field of the result matches the description in valid_product_data.
        - The stock_count field of the result matches the stock_count in valid_product_data.
    """
    schema = ProductSchema()
    result = schema.load(valid_product_data)
    assert isinstance(result, Product)
    assert result.name == valid_product_data["name"]
    assert result.category == valid_product_data["category"]
    assert result.price == valid_product_data["price"]
    assert result.description == valid_product_data["description"]
    assert result.stock_count == valid_product_data["stock_count"]


def test_product_schema_invalid_data(invalid_product_data):
    """
    Test that the ProductSchema raises a ValidationError when provided with invalid data.

    Args:
        invalid_product_data (dict): A dictionary containing invalid product data.

    Raises:
        ValidationError: If the schema validation fails.

    Asserts:
        - The error messages contain "name".
        - The error messages contain "price".
        - The error messages contain "stock_count".
    """
    schema = ProductSchema()
    with pytest.raises(ValidationError) as excinfo:
        schema.load(invalid_product_data)
    errors = excinfo.value.messages
    assert "name" in errors
    assert "price" in errors
    assert "stock_count" in errors


def test_product_schema_missing_required_fields():
    """
    Test that the ProductSchema raises a ValidationError when required fields are missing.

    This test ensures that the schema correctly identifies and reports missing required fields
    when an empty dictionary is passed to the `load` method. The required fields are:
    - name
    - category
    - price
    - stock_count

    The test asserts that the ValidationError contains error messages for each of these fields.
    """
    schema = ProductSchema()
    with pytest.raises(ValidationError) as excinfo:
        schema.load({})
    errors = excinfo.value.messages
    assert "name" in errors
    assert "category" in errors
    assert "price" in errors
    assert "stock_count" in errors


def test_product_schema_optional_description(valid_product_data):
    """
    Test that the ProductSchema correctly handles the absence of the 'description' field.

    This test ensures that when the 'description' field is omitted from the input data,
    the schema can still successfully load the data and create a Product instance with
    the 'description' attribute set to None.

    Args:
        valid_product_data (dict): A dictionary containing valid product data.

    Asserts:
        - The result is an instance of the Product class.
        - The 'description' attribute of the result is None.
    """
    valid_product_data.pop("description")
    schema = ProductSchema()
    result = schema.load(valid_product_data)
    assert isinstance(result, Product)
    assert result.description is None
