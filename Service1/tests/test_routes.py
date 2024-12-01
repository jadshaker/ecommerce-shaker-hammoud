from unittest.mock import patch

import pytest
from flask import Flask
from marshmallow import ValidationError
from routes import customer_bp


@pytest.fixture
def client():
    """
    Creates a Flask test client for the application.

    This function sets up a Flask application with the necessary configurations
    for testing purposes. It registers the customer blueprint and enables the
    testing mode. The function yields a test client that can be used to simulate
    requests to the application in a testing environment.

    Yields:
        FlaskClient: A test client for the Flask application.
    """
    app = Flask(__name__)
    app.register_blueprint(customer_bp)
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def test_register_customer(client):
    """
    Test the customer registration endpoint.

    This test mocks the `register_customer` method of the `customer_service` module
    to simulate the registration of a new customer. It sends a POST request to the
    `/register` endpoint with the customer details and asserts that the response
    status code is 201 (Created) and the response JSON contains a success message.

    Args:
        client (FlaskClient): The test client used to make requests to the application.

    Mocks:
        routes.customer_service.register_customer: Mocked to return a predefined
        customer registration response.

    Asserts:
        - The response status code is 201.
        - The response JSON contains a message indicating successful registration.
    """
    with patch("routes.customer_service.register_customer") as mock_register:
        mock_register.return_value = {
            "username": "testuser",
            "full_name": "Test User",
            "age": 25,
            "password": "password",
        }
        response = client.post(
            "/register",
            json={
                "username": "testuser",
                "full_name": "Test User",
                "age": 25,
                "password": "password",
            },
        )
        assert response.status_code == 201
        assert response.json["message"] == "Customer registered successfully"


def test_register_customer_validation_error(client):
    """
    Test case for the /register endpoint to ensure that a validation error is properly handled.

    This test mocks the `customer_schema.load` method to raise a `ValidationError` when invalid data is provided.
    It then sends a POST request to the /register endpoint with invalid data and asserts that the response status code is 400
    and the response JSON contains an "error" key with the value "Validation Error".

    Args:
        client (FlaskClient): The test client used to make requests to the application.

    Assertions:
        - The response status code should be 400.
        - The response JSON should contain an "error" key with the value "Validation Error".
    """
    with patch("routes.customer_schema.load") as mock_load:
        mock_load.side_effect = ValidationError("Invalid data")
        response = client.post("/register", json={"username": "testuser"})
        assert response.status_code == 400
        assert response.json["error"] == "Validation Error"


def test_delete_customer(client):
    """
    Test the delete_customer route.

    This test mocks the customer_service.delete_customer method and sends a DELETE request
    to the /delete/testuser endpoint. It asserts that the response status code is 200 and
    the response JSON contains the message "Customer deleted successfully".

    Args:
        client (FlaskClient): The test client used to make requests to the application.

    Mocks:
        routes.customer_service.delete_customer: Mocked method to simulate customer deletion.
    """
    with patch("routes.customer_service.delete_customer") as mock_delete:
        response = client.delete("/delete/testuser")
        assert response.status_code == 200
        assert response.json["message"] == "Customer deleted successfully"


def test_delete_customer_not_found(client):
    """
    Test case for deleting a customer that does not exist.

    This test simulates the scenario where an attempt is made to delete a customer
    who is not found in the system. It mocks the `delete_customer` method of the 
    `customer_service` to raise a `ValueError` indicating that the customer is not found.
    The test then verifies that the response status code is 404 and the error message
    in the response JSON is "Deletion Error".

    Args:
        client: The test client used to make requests to the application.

    Asserts:
        - The response status code is 404.
        - The response JSON contains an "error" key with the value "Deletion Error".
    """
    with patch("routes.customer_service.delete_customer") as mock_delete:
        mock_delete.side_effect = ValueError("Customer not found")
        response = client.delete("/delete/testuser")
        assert response.status_code == 404
        assert response.json["error"] == "Deletion Error"


def test_update_customer(client):
    """
    Test the update_customer route.

    This test mocks the customer_service.update_customer method to simulate
    updating a customer's information. It sends a PUT request to the 
    /update/testuser endpoint with a JSON payload containing the updated email.
    The test verifies that the response status code is 200 and that the response
    message indicates the customer was updated successfully.

    Args:
        client (FlaskClient): The test client used to make requests to the application.

    Mocks:
        routes.customer_service.update_customer: Mocked to return a predefined 
        response indicating the customer was updated.

    Assertions:
        - The response status code is 200.
        - The response JSON contains a message indicating the customer was updated successfully.
    """
    with patch("routes.customer_service.update_customer") as mock_update:
        mock_update.return_value = {"username": "testuser"}
        response = client.put("/update/testuser", json={"email": "test@example.com"})
        assert response.status_code == 200
        assert response.json["message"] == "Customer updated successfully"


def test_update_customer_validation_error(client):
    """
    Test case for updating a customer with invalid data.

    This test simulates a validation error when attempting to update a customer's information.
    It mocks the `customer_schema.load` method to raise a `ValidationError` and verifies that
    the response status code is 404 and the error message is "Update Error".

    Args:
        client (FlaskClient): The test client used to make requests to the application.

    Mocks:
        routes.customer_schema.load: Mocked to raise a `ValidationError` with the message "Invalid data".

    Asserts:
        - The response status code is 404.
        - The response JSON contains an "error" key with the value "Update Error".
    """
    with patch("routes.customer_schema.load") as mock_load:
        mock_load.side_effect = ValidationError("Invalid data")
        response = client.put("/update/testuser", json={"email": "test@example.com"})
        assert response.status_code == 404
        assert response.json["error"] == "Update Error"


