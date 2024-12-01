from app import create_app


def test_create_app():
    """
    Test the creation of the app instance.

    This test ensures that the `create_app` function successfully creates an app instance.
    It verifies that the created app is not None and that the app's name is correctly set to "app".
    """
    app = create_app()
    assert app is not None
    assert app.name == "app"
