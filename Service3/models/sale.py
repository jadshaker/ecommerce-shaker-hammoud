from datetime import date


class Sale:
    """
    A class to represent a sale transaction.

    Attributes:
    -----------
    sale_id : int, optional
        Unique identifier for the sale (default is None).
    customer_id : int
        Unique identifier for the customer.
    product_id : int
        Unique identifier for the product.
    sale_date : date, optional
        The date of the sale (default is today's date).
    quantity : int
        The quantity of the product sold.
    total_price : float
        The total price of the sale.

    Methods:
    --------
    __init__(self, customer_id, product_id, quantity, total_price, sale_date=None, sale_id=None):
        Initializes the Sale object with the provided attributes.
    """

    def __init__(
        self,
        customer_id,
        product_id,
        quantity,
        total_price,
        sale_date=None,
        sale_id=None,
    ):
        self.sale_id = sale_id
        self.customer_id = customer_id
        self.product_id = product_id
        self.sale_date = sale_date or date.today()
        self.quantity = quantity
        self.total_price = total_price
