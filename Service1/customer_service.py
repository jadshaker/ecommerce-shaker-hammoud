from database_utils.connect import get_supabase_client
from models.customer import Customer
from werkzeug.security import generate_password_hash, check_password_hash
from marshmallow import ValidationError

class CustomerService:
    def __init__(self):
        self.supabase = get_supabase_client()
        self.table_name = 'customer'

    def register_customer(self, customer_data):
        """
        Register a new customer
        """
        # Check if username already exists
        existing_user = self.get_customer_by_username(customer_data['username'])
        if existing_user:
            raise ValueError("Username already exists")

        # Hash the password
        customer_data['password'] = generate_password_hash(customer_data['password'])

        # Insert customer
        try:
            response = self.supabase.table(self.table_name).insert(customer_data).execute()
            return response.data[0] if response.data else None
        except Exception as e:
            raise ValueError(f"Error registering customer: {str(e)}")

    def get_customer_by_username(self, username):
        """
        Retrieve a customer by username
        """
        response = self.supabase.table(self.table_name).select('*').eq('username', username).execute()
        return response.data[0] if response.data else None

    def get_all_customers(self):
        """
        Retrieve all customers
        """
        response = self.supabase.table(self.table_name).select('*').execute()
        return response.data

    def update_customer(self, username, update_data):
        """
        Update customer information
        """
        # Remove password from update if present
        update_data.pop('password', None)
        
        try:
            response = (self.supabase.table(self.table_name)
                        .update(update_data)
                        .eq('username', username)
                        .execute())
            return response.data[0] if response.data else None
        except Exception as e:
            raise ValueError(f"Error updating customer: {str(e)}")

    def delete_customer(self, username):
        """
        Delete a customer
        """
        try:
            response = (self.supabase.table(self.table_name)
                        .delete()
                        .eq('username', username)
                        .execute())
            return True
        except Exception as e:
            raise ValueError(f"Error deleting customer: {str(e)}")

    def charge_wallet(self, username, amount):
        """
        Add money to customer's wallet
        """
        try:
            # First, get current balance
            current_customer = self.get_customer_by_username(username)
            if not current_customer:
                raise ValueError("Customer not found")

            new_balance = current_customer['wallet_balance'] + amount

            # Update wallet balance
            response = (self.supabase.table(self.table_name)
                        .update({'wallet_balance': new_balance})
                        .eq('username', username)
                        .execute())
            
            return new_balance
        except Exception as e:
            raise ValueError(f"Error charging wallet: {str(e)}")

    def deduct_wallet(self, username, amount):
        """
        Deduct money from customer's wallet
        """
        try:
            # First, get current balance
            current_customer = self.get_customer_by_username(username)
            if not current_customer:
                raise ValueError("Customer not found")

            current_balance = current_customer['wallet_balance']
            
            # Check if sufficient funds
            if current_balance < amount:
                raise ValueError("Insufficient funds")

            new_balance = current_balance - amount

            # Update wallet balance
            response = (self.supabase.table(self.table_name)
                        .update({'wallet_balance': new_balance})
                        .eq('username', username)
                        .execute())
            
            return new_balance
        except Exception as e:
            raise ValueError(f"Error deducting from wallet: {str(e)}")