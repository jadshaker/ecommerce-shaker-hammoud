import pytest

from models.product import Product


@pytest.fixture
def sample_product():
    return Product(
        name="Sample Product",
        category="Sample Category",
        price=19.99,
        description="This is a sample product",
        stock_count=10,
        product_id=1,
    )


def test_product_creation(sample_product):
    assert sample_product.name == "Sample Product"
    assert sample_product.category == "Sample Category"
    assert sample_product.price == 19.99
    assert sample_product.description == "This is a sample product"
    assert sample_product.stock_count == 10
    assert sample_product.product_id == 1


def test_product_default_values():
    product = Product(name="Default Product", category="Default Category", price=9.99)
    assert product.description is None
    assert product.stock_count == 0
    assert product.product_id is None


def test_product_update_stock(sample_product):
    sample_product.stock_count = 20
    assert sample_product.stock_count == 20


def test_product_update_price(sample_product):
    sample_product.price = 29.99
    assert sample_product.price == 29.99
