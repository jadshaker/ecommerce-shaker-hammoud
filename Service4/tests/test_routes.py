from unittest.mock import patch

import pytest
from flask import Flask, json

from Service4.routes import reviews_bp


@pytest.fixture
def client():
    """
    Creates a Flask test client for the application.

    This function sets up a Flask application with the necessary configurations
    for testing, registers the `reviews_bp` blueprint, and yields a test client
    that can be used to simulate requests to the application.

    Yields:
        FlaskClient: A test client for the Flask application.
    """
    app = Flask(__name__)
    app.register_blueprint(reviews_bp)
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


@patch("Service4.routes.review_service.submit_review")
@patch("Service4.routes.review_schema.load")
def test_submit_review(mock_load, mock_submit_review, client):
    """
    Test the review submission endpoint.

    This test verifies that the review submission endpoint works correctly by
    mocking the load and submit review functions and sending a POST request
    to the /submit endpoint.

    Args:
        mock_load (Mock): Mock object for the load function.
        mock_submit_review (Mock): Mock object for the submit review function.
        client (FlaskClient): Test client for sending requests to the application.

    Assertions:
        - The response status code should be 201 (Created).
        - The response data should contain a message indicating successful review submission.
    """
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
    """
    Test the update review functionality.

    This test mocks the loading and updating of a review and verifies that the
    update review endpoint works as expected.

    Args:
        mock_load (Mock): Mock object for loading the review.
        mock_update_review (Mock): Mock object for updating the review.
        client (FlaskClient): Test client for making requests to the application.

    Test Steps:
    1. Mock the `load` method to return an empty dictionary.
    2. Mock the `update_review` method to return a dictionary with the updated review details.
    3. Send a PUT request to the `/update/1` endpoint with the updated review data.
    4. Assert that the response status code is 200.
    5. Parse the response data and assert that the message indicates a successful update.
    """
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
    """
    Test the delete review endpoint.

    This test mocks the delete review function and verifies that the endpoint
    returns a successful response when a review is deleted.

    Args:
        mock_delete_review (Mock): Mock object for the delete review function.
        client (FlaskClient): Test client for making requests to the application.

    Asserts:
        The response status code is 200.
        The response data contains a message indicating successful deletion.
    """
    mock_delete_review.return_value = True
    response = client.delete("/delete/1")
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data["message"] == "Review deleted successfully"


@patch("Service4.routes.review_service.get_product_reviews")
def test_get_product_reviews(mock_get_product_reviews, client):
    """
    Test the endpoint for retrieving product reviews.

    This test mocks the `get_product_reviews` function to return a predefined list of reviews.
    It then sends a GET request to the `/product/1` endpoint and verifies the response.

    Args:
        mock_get_product_reviews (Mock): Mock object for the `get_product_reviews` function.
        client (FlaskClient): Test client for sending requests to the application.

    Assertions:
        - The response status code should be 200.
        - The length of the returned data should be 1.
    """
    mock_get_product_reviews.return_value = [
        {"review_date": "2023-10-01", "review": "Great product!"}
    ]
    response = client.get("/product/1")
    assert response.status_code == 200
    data = json.loads(response.data)
    assert len(data) == 1


@patch("Service4.routes.review_service.get_customer_reviews")
def test_get_customer_reviews(mock_get_customer_reviews, client):
    """
    Test the endpoint for retrieving customer reviews.

    This test mocks the `get_customer_reviews` function to return a predefined list of reviews.
    It then sends a GET request to the `/customer/1` endpoint and verifies the response.

    Args:
        mock_get_customer_reviews (Mock): Mock object for the `get_customer_reviews` function.
        client (FlaskClient): Test client for sending requests to the application.

    Assertions:
        - The response status code should be 200.
        - The length of the returned data should be 1.
    """
    mock_get_customer_reviews.return_value = [
        {"review_date": "2023-10-01", "review": "Great product!"}
    ]
    response = client.get("/customer/1")
    assert response.status_code == 200
    data = json.loads(response.data)
    assert len(data) == 1
