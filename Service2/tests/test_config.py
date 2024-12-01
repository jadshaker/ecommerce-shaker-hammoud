from config import Config


def test_app_config():
    assert Config.APP.TITLE == "E-Commerce API"
    assert Config.APP.DESCRIPTION == "An API for an e-commerce application"
    assert Config.APP.VERSION == "0.1.0"


def test_supabase_config(monkeypatch):
    assert Config.SUPABASE.KEY is not None
    assert Config.SUPABASE.URL is not None
    assert Config.SUPABASE.USER is not None
    assert Config.SUPABASE.PASSWORD is not None
