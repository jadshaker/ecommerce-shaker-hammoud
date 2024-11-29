from marshmallow import Schema, fields, validate, post_load
from models.sale import Sale
from datetime import date

class SaleSchema(Schema):
    sale_id = fields.Int(dump_only=True)
    customer_id = fields.Int(required=True)
    product_id = fields.Int(required=True)
    sale_date = fields.Date(
        required=True, 
        validate=validate.Range(max=date.today()),
        error_messages={'validator_failed': 'Sale date cannot be in the future'}
    )
    quantity = fields.Int(
        required=True,
        validate=validate.Range(min=1),
        error_messages={'validator_failed': 'Quantity must be at least 1'}
    )
    total_price = fields.Float(
        required=True,
        validate=validate.Range(min=0),
        error_messages={'validator_failed': 'Total price must be non-negative'}
    )

    @post_load
    def make_sale(self, data, **kwargs):
        return Sale(**data)

# Create an instance for easy access
sale_schema = SaleSchema()
sale_list_schema = SaleSchema(many=True)