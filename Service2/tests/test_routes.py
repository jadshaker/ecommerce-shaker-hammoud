from unittest.mock import patch

import pytest
from flask import Flask
from marshmallow import ValidationError

from Service2.routes import inventory_bp


@pytest.fixture
def client():
    app = Flask(__name__)
    app.register_blueprint(inventory_bp)
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


@patch("Service2.routes.inventory_service.add_goods")
@patch("Service2.routes.product_schema.load")
@patch("Service2.routes.product_schema.dump")
def test_add_goods(mock_dump, mock_load, mock_add_goods, client):
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
    mock_load.side_effect = ValidationError("Invalid data")

    response = client.post("/add", json={"name": "Invalid Product"})
    assert response.status_code == 400
    assert "Validation Error" in response.json["error"]


@patch("Service2.routes.inventory_service.add_goods")
@patch("Service2.routes.product_schema.load")
def test_add_goods_value_error(mock_load, mock_add_goods, client):
    mock_load.return_value = None
    mock_add_goods.side_effect = ValueError("Addition failed")

    response = client.post("/add", json={"name": "Test Product"})
    assert response.status_code == 400
    assert "Addition Error" in response.json["error"]


@patch("Service2.routes.inventory_service.deduct_goods")
def test_deduct_goods_value_error(mock_deduct_goods, client):
    mock_deduct_goods.side_effect = ValueError("Deduction failed")

    response = client.post("/deduct/1")
    assert response.status_code == 400
    assert "Deduction Error" in response.json["error"]


@patch("Service2.routes.inventory_service.update_goods")
def test_update_goods_validation_error(mock_update_goods, client):
    mock_update_goods.side_effect = ValidationError("Invalid data")

    response = client.put("/update/1", json={"name": "Invalid Product"})
    assert response.status_code == 400
    assert "Validation Error" in response.json["error"]


@patch("Service2.routes.inventory_service.update_goods")
def test_update_goods_value_error(mock_update_goods, client):
    mock_update_goods.side_effect = ValueError("Update failed")

    response = client.put("/update/1", json={"name": "Test Product"})
    assert response.status_code == 400
    assert "Update Error" in response.json["error"]
