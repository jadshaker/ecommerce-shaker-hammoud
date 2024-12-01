import os

from dotenv import load_dotenv

load_dotenv()


class Config:
    class APP:
        TITLE = "E-Commerce API"
        DESCRIPTION = "An API for an e-commerce application"
        VERSION = "0.1.0"

    class SUPABASE:
        KEY = os.getenv("SUPABASE_KEY")
        URL = os.getenv("SUPABASE_URL")
        USER = os.getenv("SUPABASE_USER")
        PASSWORD = os.getenv("SUPABASE_PASSWORD")
