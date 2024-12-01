from datetime import date

from models.sale import Sale


def test_sale_initialization():
    sale = Sale(customer_id=1, product_id=2, quantity=3, total_price=100.0)
    assert sale.customer_id == 1
    assert sale.product_id == 2
    assert sale.quantity == 3
    assert sale.total_price == 100.0
    assert sale.sale_date == date.today()
    assert sale.sale_id is None


def test_sale_initialization_with_date():
    sale_date = date(2023, 1, 1)
    sale = Sale(
        customer_id=1, product_id=2, quantity=3, total_price=100.0, sale_date=sale_date
    )
    assert sale.sale_date == sale_date


def test_sale_initialization_with_sale_id():
    sale = Sale(customer_id=1, product_id=2, quantity=3, total_price=100.0, sale_id=10)
    assert sale.sale_id == 10
