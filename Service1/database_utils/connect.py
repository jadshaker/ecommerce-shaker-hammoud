from supabase import create_client
from config import Config


class DatabaseConnection:
    """
    A singleton class to manage the database connection using Supabase.

    This class ensures that only one instance of the database connection 
    is created and reused throughout the application.

    :ivar _instance: The single instance of the database connection.
    :type _instance: SupabaseClient
    """

    _instance = None

    @classmethod
    def get_instance(cls):
        """
        Returns the single instance of the database connection.

        If the instance does not exist, it creates one using the Supabase 
        URL and KEY from the configuration.

        :return: The Supabase client instance
        :rtype: SupabaseClient
        :raises ValueError: If Supabase URL or KEY is not found in environment variables
        """
        if cls._instance is None:
            url = Config.SUPABASE.URL
            key = Config.SUPABASE.KEY
            if not url or not key:
                raise ValueError(
                    "Supabase URL or KEY not found in environment variables"
                )
            cls._instance = create_client(url, key)
        return cls._instance


def get_supabase_client():
    """
    Convenience function to get the Supabase client instance.

    :return: The Supabase client instance
    :rtype: SupabaseClient
    """
    return DatabaseConnection.get_instance()
