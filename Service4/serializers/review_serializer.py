from datetime import date

from marshmallow import Schema, fields, post_load, validate

from models.review import Review


class ReviewSchema(Schema):
    """
    ReviewSchema is a Marshmallow schema for validating and serializing review data.

    Attributes:
        review_id (int): The unique identifier of the review. This field is read-only.
        customer_id (int): The unique identifier of the customer. This field is required.
        product_id (int): The unique identifier of the product. This field is required.
        rating (int): The rating given by the customer. This field is required and must be between 1 and 5.
        comment (str): The comment provided by the customer. This field is optional.
        review_date (date): The date when the review was made. This field is required and cannot be in the future.
        status (str): The status of the review. This field must be one of "Pending", "Approved", or "Rejected".

    Methods:
        make_review(data, **kwargs): A post-load method that creates a Review instance from the validated data.
    """
    review_id = fields.Int(dump_only=True)
    customer_id = fields.Int(required=True)
    product_id = fields.Int(required=True)
    rating = fields.Int(
        required=True,
        validate=validate.Range(min=1, max=5),
        error_messages={"validator_failed": "Rating must be between 1 and 5"},
    )
    comment = fields.Str(allow_none=True)
    review_date = fields.Date(
        required=True,
        validate=validate.Range(max=date.today()),
        error_messages={"validator_failed": "Review date cannot be in the future"},
    )
    status = fields.Str(
        validate=validate.OneOf(["Pending", "Approved", "Rejected"]),
        error_messages={"validator_failed": "Invalid review status"},
    )

    @post_load
    def make_review(self, data, **kwargs):
        return Review(**data)


# Create an instance for easy access
review_schema = ReviewSchema()
review_list_schema = ReviewSchema(many=True)