def test_get_all_customers(client):
    """
    Test the endpoint to get all customers.

    This test mocks the `get_all_customers` method from the `customer_service` module
    to return a predefined list of customers. It then sends a GET request to the `/all`
    endpoint and verifies that the response status code is 200 and that the response
    contains the key "customers".

    Args:
        client (FlaskClient): The test client used to make requests to the application.

    Assertions:
        - The response status code should be 200.
        - The response JSON should contain the key "customers".
    """
    with patch("routes.customer_service.get_all_customers") as mock_get_all:
        mock_get_all.return_value = [{"username": "testuser"}]
        response = client.get("/all")
        assert response.status_code == 200
        assert "customers" in response.json


def test_get_customer_by_username(client):
    """
    Test the `get_customer_by_username` route.

    This test mocks the `get_customer_by_username` method from the `customer_service` module
    to return a predefined customer dictionary. It then sends a GET request to the route
    with a test username and asserts that the response status code is 200 and that the 
    response JSON contains the key "customer".

    Args:
        client (FlaskClient): The test client used to make requests to the application.

    Mocks:
        routes.customer_service.get_customer_by_username: Mocked to return a predefined customer dictionary.

    Asserts:
        - The response status code is 200.
        - The response JSON contains the key "customer".
    """
    with patch("routes.customer_service.get_customer_by_username") as mock_get:
        mock_get.return_value = {"username": "testuser"}
        response = client.get("/testuser")
        assert response.status_code == 200
        assert "customer" in response.json


def test_get_customer_by_username_not_found(client):
    """
    Test case for the endpoint that retrieves a customer by username when the customer is not found.

    This test mocks the `get_customer_by_username` method of the `customer_service` to return `None`,
    simulating a scenario where the customer does not exist in the database. It then sends a GET request
    to the endpoint with a test username and asserts that the response status code is 404 (Not Found)
    and the response JSON contains an error message indicating that the customer was not found.

    Args:
        client (FlaskClient): The test client used to make requests to the application.

    Assertions:
        - The response status code should be 404.
        - The response JSON should contain an "error" key with the value "Not Found".
    """
    with patch("routes.customer_service.get_customer_by_username") as mock_get:
        mock_get.return_value = None
        response = client.get("/testuser")
        assert response.status_code == 404
        assert response.json["error"] == "Not Found"


def test_charge_customer_wallet(client):
    """
    Test the charge_customer_wallet route.

    This test mocks the `charge_wallet` method from the `customer_service` module
    to simulate charging a customer's wallet. It verifies that the endpoint
    returns a successful response with the expected status code and message.

    Args:
        client (FlaskClient): The test client used to make requests to the application.

    Asserts:
        - The response status code is 200.
        - The response JSON contains the message "Wallet charged successfully".
    """
    with patch("routes.customer_service.charge_wallet") as mock_charge:
        mock_charge.return_value = 100
        response = client.post("/charge/testuser", json={"amount": 50})
        assert response.status_code == 200
        assert response.json["message"] == "Wallet charged successfully"


def test_charge_customer_wallet_invalid_amount(client):
    """
    Test the /charge/testuser endpoint with an invalid amount.

    This test sends a POST request to the /charge/testuser endpoint with a negative amount
    and verifies that the response status code is 400 and the error message indicates an
    invalid amount.

    Args:
        client: The test client used to make the request.

    Asserts:
        The response status code is 400.
        The response JSON contains an "error" key with the value "Invalid Amount".
    """
    response = client.post("/charge/testuser", json={"amount": -50})
    assert response.status_code == 400
    assert response.json["error"] == "Invalid Amount"


def test_deduct_customer_wallet(client):
    """
    Test the deduct_customer_wallet route.

    This test mocks the `deduct_wallet` method from the `customer_service` module
    to return a fixed value of 50. It then sends a POST request to the `/deduct/testuser`
    endpoint with a JSON payload containing the amount to be deducted. The test
    asserts that the response status code is 200 and that the response JSON contains
    the message "Wallet deducted successfully".

    Args:
        client (FlaskClient): The test client used to make requests to the application.

    Mocks:
        routes.customer_service.deduct_wallet: Mocked to return a fixed value of 50.

    Asserts:
        The response status code is 200.
        The response JSON contains the message "Wallet deducted successfully".
    """
    with patch("routes.customer_service.deduct_wallet") as mock_deduct:
        mock_deduct.return_value = 50
        response = client.post("/deduct/testuser", json={"amount": 50})
        assert response.status_code == 200
        assert response.json["message"] == "Wallet deducted successfully"


def test_deduct_customer_wallet_invalid_amount(client):
    """
    Test the deduction of an invalid amount from a customer's wallet.

    This test sends a POST request to the endpoint "/deduct/testuser" with a negative amount in the JSON payload.
    It asserts that the response status code is 400 (Bad Request) and that the response JSON contains an error message
    indicating an "Invalid Amount".

    Args:
        client: A test client instance for making HTTP requests.

    Asserts:
        The response status code is 400.
        The response JSON contains an "error" key with the value "Invalid Amount".
    """
    response = client.post("/deduct/testuser", json={"amount": -50})
    assert response.status_code == 400
    assert response.json["error"] == "Invalid Amount"
