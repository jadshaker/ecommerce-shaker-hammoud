import os
from supabase import create_client, Client

# Load environment variables

# Supabase connection
class DatabaseConnection:
    _instance = None
    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            url = "https://vstesuqxigarpzqrxehj.supabase.co"
            key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InZzdGVzdXF4aWdhcnB6cXJ4ZWhqIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MzI4Nzc2MzMsImV4cCI6MjA0ODQ1MzYzM30.Rut863Jmq7nQ4DSbI25PHiWmAWAq3NIIo5T32vRtTb4"

            if not url or not key:
                raise ValueError("Supabase URL or KEY not found in environment variables")
            
            cls._instance = create_client(url, key)
        
        return cls._instance

def get_supabase_client():
    return DatabaseConnection.get_instance()