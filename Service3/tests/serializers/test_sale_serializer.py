from datetime import date, timedelta

import pytest
from marshmallow import ValidationError

from models.sale import Sale
from serializers.sale_serializer import sale_schema


def test_sale_serializer_valid_data():
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
    invalid_data = {
        "customer_id": 1,
        "product_id": 2,
        "sale_date": date.today().isoformat(),
        "quantity": 5,
        "total_price": -10.0,
    }
    with pytest.raises(ValidationError) as excinfo:
        sale_schema.load(invalid_data)
