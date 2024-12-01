import psycopg2
from supabase import Client, create_client

from config import Config

url: str = Config.SUPABASE.URL
key: str = Config.SUPABASE.KEY
supabase: Client = create_client(url, key)


db_params = {
    "host": "aws-0-us-east-1.pooler.supabase.com",
    "database": "postgres",
    "user": Config.SUPABASE.USER,
    "password": Config.SUPABASE.PASSWORD,
    "port": 6543,
}


def create_tables():
    """
    Creates the necessary tables for the ecommerce database if they do not already exist.

    The following tables are created:
    - Customer: Stores customer information including id, name, username, password, age, address, gender, wallet balance, and creation timestamp.
    - Product: Stores product information including id, name, category, price, description, and stock count.
    - Review: Stores reviews given by customers for products including review id, customer id, product id, rating, comment, review date, and status.
    - Sale: Stores sales transactions including sale id, customer id, product id, sale date, quantity, and total price.

    The function connects to the PostgreSQL database using the provided connection parameters, executes the table creation queries, 
    and handles any exceptions that occur during the process.

    Raises:
        Exception: If there is an error connecting to the database or executing the queries.

    Note:
        The connection parameters should be provided in the `db_params` dictionary.
    """
    queries = [
        """
        CREATE TABLE IF NOT EXISTS Customer (
            customer_id SERIAL PRIMARY KEY,
            full_name VARCHAR(100) NOT NULL,
            username VARCHAR(50) NOT NULL,
            password VARCHAR(255) NOT NULL,  -- Password length can be more than 50 characters to meet validation requirements
            age INT NOT NULL CHECK (age >= 18 AND age <= 120),
            address VARCHAR(200),
            gender VARCHAR(10) CHECK (gender IN ('Male', 'Female', 'Other')),
            wallet_balance DECIMAL(10, 2) DEFAULT 0.00,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS Product (
            product_id SERIAL PRIMARY KEY,
            name VARCHAR(255),
            category VARCHAR(255),
            price DECIMAL(10, 2),
            description TEXT,
            stock_count INT
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS Review (
            review_id SERIAL PRIMARY KEY,
            customer_id INT REFERENCES Customer(customer_id),
            product_id INT REFERENCES Product(product_id),
            rating INT CHECK (rating >= 1 AND rating <= 5),
            comment TEXT,
            review_date DATE,
            status VARCHAR(50)
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS Sale (
            sale_id SERIAL PRIMARY KEY,
            customer_id INT REFERENCES Customer(customer_id),
            product_id INT REFERENCES Product(product_id),
            sale_date DATE,
            quantity INT,
            total_price DECIMAL(10, 2)
        );
        """,
    ]

    try:
        conn = psycopg2.connect(**db_params)
        conn.autocommit = True
        cursor = conn.cursor()
        for query in queries:
            try:
                cursor.execute(query)
            except Exception as table_err:
                print(f"Error creating table: {table_err}")

    except Exception as conn_err:
        print(f"Connection error: {conn_err}")

    finally:
        if conn:
            cursor.close()
            conn.close()


create_tables()
