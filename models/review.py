from datetime import date


class Review:
    """
    A class to represent a product review.

    Attributes:
    ----------
    review_id : int, optional
        Unique identifier for the review (default is None).
    customer_id : int
        Unique identifier for the customer who wrote the review.
    product_id : int
        Unique identifier for the product being reviewed.
    rating : int
        Rating given by the customer (e.g., 1 to 5).
    comment : str, optional
        Text comment provided by the customer (default is None).
    review_date : date, optional
        Date when the review was written (default is today's date).
    status : str, optional
        Status of the review (e.g., "Pending", "Approved", "Rejected") (default is "Pending").

    Methods:
    -------
    __init__(self, customer_id, product_id, rating, comment=None, review_date=None, status=None, review_id=None):
        Constructs all the necessary attributes for the Review object.
    """

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
