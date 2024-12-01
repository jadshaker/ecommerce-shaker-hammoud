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
        """
        Initialize a new Product instance.

        Args:
            name (str): The name of the product.
            category (str): The category to which the product belongs.
            price (float): The price of the product.
            description (str, optional): A brief description of the product. Defaults to None.
            stock_count (int, optional): The number of items available in stock. Defaults to 0.
            product_id (int, optional): The unique identifier for the product. Defaults to None.
        """
        self.product_id = product_id
        self.name = name
        self.category = category
        self.price = price
        self.description = description
        self.stock_count = stock_count
