# models/product.py
class Product:
    def __init__(self, name, category, price, 
                 description=None, stock_count=0, product_id=None):
        self.product_id = product_id
        self.name = name
        self.category = category
        self.price = price
        self.description = description
        self.stock_count = stock_count