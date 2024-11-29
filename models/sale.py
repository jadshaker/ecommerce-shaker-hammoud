# models/sale.py
from datetime import date
class Sale:
    def __init__(self, customer_id, product_id, quantity, total_price, 
                 sale_date=None, sale_id=None):
        self.sale_id = sale_id
        self.customer_id = customer_id
        self.product_id = product_id
        self.sale_date = sale_date or date.today()
        self.quantity = quantity
        self.total_price = total_price