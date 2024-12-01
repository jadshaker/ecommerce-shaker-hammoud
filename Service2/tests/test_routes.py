from unittest.mock import patch

import pytest
from flask import Flask
from marshmallow import ValidationError

from Service2.routes import inventory_bp


@pytest.fixture
def client():
    """
    Creates a Flask test client for the application.

    This function sets up a Flask application with the inventory blueprint
    registered and the testing configuration enabled. It yields a test client
    that can be used to simulate requests to the application in a testing context.

    Yields:
        FlaskClient: A test client for the Flask application.
    """
    app = Flask(__name__)
    app.register_blueprint(inventory_bp)
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


@patch("Service2.routes.inventory_service.add_goods")
@patch("Service2.routes.product_schema.load")
@patch("Service2.routes.product_schema.dump")
def test_add_goods(mock_dump, mock_load, mock_add_goods, client):
    """
    Test the add_goods route.
    This test verifies that the add_goods endpoint correctly adds a new product
    and returns the expected response.
    Args:
        mock_dump (Mock): Mock object for the dump function.
        mock_load (Mock): Mock object for the load function.
        mock_add_goods (Mock): Mock object for the add_goods function.
        client (FlaskClient): Test client for making requests to the application.
    Setup:
        - mock_load is set to return None.
        - mock_add_goods is set to return a dictionary representing the added product.
        - mock_dump is set to return the same dictionary.
    Test:
        - Sends a POST request to the /add endpoint with a JSON payload containing the product name.
        - Asserts that the response status code is 201 (Created).
        - Asserts that the response JSON contains a success message and the added product details.
    """
    mock_load.return_value = None
    mock_add_goods.return_value = {"id": 1, "name": "Test Product"}
    mock_dump.return_value = {"id": 1, "name": "Test Product"}

    response = client.post("/add", json={"name": "Test Product"})
    assert response.status_code == 201
    assert response.json == {
        "message": "Product added successfully",
        "product": {"id": 1, "name": "Test Product"},
    }


@patch("Service2.routes.inventory_service.deduct_goods")
@patch("Service2.routes.product_schema.dump")
def test_deduct_goods(mock_dump, mock_deduct_goods, client):
    """
    Test the deduct_goods endpoint.
    This test verifies that the deduct_goods endpoint correctly deducts a product
    and returns the expected response.
    Args:
        mock_dump (Mock): Mock object for the dump function.
        mock_deduct_goods (Mock): Mock object for the deduct_goods function.
        client (FlaskClient): Test client for making requests to the application.
    Setup:
        - Mocks the deduct_goods function to return a predefined product.
        - Mocks the dump function to return a predefined product.
    Test:
        - Sends a POST request to the /deduct/1 endpoint.
        - Asserts that the response status code is 200.
        - Asserts that the response JSON matches the expected output.
    Expected Output:
        {
            "product": {"id": 1, "name": "Test Product"}
    """
    mock_deduct_goods.return_value = {"id": 1, "name": "Test Product"}
    mock_dump.return_value = {"id": 1, "name": "Test Product"}

    response = client.post("/deduct/1")
    assert response.status_code == 200
    assert response.json == {
        "message": "Product deducted successfully",
        "product": {"id": 1, "name": "Test Product"},
    }


@patch("Service2.routes.inventory_service.update_goods")
@patch("Service2.routes.product_schema.dump")
def test_update_goods(mock_dump, mock_update_goods, client):
    """
    Test the update_goods endpoint.
    This test verifies that the update_goods endpoint correctly updates a product
    and returns the expected response.
    Args:
        mock_dump (Mock): Mock object for the dump function.
        mock_update_goods (Mock): Mock object for the update_goods function.
        client (FlaskClient): Test client for making requests to the application.
    Setup:
        - Mocks the update_goods function to return a predefined product.
        - Mocks the dump function to return the same predefined product.
    Test:
        - Sends a PUT request to the /update/1 endpoint with the updated product data.
        - Asserts that the response status code is 200.
        - Asserts that the response JSON contains the expected success message and updated product data.
    """
    mock_update_goods.return_value = {"id": 1, "name": "Updated Product"}
    mock_dump.return_value = {"id": 1, "name": "Updated Product"}

    response = client.put("/update/1", json={"name": "Updated Product"})
    assert response.status_code == 200
    assert response.json == {
        "message": "Product updated successfully",
        "product": {"id": 1, "name": "Updated Product"},
    }


