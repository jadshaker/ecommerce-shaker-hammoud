from marshmallow import Schema, fields, validate, post_load
from marshmallow.validate import OneOf
from models.customer import Customer
from datetime import datetime

class CustomerSchema(Schema):
    customer_id = fields.Int(dump_only=True)
    full_name = fields.Str(
        required=True, 
        validate=validate.Length(min=2, max=100),
        error_messages={'validator_failed': 'Full name must be between 2 and 100 characters'}
    )
    username = fields.Str(
        required=True, 
        validate=validate.Length(min=3, max=50),
        error_messages={'validator_failed': 'Username must be between 3 and 50 characters'}
    )
    password = fields.Str(
        required=True, 
        validate=validate.Length(min=8),
        load_only=True,
        error_messages={'validator_failed': 'Password must be at least 8 characters long'}
    )
    age = fields.Int(
        required=True, 
        validate=validate.Range(min=18, max=120),
        error_messages={'validator_failed': 'Age must be between 18 and 120'}
    )
    address = fields.Str(allow_none=True, validate=validate.Length(max=200))
    gender = fields.Str(
        validate=OneOf(['Male', 'Female', 'Other']),
        allow_none=True,
        error_messages={'validator_failed': 'Gender must be Male, Female, or Other'}
    )
    wallet_balance = fields.Float(dump_only=True)
    
    @post_load
    def make_customer(self, data, **kwargs):
        return Customer(**data)

# Create schema instances
customer_schema = CustomerSchema()
customers_schema = CustomerSchema(many=True)
