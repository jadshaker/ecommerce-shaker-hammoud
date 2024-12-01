import datetime
from datetime import date, timedelta

import pytest
from marshmallow import ValidationError

from models.review import Review
from serializers.review_serializer import ReviewSchema


@pytest.fixture
def valid_review_data():
    """
    Fixture that provides valid review data for testing.

    This fixture returns a dictionary containing the following keys:
    - customer_id: The ID of the customer who wrote the review.
    - product_id: The ID of the product being reviewed.
    - rating: The rating given to the product (e.g., 5).
    - comment: The comment provided by the customer (e.g., "Great product!").
    - review_date: The date when the review was written (e.g., "2024-11-30").
    - status: The status of the review (e.g., "Approved").

    Returns:
        dict: A dictionary containing valid review data.
    """
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
    """
    Fixture that provides invalid review data for testing purposes.

    Returns:
        dict: A dictionary containing the following invalid review data:
            - customer_id (int): The ID of the customer.
            - product_id (int): The ID of the product.
            - rating (int): An invalid rating value (greater than the maximum allowed).
            - comment (str): A comment about the product.
            - review_date (date): A future date, which is invalid for a review.
            - status (str): An invalid status value.
    """
    return {
        "customer_id": 1,
        "product_id": 1,
        "rating": 6,  # Invalid rating
        "comment": "Great product!",
        "review_date": date.today() + timedelta(days=1),  # Future date
        "status": "Unknown",  # Invalid status
    }


def test_valid_review_serialization(valid_review_data):
    """
    Test the serialization of a valid review.

    This test ensures that the ReviewSchema correctly deserializes valid review data
    into a Review object and that all fields are accurately populated.

    Args:
        valid_review_data (dict): A dictionary containing valid review data with the following keys:
            - customer_id (int): The ID of the customer who wrote the review.
            - product_id (int): The ID of the product being reviewed.
            - rating (int): The rating given by the customer.
            - comment (str): The comment provided by the customer.
            - review_date (str): The date the review was written in the format 'YYYY-MM-DD'.
            - status (str): The status of the review.

    Asserts:
        - The result is an instance of the Review class.
        - The customer_id of the result matches the input data.
        - The product_id of the result matches the input data.
        - The rating of the result matches the input data.
        - The comment of the result matches the input data.
        - The review_date of the result matches the input data, converted to a date object.
        - The status of the result matches the input data.
    """
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
    """
    Test the serialization of invalid review data.

    This test ensures that the `ReviewSchema` correctly raises a `ValidationError`
    when provided with invalid review data. It checks that the error messages
    include the expected fields: "rating", "review_date", and "status".

    Args:
        invalid_review_data (dict): A dictionary containing invalid review data.

    Raises:
        ValidationError: If the review data does not meet the schema requirements.
    """
    schema = ReviewSchema()
    with pytest.raises(ValidationError) as excinfo:
        schema.load(invalid_review_data)
    errors = excinfo.value.messages
    assert "rating" in errors
    assert "review_date" in errors
    assert "status" in errors


def test_missing_required_fields():
    """
    Test that the ReviewSchema raises a ValidationError when required fields are missing.

    This test ensures that the schema correctly identifies and reports missing required fields.
    It attempts to load an empty dictionary and checks that the appropriate validation errors
    are raised for the following fields:
    - customer_id
    - product_id
    - rating
    - review_date

    The test asserts that these fields are present in the error messages.
    """
    schema = ReviewSchema()
    with pytest.raises(ValidationError) as excinfo:
        schema.load({})
    errors = excinfo.value.messages
    assert "customer_id" in errors
    assert "product_id" in errors
    assert "rating" in errors
    assert "review_date" in errors
