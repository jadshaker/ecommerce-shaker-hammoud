import pytest

from models.customer import Customer


@pytest.fixture
def customer():
    return Customer(
        full_name="John Doe", username="johndoe", password="password", age=25
    )


def test_customer_instance(customer):
    assert isinstance(customer, Customer)


def test_customer_attributes(customer):
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
