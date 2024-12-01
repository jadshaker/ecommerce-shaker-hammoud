from datetime import date

from marshmallow import Schema, fields, post_load, validate

from models.sale import Sale


class SaleSchema(Schema):
    """
    SaleSchema is a Marshmallow schema for serializing and deserializing Sale objects.

    Attributes:
        sale_id (int): The unique identifier for the sale. This field is read-only.
        customer_id (int): The unique identifier for the customer. This field is required.
        product_id (int): The unique identifier for the product. This field is required.
        sale_date (date): The date of the sale. This field is required and cannot be in the future.
        quantity (int): The quantity of the product sold. This field is required and must be at least 1.
        total_price (float): The total price of the sale. This field is required and must be non-negative.

    Methods:
        make_sale(data, **kwargs): A post-load method that creates a Sale object from the deserialized data.
    """
    sale_id = fields.Int(dump_only=True)
    customer_id = fields.Int(required=True)
    product_id = fields.Int(required=True)
    sale_date = fields.Date(
        required=True,
        validate=validate.Range(max=date.today()),
        error_messages={"validator_failed": "Sale date cannot be in the future"},
    )
    quantity = fields.Int(
        required=True,
        validate=validate.Range(min=1),
        error_messages={"validator_failed": "Quantity must be at least 1"},
    )
    total_price = fields.Float(
        required=True,
        validate=validate.Range(min=0),
        error_messages={"validator_failed": "Total price must be non-negative"},
    )

    @post_load
    def make_sale(self, data, **kwargs):
        return Sale(**data)


# Create an instance for easy access
sale_schema = SaleSchema()
sale_list_schema = SaleSchema(many=True)
