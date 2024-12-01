from database_utils.connect import get_supabase_client


class InventoryService:
    """
    InventoryService class to manage inventory operations such as adding, deducting, updating, and retrieving products.

    Methods:
        __init__():
            Initializes the InventoryService class with a Supabase client and table name.

        add_goods(product_data):
            Adds a new product to the inventory.
            Args:
                product_data (dict): The data of the product to be added.
            Returns:
                dict: The added product data if successful, None otherwise.
            Raises:
                ValueError: If there is an error adding the product.

        deduct_goods(product_id):
            Deducts a product from the inventory by decreasing its stock count.
            Args:
                product_id (str): The ID of the product to be deducted.
            Returns:
                dict: The updated product data if successful, None otherwise.
            Raises:
                ValueError: If the product is not found, stock count is zero, or there is an error deducting the product.

        update_goods(product_id, update_data):
            Updates fields related to a specific product.
            Args:
                product_id (str): The ID of the product to be updated.
                update_data (dict): The data to update the product with.
            Returns:
                dict: The updated product data if successful, None otherwise.
            Raises:
                ValueError: If there is an error updating the product.

        get_product_by_id(product_id):
            Retrieves a product by its ID.
            Args:
                product_id (str): The ID of the product to be retrieved.
            Returns:
                dict: The product data if found, None otherwise.
    """

    def __init__(self):
        """
        Initializes the InventoryService class.

        Attributes:
            supabase (SupabaseClient): The client used to interact with the Supabase database.
            table_name (str): The name of the table in the database where product information is stored.
        """
        self.supabase = get_supabase_client()
        self.table_name = "product"

    def add_goods(self, product_data):
        """
        Add a new product to the inventory
        """
        try:
            # Insert product
            response = (
                self.supabase.table(self.table_name).insert(product_data).execute()
            )
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

            if product["stock_count"] <= 0:
                raise ValueError("Stock count is already zero")

            updated_stock = product["stock_count"] - 1

            # Update stock count
            response = (
                self.supabase.table(self.table_name)
                .update({"stock_count": updated_stock})
                .eq("product_id", product_id)
                .execute()
            )

            return response.data[0] if response.data else None
        except Exception as e:
            raise ValueError(f"Error deducting product: {str(e)}")

    def update_goods(self, product_id, update_data):
        """
        Update fields related to a specific product
        """
        try:
            response = (
                self.supabase.table(self.table_name)
                .update(update_data)
                .eq("product_id", product_id)
                .execute()
            )
            return response.data[0] if response.data else None
        except Exception as e:
            raise ValueError(f"Error updating product: {str(e)}")

    def get_product_by_id(self, product_id):
        """
        Retrieve a product by its ID
        """
        response = (
            self.supabase.table(self.table_name)
            .select("*")
            .eq("product_id", product_id)
            .execute()
        )
        return response.data[0] if response.data else None
