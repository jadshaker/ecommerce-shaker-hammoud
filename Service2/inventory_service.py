from database_utils.connect import get_supabase_client
from models.product import Product

class InventoryService:
    def __init__(self):
        self.supabase = get_supabase_client()
        self.table_name = 'product'

    def add_goods(self, product_data):
        """
        Add a new product to the inventory
        """
        try:
            # Insert product
            response = self.supabase.table(self.table_name).insert(product_data).execute()
            return response.data[0] if response.data else None
        except Exception as e:
            raise ValueError(f"Error adding product: {str(e)}")

    def deduct_goods(self, product_id):
        """
        Deduct a product from inventory (decrease stock count)
        """
        try:
            # Get the current product
            product = self.get_product_by_id(product_id)
            if not product:
                raise ValueError("Product not found")
            
            if product['stock_count'] <= 0:
                raise ValueError("Stock count is already zero")
            
            updated_stock = product['stock_count'] - 1

            # Update stock count
            response = (self.supabase.table(self.table_name)
                        .update({'stock_count': updated_stock})
                        .eq('product_id', product_id)
                        .execute())
            
            return response.data[0] if response.data else None
        except Exception as e:
            raise ValueError(f"Error deducting product: {str(e)}")

    def update_goods(self, product_id, update_data):
        """
        Update fields related to a specific product
        """
        try:
            response = (self.supabase.table(self.table_name)
                        .update(update_data)
                        .eq('product_id', product_id)
                        .execute())
            return response.data[0] if response.data else None
        except Exception as e:
            raise ValueError(f"Error updating product: {str(e)}")

    def get_product_by_id(self, product_id):
        """
        Retrieve a product by its ID
        """
        response = self.supabase.table(self.table_name).select('*').eq('product_id', product_id).execute()
        return response.data[0] if response.data else None
