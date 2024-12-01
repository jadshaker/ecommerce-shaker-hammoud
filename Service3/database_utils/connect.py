from supabase import create_client

from config import Config


class DatabaseConnection:
    """
    A singleton class to manage the database connection using Supabase.

    This class ensures that only one instance of the database connection is created
    and reused throughout the application.

    Attributes:
        _instance (SupabaseClient): The single instance of the database connection.

    Methods:
        get_instance():
            Returns the single instance of the database connection. If the instance
            does not exist, it creates one using the Supabase URL and KEY from the
            configuration.
    """
    _instance = None

    @classmethod
    def get_instance(cls):
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
    return DatabaseConnection.get_instance()
