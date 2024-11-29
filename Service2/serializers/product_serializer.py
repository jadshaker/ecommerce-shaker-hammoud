from marshmallow import Schema, fields, validate, post_load
from models.product import Product

class ProductSchema(Schema):
    product_id = fields.Int(dump_only=True)
    name = fields.Str(
        required=True, 
        validate=validate.Length(min=1, max=255),
        error_messages={'validator_failed': 'Product name must be between 1 and 255 characters'}
    )
    category = fields.Str(
        required=True, 
        validate=validate.Length(max=255),
        error_messages={'validator_failed': 'Category must be less than 255 characters'}
    )
    price = fields.Float(
        required=True,
        validate=validate.Range(min=0),
        error_messages={'validator_failed': 'Price must be non-negative'}
    )
    description = fields.Str(allow_none=True)
    stock_count = fields.Int(
        required=True,
        validate=validate.Range(min=0),
        error_messages={'validator_failed': 'Stock count must be non-negative'}
    )

    @post_load
    def make_product(self, data, **kwargs):
        return Product(**data)

# Create an instance for easy access
product_schema = ProductSchema()
product_list_schema = ProductSchema(many=True)