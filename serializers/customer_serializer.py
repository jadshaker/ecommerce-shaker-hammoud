from marshmallow import Schema, fields, post_load, validate
from marshmallow.validate import OneOf

from models.customer import Customer


class CustomerSchema(Schema):
    """
    CustomerSchema is a Marshmallow schema for serializing and deserializing customer data.

    Attributes:
        customer_id (int): The unique identifier for the customer. This field is read-only.
        full_name (str): The full name of the customer. Must be between 2 and 100 characters.
        username (str): The username of the customer. Must be between 3 and 50 characters.
        password (str): The password for the customer account. Must be at least 8 characters long. This field is write-only.
        age (int): The age of the customer. Must be between 18 and 120.
        address (str, optional): The address of the customer. Can be None and must be at most 200 characters.
        gender (str, optional): The gender of the customer. Must be one of "Male", "Female", or "Other". Can be None.
        marital_status (str, optional): The marital status of the customer. Must be one of "Single", "Married", "Divorced", or "Widowed". Can be None.
        wallet_balance (float): The wallet balance of the customer. This field is read-only.
        created_at (datetime): The timestamp when the customer was created. This field is read-only.

    Methods:
        make_customer(data, **kwargs): Creates a Customer instance from the deserialized data.
    """
    customer_id = fields.Int(dump_only=True)
    full_name = fields.Str(
        required=True,
        validate=validate.Length(min=2, max=100),
        error_messages={
            "validator_failed": "Full name must be between 2 and 100 characters"
        },
    )
    username = fields.Str(
        required=True,
        validate=validate.Length(min=3, max=50),
        error_messages={
            "validator_failed": "Username must be between 3 and 50 characters"
        },
    )
    password = fields.Str(
        required=True,
        validate=validate.Length(min=8),
        load_only=True,
        error_messages={
            "validator_failed": "Password must be at least 8 characters long"
        },
    )
    age = fields.Int(
        required=True,
        validate=validate.Range(min=18, max=120),
        error_messages={"validator_failed": "Age must be between 18 and 120"},
    )
    address = fields.Str(allow_none=True, validate=validate.Length(max=200))
    gender = fields.Str(
        validate=OneOf(["Male", "Female", "Other"]),
        allow_none=True,
        error_messages={"validator_failed": "Gender must be Male, Female, or Other"},
    )
    marital_status = fields.Str(
        validate=OneOf(["Single", "Married", "Divorced", "Widowed"]),
        allow_none=True,
        error_messages={"validator_failed": "Invalid marital status"},
    )
    wallet_balance = fields.Float(dump_only=True)
    created_at = fields.DateTime(dump_only=True)

    @post_load
    def make_customer(self, data, **kwargs):
        return Customer(**data)


# Create schema instances
customer_schema = CustomerSchema()
customers_schema = CustomerSchema(many=True)
