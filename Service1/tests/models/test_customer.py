import pytest

from models.customer import Customer


@pytest.fixture
def customer():
    """
    Fixture for creating a Customer instance for testing purposes.

    Returns:
        Customer: A Customer instance with predefined attributes.
    """
    return Customer(
        full_name="John Doe", username="johndoe", password="password", age=25
    )


def test_customer_instance(customer):
    """
    Test that the given customer instance is of type Customer.

    Args:
        customer (Customer): The customer instance to be tested.

    Asserts:
        bool: True if the customer is an instance of Customer, False otherwise.
    """
    assert isinstance(customer, Customer)


def test_customer_attributes(customer):
    """
    Test the attributes of the Customer model.

    This test verifies that the attributes of a Customer instance are correctly set to their expected values.

    Args:
        customer (Customer): An instance of the Customer model to be tested.

    Assertions:
        - The full_name attribute should be "John Doe".
        - The username attribute should be "johndoe".
        - The password attribute should be "password".
        - The age attribute should be 25.
        - The address attribute should be None.
        - The gender attribute should be None.
        - The marital_status attribute should be None.
        - The wallet_balance attribute should be 0.0.
        - The customer_id attribute should be None.
        - The created_at attribute should not be None.
        - The customer_id attribute should be None.
    """
    assert customer.full_name == "John Doe"
    assert customer.username == "johndoe"
    assert customer.password == "password"
    assert customer.age == 25
    assert customer.address is None
    assert customer.gender is None
    assert customer.marital_status is None
    assert customer.wallet_balance == 0.0
    assert customer.customer_id is None
    assert customer.created_at is not None
    assert customer.customer_id is None
