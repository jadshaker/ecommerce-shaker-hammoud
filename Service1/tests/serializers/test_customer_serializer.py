import pytest
from marshmallow import ValidationError

from serializers.customer_serializer import CustomerSchema


@pytest.fixture
def valid_customer_data():
    """
    Generate a dictionary containing valid customer data for testing purposes.

    Returns:
        dict: A dictionary with the following keys:
            - full_name (str): The full name of the customer.
            - username (str): The username of the customer.
            - password (str): The password of the customer.
            - age (int): The age of the customer.
            - address (str): The address of the customer.
            - gender (str): The gender of the customer.
            - marital_status (str): The marital status of the customer.
    """
    return {
        "full_name": "John Doe",
        "username": "johndoe",
        "password": "securepassword123",
        "age": 30,
        "address": "123 Main St",
        "gender": "Male",
        "marital_status": "Single",
    }


@pytest.fixture
def invalid_customer_data():
    """
    Generates a dictionary containing invalid customer data for testing purposes.

    Returns:
        dict: A dictionary with the following invalid customer data:
            - full_name (str): A name that is too short.
            - username (str): A username that is too short.
            - password (str): A password that is too short.
            - age (int): An age that is below the valid threshold.
            - address (str): An address that exceeds the maximum allowed length.
            - gender (str): A gender value that is not recognized.
            - marital_status (str): A marital status that is not recognized.
    """
    return {
        "full_name": "J",
        "username": "jd",
        "password": "123",
        "age": 17,
        "address": "A" * 201,
        "gender": "Unknown",
        "marital_status": "Complicated",
    }


def test_valid_customer_data(valid_customer_data):
    """
    Test the CustomerSchema with valid customer data.

    This test ensures that the CustomerSchema correctly loads and validates
    a dictionary of valid customer data, and that the resulting object has
    the expected attributes.

    Args:
        valid_customer_data (dict): A dictionary containing valid customer data
            with keys "full_name", "username", "password", "age", "address",
            "gender", and "marital_status".

    Asserts:
        The resulting object's attributes match the corresponding values in
        the valid_customer_data dictionary.
    """
    schema = CustomerSchema()
    result = schema.load(valid_customer_data)
    assert result.full_name == valid_customer_data["full_name"]
    assert result.username == valid_customer_data["username"]
    assert result.password == valid_customer_data["password"]
    assert result.age == valid_customer_data["age"]
    assert result.address == valid_customer_data["address"]
    assert result.gender == valid_customer_data["gender"]
    assert result.marital_status == valid_customer_data["marital_status"]


def test_invalid_customer_data(invalid_customer_data):
    """
    Test case for validating customer data with invalid inputs.

    This test ensures that the CustomerSchema correctly raises a ValidationError
    when provided with invalid customer data. It checks that the error messages
    contain the expected fields: "full_name", "username", "password", "age",
    "address", "gender", and "marital_status".

    Args:
        invalid_customer_data (dict): A dictionary containing invalid customer data.

    Raises:
        ValidationError: If the customer data does not meet the schema requirements.
    """
    schema = CustomerSchema()
    with pytest.raises(ValidationError) as excinfo:
        schema.load(invalid_customer_data)
    errors = excinfo.value.messages
    assert "full_name" in errors
    assert "username" in errors
    assert "password" in errors
    assert "age" in errors
    assert "address" in errors
    assert "gender" in errors
    assert "marital_status" in errors


def test_missing_required_fields():
    """
    Test that the CustomerSchema raises a ValidationError when required fields are missing.

    This test ensures that the schema correctly identifies and reports missing required fields.
    It attempts to load an empty dictionary and checks that the appropriate validation errors
    are raised for the required fields: 'full_name', 'username', 'password', and 'age'.

    Assertions:
        - 'full_name' is in the error messages.
        - 'username' is in the error messages.
        - 'password' is in the error messages.
        - 'age' is in the error messages.
    """
    schema = CustomerSchema()
    with pytest.raises(ValidationError) as excinfo:
        schema.load({})
    errors = excinfo.value.messages
    assert "full_name" in errors
    assert "username" in errors
    assert "password" in errors
    assert "age" in errors


def test_optional_fields(valid_customer_data):
    """
    Test the optional fields in the CustomerSchema.

    This test ensures that the 'address', 'gender', and 'marital_status' fields
    are optional in the CustomerSchema. It removes these fields from the 
    valid_customer_data and verifies that the schema can still load the data 
    correctly, setting the missing fields to None.

    Args:
        valid_customer_data (dict): A dictionary containing valid customer data.

    Asserts:
        The 'address', 'gender', and 'marital_status' fields are set to None 
        when they are not present in the input data.
    """
    valid_customer_data.pop("address")
    valid_customer_data.pop("gender")
    valid_customer_data.pop("marital_status")
    schema = CustomerSchema()
    result = schema.load(valid_customer_data)
    assert result.address is None
    assert result.gender is None
    assert result.marital_status is None
