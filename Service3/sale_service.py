from database_utils.connect import get_supabase_client


class SaleService:
    """
    SaleService class provides methods to interact with the sales table in the Supabase database.
    Methods:
        __init__():
            Initializes the SaleService instance, setting up the connection to the Supabase client and specifying the sales table name.
        submit_sale(sale_data):
            Submits a new sale to the sales table.
            Args:
                sale_data (dict): The data of the sale to be submitted.
            Returns:
                dict: The submitted sale data if successful, None otherwise.
            Raises:
                ValueError: If there is an error submitting the sale.
        update_sale(sale_id, update_data):
            Updates an existing sale in the sales table.
            Args:
                sale_id (int): The ID of the sale to be updated.
                update_data (dict): The data to update the sale with.
            Returns:
                dict: The updated sale data if successful, None otherwise.
            Raises:
                ValueError: If there is an error updating the sale.
        delete_sale(sale_id):
            Deletes a sale from the sales table by its ID.
            Args:
                sale_id (int): The ID of the sale to be deleted.
            Returns:
                list: The data of the deleted sale if successful, None otherwise.
            Raises:
                ValueError: If there is an error deleting the sale.
        get_customer_sales(customer_id):
            Retrieves all sales for a specific customer from the sales table.
            Args:
                customer_id (int): The ID of the customer whose sales are to be retrieved.
            Returns:
                list: A list of sales data for the specified customer.
            Raises:
                ValueError: If there is an error retrieving the sales.
        get_available_goods():
            Retrieves all available goods from the sales table.
            Returns:
                list: A list of all available goods data.
            Raises:
                ValueError: If there is an error retrieving the available goods.
    """

    def __init__(self):
        """
        Initializes the SaleService instance.

        This constructor sets up the connection to the Supabase client and specifies
        the sales table name.

        Attributes:
            supabase: The Supabase client instance.
            sales_table (str): The name of the sales table in the database.
        """
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
