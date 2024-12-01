from datetime import date

from models.review import Review


def test_review_initialization():
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
    review = Review(customer_id=2, product_id=102, rating=4)
    assert review.review_id is None
    assert review.customer_id == 2
    assert review.product_id == 102
    assert review.rating == 4
    assert review.comment is None
    assert review.review_date == date.today()
    assert review.status == "Pending"


def test_review_optional_fields():
    review = Review(customer_id=3, product_id=103, rating=3, comment="Average product")
    assert review.comment == "Average product"
    assert review.review_date == date.today()
    assert review.status == "Pending"
