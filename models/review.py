# models/review.py
from datetime import date


class Review:
    def __init__(
        self,
        customer_id,
        product_id,
        rating,
        comment=None,
        review_date=None,
        status=None,
        review_id=None,
    ):
        self.review_id = review_id
        self.customer_id = customer_id
        self.product_id = product_id
        self.rating = rating
        self.comment = comment
        self.review_date = review_date or date.today()
        self.status = status or "Pending"
