from datetime import date

from models.review import Review


def test_review_initialization():
    """
    Test the initialization of the Review model.

    This test verifies that a Review object is correctly initialized with the given parameters.

    Assertions:
        - The review_id is correctly set to 1001.
        - The customer_id is correctly set to 1.
        - The product_id is correctly set to 101.
        - The rating is correctly set to 5.
        - The comment is correctly set to "Great product!".
        - The review_date is correctly set to October 1, 2023.
        - The status is correctly set to "Approved".
    """
    review = Review(
        customer_id=1,
        product_id=101,
        rating=5,
        comment="Great product!",
        review_date=date(2023, 10, 1),
        status="Approved",
        review_id=1001,
    )
    assert review.review_id == 1001
    assert review.customer_id == 1
    assert review.product_id == 101
    assert review.rating == 5
    assert review.comment == "Great product!"
    assert review.review_date == date(2023, 10, 1)
    assert review.status == "Approved"


def test_review_default_values():
    """
    Test the default values of the Review model.

    This test ensures that when a Review object is created with only the required fields
    (customer_id, product_id, and rating), the default values for the optional fields
    are correctly set.

    Assertions:
        - review_id should be None by default.
        - customer_id should be set to the provided value (2).
        - product_id should be set to the provided value (102).
        - rating should be set to the provided value (4).
        - comment should be None by default.
        - review_date should be set to the current date by default.
        - status should be "Pending" by default.
    """
    review = Review(customer_id=2, product_id=102, rating=4)
    assert review.review_id is None
    assert review.customer_id == 2
    assert review.product_id == 102
    assert review.rating == 4
    assert review.comment is None
    assert review.review_date == date.today()
    assert review.status == "Pending"


def test_review_optional_fields():
    """
    Test the creation of a Review object with optional fields.

    This test verifies that a Review object is correctly instantiated with the provided
    customer_id, product_id, rating, and comment. It also checks that the default values
    for the optional fields (review_date and status) are correctly set.

    Assertions:
        - The comment field should be set to "Average product".
        - The review_date field should be set to the current date.
        - The status field should be set to "Pending".
    """
    review = Review(customer_id=3, product_id=103, rating=3, comment="Average product")
    assert review.comment == "Average product"
    assert review.review_date == date.today()
    assert review.status == "Pending"
