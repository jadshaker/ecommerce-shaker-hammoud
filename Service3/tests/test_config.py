from config import Config


def test_app_config():
    """
    Test the application configuration settings.

    This test verifies that the application configuration settings for the title,
    description, and version are correctly set.

    Assertions:
        - Config.APP.TITLE is "E-Commerce API"
        - Config.APP.DESCRIPTION is "An API for an e-commerce application"
        - Config.APP.VERSION is "0.1.0"
    """
    assert Config.APP.TITLE == "E-Commerce API"
    assert Config.APP.DESCRIPTION == "An API for an e-commerce application"
    assert Config.APP.VERSION == "0.1.0"


def test_supabase_config(monkeypatch):
    """
    Test the Supabase configuration settings.

    This test ensures that the Supabase configuration settings are not None.
    It checks the following attributes of the Config.SUPABASE class:
    - KEY: The Supabase API key.
    - URL: The Supabase URL.
    - USER: The Supabase user.
    - PASSWORD: The Supabase password.

    Args:
        monkeypatch: A pytest fixture used to modify or set environment variables or attributes.
    """
    assert Config.SUPABASE.KEY is not None
    assert Config.SUPABASE.URL is not None
    assert Config.SUPABASE.USER is not None
    assert Config.SUPABASE.PASSWORD is not None
