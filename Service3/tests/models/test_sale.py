from datetime import date

from models.sale import Sale


def test_sale_initialization():
    """
    Test the initialization of the Sale model.

    This test verifies that a Sale object is correctly initialized with the given
    customer_id, product_id, quantity, and total_price. It also checks that the
    sale_date is set to the current date and that the sale_id is initially None.

    Assertions:
        - sale.customer_id is set to 1
        - sale.product_id is set to 2
        - sale.quantity is set to 3
        - sale.total_price is set to 100.0
        - sale.sale_date is set to today's date
        - sale.sale_id is None
    """
    sale = Sale(customer_id=1, product_id=2, quantity=3, total_price=100.0)
    assert sale.customer_id == 1
    assert sale.product_id == 2
    assert sale.quantity == 3
    assert sale.total_price == 100.0
    assert sale.sale_date == date.today()
    assert sale.sale_id is None


def test_sale_initialization_with_date():
    """
    Test the initialization of a Sale object with a specific sale date.

    This test ensures that a Sale object is correctly initialized with the provided
    sale date and that the sale_date attribute of the Sale object matches the expected
    date.

    Steps:
    1. Create a sale_date with the value January 1, 2023.
    2. Initialize a Sale object with the given customer_id, product_id, quantity,
        total_price, and sale_date.
    3. Assert that the sale_date attribute of the Sale object is equal to the
        expected sale_date.

    Expected Result:
    The sale_date attribute of the Sale object should match the provided sale_date.
    """
    sale_date = date(2023, 1, 1)
    sale = Sale(
        customer_id=1, product_id=2, quantity=3, total_price=100.0, sale_date=sale_date
    )
    assert sale.sale_date == sale_date


def test_sale_initialization_with_sale_id():
    """
    Test the initialization of a Sale object with a specified sale_id.

    This test ensures that when a Sale object is initialized with a sale_id,
    the sale_id attribute is correctly set to the provided value.

    Assertions:
        - The sale_id attribute of the Sale object should be equal to the provided sale_id (10).
    """
    sale = Sale(customer_id=1, product_id=2, quantity=3, total_price=100.0, sale_id=10)
    assert sale.sale_id == 10
