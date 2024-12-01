from config import Config
from supabase import create_client


class DatabaseConnection:
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
