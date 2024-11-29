from supabase import create_client, Client
import psycopg2

url: str = "https://vstesuqxigarpzqrxehj.supabase.co"
key: str = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InZzdGVzdXF4aWdhcnB6cXJ4ZWhqIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MzI4Nzc2MzMsImV4cCI6MjA0ODQ1MzYzM30.Rut863Jmq7nQ4DSbI25PHiWmAWAq3NIIo5T32vRtTb4"
supabase: Client = create_client(url, key)


db_params = {
    'host': 'aws-0-us-east-1.pooler.supabase.com',
    'database': 'postgres',
    'user': 'postgres.vstesuqxigarpzqrxehj', 
    'password': 'shakerhamoud',  
    'port': 6543
}

def create_tables():
    queries = [
        """
        CREATE TABLE IF NOT EXISTS Customer (
            customer_id SERIAL PRIMARY KEY,
            full_name VARCHAR(255),
            username VARCHAR(255),
            age INT,
            address TEXT,
            gender VARCHAR(10),
            wallet_balance DECIMAL(10, 2)
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
        """
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