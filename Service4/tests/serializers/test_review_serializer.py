import datetime
from datetime import date, timedelta

import pytest
from marshmallow import ValidationError

from models.review import Review
from serializers.review_serializer import ReviewSchema


@pytest.fixture
def valid_review_data():
    return {
        "customer_id": 1,
        "product_id": 1,
        "rating": 5,
        "comment": "Great product!",
        "review_date": "2024-11-30",
        "status": "Approved",
    }


@pytest.fixture
def invalid_review_data():
    return {
        "customer_id": 1,
        "product_id": 1,
        "rating": 6,  # Invalid rating
        "comment": "Great product!",
        "review_date": date.today() + timedelta(days=1),  # Future date
        "status": "Unknown",  # Invalid status
    }


def test_valid_review_serialization(valid_review_data):
    schema = ReviewSchema()
    result = schema.load(valid_review_data)
    assert isinstance(result, Review)
    assert result.customer_id == valid_review_data["customer_id"]
    assert result.product_id == valid_review_data["product_id"]
    assert result.rating == valid_review_data["rating"]
    assert result.comment == valid_review_data["comment"]
    assert (
        result.review_date
        == datetime.datetime.strptime(
            valid_review_data["review_date"], "%Y-%m-%d"
        ).date()
    )
    assert result.status == valid_review_data["status"]


def test_invalid_review_serialization(invalid_review_data):
    schema = ReviewSchema()
    with pytest.raises(ValidationError) as excinfo:
        schema.load(invalid_review_data)
    errors = excinfo.value.messages
    assert "rating" in errors
    assert "review_date" in errors
    assert "status" in errors


def test_missing_required_fields():
    schema = ReviewSchema()
    with pytest.raises(ValidationError) as excinfo:
        schema.load({})
    errors = excinfo.value.messages
    assert "customer_id" in errors
    assert "product_id" in errors
    assert "rating" in errors
    assert "review_date" in errors
