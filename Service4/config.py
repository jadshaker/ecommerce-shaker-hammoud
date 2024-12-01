import os

from dotenv import load_dotenv

load_dotenv()


class Config:
    """
    Configuration settings for the E-Commerce API application.

    Classes:
        APP: Contains application-specific settings.
            - TITLE (str): The title of the application.
            - DESCRIPTION (str): A brief description of the application.
            - VERSION (str): The current version of the application.

        SUPABASE: Contains Supabase-specific settings.
            - KEY (str): The API key for accessing Supabase, retrieved from environment variables.
            - URL (str): The URL for the Supabase instance, retrieved from environment variables.
            - USER (str): The username for Supabase authentication, retrieved from environment variables.
            - PASSWORD (str): The password for Supabase authentication, retrieved from environment variables.
    """
    class APP:
        """
        APP configuration class for the E-Commerce API.

        Attributes:
            TITLE (str): The title of the API.
            DESCRIPTION (str): A brief description of the API.
            VERSION (str): The current version of the API.
        """
        TITLE = "E-Commerce API"
        DESCRIPTION = "An API for an e-commerce application"
        VERSION = "0.1.0"

    class SUPABASE:
        """
        A configuration class for Supabase credentials.

        Attributes:
            KEY (str): The API key for Supabase, retrieved from environment variables.
            URL (str): The URL for the Supabase instance, retrieved from environment variables.
            USER (str): The username for Supabase, retrieved from environment variables.
            PASSWORD (str): The password for Supabase, retrieved from environment variables.
        """
        KEY = os.getenv("SUPABASE_KEY")
        URL = os.getenv("SUPABASE_URL")
        USER = os.getenv("SUPABASE_USER")
        PASSWORD = os.getenv("SUPABASE_PASSWORD")
