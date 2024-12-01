from unittest.mock import patch

import pytest
from flask import Flask
from marshmallow import ValidationError
from routes import customer_bp


@pytest.fixture
def client():
    app = Flask(__name__)
    app.register_blueprint(customer_bp)
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def test_register_customer(client):
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
    with patch("routes.customer_schema.load") as mock_load:
        mock_load.side_effect = ValidationError("Invalid data")
        response = client.post("/register", json={"username": "testuser"})
        assert response.status_code == 400
        assert response.json["error"] == "Validation Error"


def test_delete_customer(client):
    with patch("routes.customer_service.delete_customer") as mock_delete:
        response = client.delete("/delete/testuser")
        assert response.status_code == 200
        assert response.json["message"] == "Customer deleted successfully"


def test_delete_customer_not_found(client):
    with patch("routes.customer_service.delete_customer") as mock_delete:
        mock_delete.side_effect = ValueError("Customer not found")
        response = client.delete("/delete/testuser")
        assert response.status_code == 404
        assert response.json["error"] == "Deletion Error"


def test_update_customer(client):
    with patch("routes.customer_service.update_customer") as mock_update:
        mock_update.return_value = {"username": "testuser"}
        response = client.put("/update/testuser", json={"email": "test@example.com"})
        assert response.status_code == 200
        assert response.json["message"] == "Customer updated successfully"


def test_update_customer_validation_error(client):
    with patch("routes.customer_schema.load") as mock_load:
        mock_load.side_effect = ValidationError("Invalid data")
        response = client.put("/update/testuser", json={"email": "test@example.com"})
        assert response.status_code == 404
        assert response.json["error"] == "Update Error"


def test_get_all_customers(client):
    with patch("routes.customer_service.get_all_customers") as mock_get_all:
        mock_get_all.return_value = [{"username": "testuser"}]
        response = client.get("/all")
        assert response.status_code == 200
        assert "customers" in response.json


def test_get_customer_by_username(client):
    with patch("routes.customer_service.get_customer_by_username") as mock_get:
        mock_get.return_value = {"username": "testuser"}
        response = client.get("/testuser")
        assert response.status_code == 200
        assert "customer" in response.json


def test_get_customer_by_username_not_found(client):
    with patch("routes.customer_service.get_customer_by_username") as mock_get:
        mock_get.return_value = None
        response = client.get("/testuser")
        assert response.status_code == 404
        assert response.json["error"] == "Not Found"


def test_charge_customer_wallet(client):
    with patch("routes.customer_service.charge_wallet") as mock_charge:
        mock_charge.return_value = 100
        response = client.post("/charge/testuser", json={"amount": 50})
        assert response.status_code == 200
        assert response.json["message"] == "Wallet charged successfully"


def test_charge_customer_wallet_invalid_amount(client):
    response = client.post("/charge/testuser", json={"amount": -50})
    assert response.status_code == 400
    assert response.json["error"] == "Invalid Amount"


def test_deduct_customer_wallet(client):
    with patch("routes.customer_service.deduct_wallet") as mock_deduct:
        mock_deduct.return_value = 50
        response = client.post("/deduct/testuser", json={"amount": 50})
        assert response.status_code == 200
        assert response.json["message"] == "Wallet deducted successfully"


def test_deduct_customer_wallet_invalid_amount(client):
    response = client.post("/deduct/testuser", json={"amount": -50})
    assert response.status_code == 400
    assert response.json["error"] == "Invalid Amount"
