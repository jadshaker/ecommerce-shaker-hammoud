from datetime import date, timedelta

import pytest
from marshmallow import ValidationError

from models.sale import Sale
from serializers.sale_serializer import sale_schema


def test_sale_serializer_valid_data():
    """
    Test the sale serializer with valid data.

    This test ensures that the sale serializer correctly processes valid input data
    and returns a Sale object with the expected attributes.

    Test case:
    - Valid data dictionary containing customer_id, product_id, sale_date, quantity, and total_price.
    - Asserts that the result is an instance of the Sale class.
    - Asserts that the attributes of the result match the input data.

    Expected result:
    - The serializer should successfully load the valid data and create a Sale object.
    - The attributes of the Sale object should match the input data.
    """
    valid_data = {
        "customer_id": 1,
        "product_id": 2,
        "sale_date": date.today().isoformat(),
        "quantity": 5,
        "total_price": 100.0,
    }
    result = sale_schema.load(valid_data)
    assert isinstance(result, Sale)
    assert result.customer_id == 1
    assert result.product_id == 2
    assert result.sale_date == date.today()
    assert result.quantity == 5
    assert result.total_price == 100.0


def test_sale_serializer_invalid_future_date():
    """
    Test case for validating the sale serializer with an invalid future sale date.

    This test ensures that the serializer raises a ValidationError when attempting
    to serialize a sale with a sale_date set in the future.

    Test Steps:
    1. Create a dictionary `invalid_data` with the following keys:
        - customer_id: ID of the customer (integer).
        - product_id: ID of the product (integer).
        - sale_date: A date set to tomorrow (future date).
        - quantity: Quantity of the product sold (integer).
        - total_price: Total price of the sale (float).
    2. Attempt to load the `invalid_data` using the `sale_schema`.
    3. Verify that a ValidationError is raised due to the future sale_date.

    Expected Result:
    A ValidationError should be raised indicating that the sale_date cannot be in the future.
    """
    invalid_data = {
        "customer_id": 1,
        "product_id": 2,
        "sale_date": (date.today() + timedelta(days=1)).isoformat(),
        "quantity": 5,
        "total_price": 100.0,
    }
    with pytest.raises(ValidationError) as excinfo:
        sale_schema.load(invalid_data)


def test_sale_serializer_invalid_quantity():
    """
    Test case for validating the SaleSerializer with an invalid quantity.

    This test ensures that the serializer raises a ValidationError when the quantity
    is set to an invalid value (e.g., 0). The test provides a dictionary with the
    necessary fields and an invalid quantity, then attempts to load the data using
    the sale_schema. If the serializer correctly identifies the invalid quantity,
    it will raise a ValidationError.

    Raises:
        ValidationError: If the quantity is invalid (e.g., 0).
    """
    invalid_data = {
        "customer_id": 1,
        "product_id": 2,
        "sale_date": date.today().isoformat(),
        "quantity": 0,
        "total_price": 100.0,
    }
    with pytest.raises(ValidationError) as excinfo:
        sale_schema.load(invalid_data)


def test_sale_serializer_invalid_total_price():
    """
    Test case for validating the SaleSerializer with an invalid total price.

    This test ensures that the serializer raises a ValidationError when the 
    total_price field is negative, which is considered invalid.

    Test Steps:
    1. Define a dictionary `invalid_data` with a negative `total_price`.
    2. Attempt to load the `invalid_data` using the `sale_schema`.
    3. Verify that a ValidationError is raised.

    Expected Result:
    A ValidationError should be raised indicating that the total_price cannot be negative.
    """
    invalid_data = {
        "customer_id": 1,
        "product_id": 2,
        "sale_date": date.today().isoformat(),
        "quantity": 5,
        "total_price": -10.0,
    }
    with pytest.raises(ValidationError) as excinfo:
        sale_schema.load(invalid_data)
