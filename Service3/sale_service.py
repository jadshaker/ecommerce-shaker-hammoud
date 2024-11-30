from database_utils.connect import get_supabase_client


class SaleService:
    def __init__(self):
        self.supabase = get_supabase_client()
        self.sales_table = "sale"

    def submit_sale(self, sale_data):
        """
        Submit a new sale
        """
        try:
            response = self.supabase.table(self.sales_table).insert(sale_data).execute()
            return response.data[0] if response.data else None
        except Exception as e:
            raise ValueError(f"Error submitting sale: {str(e)}")

    def update_sale(self, sale_id, update_data):
        """
        Update an existing sale
        """
        try:
            response = (
                self.supabase.table(self.sales_table)
                .update(update_data)
                .eq("sale_id", sale_id)
                .execute()
            )
            return response.data[0] if response.data else None
        except Exception as e:
            raise ValueError(f"Error updating sale: {str(e)}")

    def delete_sale(self, sale_id):
        """
        Delete a sale by its ID
        """
        try:
            response = (
                self.supabase.table(self.sales_table)
                .delete()
                .eq("sale_id", sale_id)
                .execute()
            )
            return response.data if response.data else None
        except Exception as e:
            raise ValueError(f"Error deleting sale: {str(e)}")

    def get_customer_sales(self, customer_id):
        """
        Retrieve all sales for a specific customer
        """
        try:
            response = (
                self.supabase.table(self.sales_table)
                .select("*")
                .eq("customer_id", customer_id)
                .execute()
            )
            return response.data
        except Exception as e:
            raise ValueError(f"Error retrieving sales: {str(e)}")

    def get_available_goods(self):
        """
        Retrieve all available goods
        """
        try:
            response = self.supabase.table(self.sales_table).select("*").execute()
            return response.data
        except Exception as e:
            raise ValueError(f"Error retrieving available goods: {str(e)}")
