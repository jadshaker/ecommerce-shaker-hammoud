import pytest

from models.product import Product


@pytest.fixture
def sample_product():
    """
    Creates a sample Product instance with predefined attributes.

    Returns:
        Product: A Product instance with the following attributes:
            - name: "Sample Product"
            - category: "Sample Category"
            - price: 19.99
            - description: "This is a sample product"
            - stock_count: 10
            - product_id: 1
    """
    return Product(
        name="Sample Product",
        category="Sample Category",
        price=19.99,
        description="This is a sample product",
        stock_count=10,
        product_id=1,
    )


def test_product_creation(sample_product):
    """
    Test the creation of a product instance.

    This test verifies that a sample product is created with the expected attributes.

    Args:
        sample_product (Product): A fixture that provides a sample product instance.

    Assertions:
        - The product's name should be "Sample Product".
        - The product's category should be "Sample Category".
        - The product's price should be 19.99.
        - The product's description should be "This is a sample product".
        - The product's stock count should be 10.
        - The product's product_id should be 1.
    """
    assert sample_product.name == "Sample Product"
    assert sample_product.category == "Sample Category"
    assert sample_product.price == 19.99
    assert sample_product.description == "This is a sample product"
    assert sample_product.stock_count == 10
    assert sample_product.product_id == 1


def test_product_default_values():
    """
    Test the default values of the Product model.

    This test ensures that when a Product instance is created with only the 
    required parameters (name, category, and price), the optional parameters 
    (description, stock_count, and product_id) are set to their expected default values.

    Assertions:
        - The description should be None.
        - The stock_count should be 0.
        - The product_id should be None.
    """
    product = Product(name="Default Product", category="Default Category", price=9.99)
    assert product.description is None
    assert product.stock_count == 0
    assert product.product_id is None


def test_product_update_stock(sample_product):
    """
    Test the update of the stock count for a product.

    This test ensures that the stock count of a sample product can be updated
    correctly. It sets the stock count to 20 and asserts that the stock count
    is updated to the expected value.

    Args:
        sample_product (Product): A fixture that provides a sample product instance.

    Asserts:
        The stock count of the sample product is updated to 20.
    """
    sample_product.stock_count = 20
    assert sample_product.stock_count == 20


def test_product_update_price(sample_product):
    """
    Test the update of the product price.

    This test function updates the price of a sample product to 29.99 and asserts
    that the price has been updated correctly.

    Args:
        sample_product (Product): A fixture that provides a sample product instance.

    Asserts:
        The price of the sample product is updated to 29.99.
    """
    sample_product.price = 29.99
    assert sample_product.price == 29.99
