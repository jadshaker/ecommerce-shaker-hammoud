from app import create_app


def test_create_app():
    """
    Test the creation of the app instance.

    This test ensures that the `create_app` function successfully creates an app instance
    and verifies that the app instance is not None and has the expected name "app".
    """
    app = create_app()
    assert app is not None
    assert app.name == "app"