@patch("Service2.routes.product_schema.load")
def test_add_goods_validation_error(mock_load, client):
    """
    Test case for adding goods with validation error.
    This test simulates a scenario where the input data for adding goods is invalid,
    and a `ValidationError` is raised. It verifies that the API responds with a 
    400 status code and includes an appropriate error message in the response.
    Args:
        mock_load (Mock): A mock object for the load function, which raises a 
                          `ValidationError` when called.
        client (FlaskClient): A test client for making requests to the application.
    Assertions:
        - The response status code should be 400.
        - The error message in the response should contain "Validation Error".
    """
    mock_load.side_effect = ValidationError("Invalid data")

    response = client.post("/add", json={"name": "Invalid Product"})
    assert response.status_code == 400
    assert "Validation Error" in response.json["error"]


@patch("Service2.routes.inventory_service.add_goods")
@patch("Service2.routes.product_schema.load")
def test_add_goods_value_error(mock_load, mock_add_goods, client):
    """
    Test case for adding goods with a ValueError.
    This test simulates a scenario where adding goods fails due to a ValueError.
    It mocks the `load` and `add_goods` functions to control their behavior during the test.
    Args:
        mock_load (Mock): Mock object for the `load` function.
        mock_add_goods (Mock): Mock object for the `add_goods` function.
        client (FlaskClient): Test client for making HTTP requests.
    Test Steps:
    1. Set `mock_load` to return None.
    2. Set `mock_add_goods` to raise a ValueError with the message "Addition failed".
    3. Send a POST request to the "/add" endpoint with a JSON payload containing the product name.
    4. Assert that the response status code is 400 (Bad Request).
    5. Assert that the response JSON contains an error message with "Addition Error".
    """
    mock_load.return_value = None
    mock_add_goods.side_effect = ValueError("Addition failed")

    response = client.post("/add", json={"name": "Test Product"})
    assert response.status_code == 400
    assert "Addition Error" in response.json["error"]


@patch("Service2.routes.inventory_service.deduct_goods")
def test_deduct_goods_value_error(mock_deduct_goods, client):
    """
    Test case for the /deduct/<id> endpoint when a ValueError is raised.
    This test simulates a scenario where the deduction of goods fails due to a ValueError.
    It verifies that the API responds with a 400 status code and an appropriate error message.
    Args:
        mock_deduct_goods (Mock): A mock object for the deduct_goods function.
        client (FlaskClient): A test client for making HTTP requests to the Flask application.
    Assertions:
        - The response status code should be 400.
        - The response JSON should contain an "error" key with the message "Deduction Error".
    """
    mock_deduct_goods.side_effect = ValueError("Deduction failed")

    response = client.post("/deduct/1")
    assert response.status_code == 400
    assert "Deduction Error" in response.json["error"]


@patch("Service2.routes.inventory_service.update_goods")
def test_update_goods_validation_error(mock_update_goods, client):
    """
    Test case for updating goods with invalid data.
    This test simulates a validation error when attempting to update goods.
    It mocks the `update_goods` function to raise a `ValidationError` and
    verifies that the API responds with a 400 status code and an appropriate
    error message.
    Args:
        mock_update_goods (Mock): Mock object for the `update_goods` function.
        client (FlaskClient): Test client for making HTTP requests.
    Assertions:
        - The response status code should be 400.
        - The response JSON should contain an error message indicating a validation error.
    """
    mock_update_goods.side_effect = ValidationError("Invalid data")

    response = client.put("/update/1", json={"name": "Invalid Product"})
    assert response.status_code == 400
    assert "Validation Error" in response.json["error"]


@patch("Service2.routes.inventory_service.update_goods")
def test_update_goods_value_error(mock_update_goods, client):
    """
    Test case for updating goods with a ValueError.
    This test simulates a scenario where the `update_goods` function raises a 
    ValueError, and verifies that the API responds with a 400 status code and 
    an appropriate error message.
    Args:
        mock_update_goods (Mock): A mock object for the `update_goods` function.
        client (FlaskClient): A test client for making HTTP requests to the API.
    Assertions:
        - The response status code should be 400.
        - The response JSON should contain an error message with "Update Error".
    """
    mock_update_goods.side_effect = ValueError("Update failed")

    response = client.put("/update/1", json={"name": "Test Product"})
    assert response.status_code == 400
    assert "Update Error" in response.json["error"]
