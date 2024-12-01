class Product:
    """
    A class to represent a product in an e-commerce system.

    Attributes:
    product_id : int, optional
        Unique identifier for the product (default is None).
    name : str
        Name of the product.
    category : str
        Category to which the product belongs.
    price : float
        Price of the product.
    description : str, optional
        Description of the product (default is None).
    stock_count : int, optional
        Number of items available in stock (default is 0).

    Methods:
    __init__(self, name, category, price, description=None, stock_count=0, product_id=None):
        Initializes the Product with the given attributes.
    """

    def __init__(
        self, name, category, price, description=None, stock_count=0, product_id=None
    ):
        self.product_id = product_id
        self.name = name
        self.category = category
        self.price = price
        self.description = description
        self.stock_count = stock_count
