from unittest.mock import patch

import pytest
from flask import Flask, json

from Service4.routes import reviews_bp


@pytest.fixture
def client():
    app = Flask(__name__)
    app.register_blueprint(reviews_bp)
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


@patch("Service4.routes.review_service.submit_review")
@patch("Service4.routes.review_schema.load")
def test_submit_review(mock_load, mock_submit_review, client):
    mock_load.return_value = {}
    mock_submit_review.return_value = {
        "review_date": "2023-10-01",
        "review": "Great product!",
    }
    response = client.post("/submit", json={"review": "Great product!"})
    assert response.status_code == 201
    data = json.loads(response.data)
    assert data["message"] == "Review submitted successfully"


@patch("Service4.routes.review_service.update_review")
@patch("Service4.routes.review_schema.load")
def test_update_review(mock_load, mock_update_review, client):
    mock_load.return_value = {}
    mock_update_review.return_value = {
        "review_date": "2023-10-01",
        "review": "Updated review!",
    }
    response = client.put("/update/1", json={"review": "Updated review!"})
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data["message"] == "Review updated successfully"


@patch("Service4.routes.review_service.delete_review")
def test_delete_review(mock_delete_review, client):
    mock_delete_review.return_value = True
    response = client.delete("/delete/1")
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data["message"] == "Review deleted successfully"


@patch("Service4.routes.review_service.get_product_reviews")
def test_get_product_reviews(mock_get_product_reviews, client):
    mock_get_product_reviews.return_value = [
        {"review_date": "2023-10-01", "review": "Great product!"}
    ]
    response = client.get("/product/1")
    assert response.status_code == 200
    data = json.loads(response.data)
    assert len(data) == 1


@patch("Service4.routes.review_service.get_customer_reviews")
def test_get_customer_reviews(mock_get_customer_reviews, client):
    mock_get_customer_reviews.return_value = [
        {"review_date": "2023-10-01", "review": "Great product!"}
    ]
    response = client.get("/customer/1")
    assert response.status_code == 200
    data = json.loads(response.data)
    assert len(data) == 1
