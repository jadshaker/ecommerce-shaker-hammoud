from unittest.mock import MagicMock, patch

import pytest
from review_service import ReviewService


@pytest.fixture
def review_service():
    """
    Fixture for setting up the ReviewService with a mocked Supabase client.

    This fixture patches the `get_supabase_client` method to return a mocked
    Supabase client, which is used to initialize the ReviewService. The fixture
    yields the initialized ReviewService instance for use in tests.

    Yields:
        ReviewService: An instance of ReviewService with a mocked Supabase client.
    """
    with patch("review_service.get_supabase_client") as mock_get_supabase_client:
        mock_supabase_client = MagicMock()
        mock_get_supabase_client.return_value = mock_supabase_client
        service = ReviewService()
        yield service


def test_submit_review_success(review_service):
    """
    Test the successful submission of a review.
    This test verifies that the `submit_review` method of the `review_service`
    correctly processes and returns the review data when a review is successfully
    submitted.
    Args:
        review_service: An instance of the review service being tested.
    Setup:
        - Mocks the `execute` method of the `insert` operation on the `supabase.table()`
          to return a MagicMock with the review data.
    Test Steps:
        1. Define the review data to be submitted.
        2. Mock the `execute` method to return the review data.
        3. Call the `submit_review` method with the review data.
        4. Assert that the response from `submit_review` matches the review data.
    Asserts:
        - The response from `submit_review` should be equal to the review data.
    """
    review_data = {
        "product_id": 1,
        "customer_id": 1,
        "rating": 5,
        "comment": "Great product!",
    }
    review_service.supabase.table().insert().execute.return_value = MagicMock(
        data=[review_data]
    )

    response = review_service.submit_review(review_data)

    assert response == review_data


def test_submit_review_failure(review_service):
    """
    Test the failure scenario of submitting a review.
    This test verifies that the `submit_review` method of the `review_service` raises
    a `ValueError` when the underlying database insert operation fails.
    Args:
        review_service (ReviewService): The review service instance to be tested.
    Raises:
        ValueError: If the review submission fails due to a database insert error.
    """
    review_data = {
        "product_id": 1,
        "customer_id": 1,
        "rating": 5,
        "comment": "Great product!",
    }
    review_service.supabase.table().insert().execute.side_effect = Exception(
        "Insert failed"
    )

    with pytest.raises(ValueError, match="Error submitting review: Insert failed"):
        review_service.submit_review(review_data)


def test_update_review_success(review_service):
    """
    Test the successful update of a review.
    This test verifies that the `update_review` method of the `review_service` correctly updates a review
    with the given `review_id` and `update_data`. It mocks the response from the database to ensure that
    the update operation returns the expected data.
    Args:
        review_service (ReviewService): The review service instance to be tested.
    Setup:
        - Mocks the database update operation to return the `update_data`.
    Test Steps:
        1. Define the `review_id` and `update_data`.
        2. Mock the database update operation to return the `update_data`.
        3. Call the `update_review` method with the `review_id` and `update_data`.
        4. Assert that the response from `update_review` matches the `update_data`.
    Asserts:
        - The response from `update_review` should be equal to the `update_data`.
    """
    review_id = 1
    update_data = {"rating": 4, "comment": "Good product"}
    review_service.supabase.table().update().eq().execute.return_value = MagicMock(
        data=[update_data]
    )

    response = review_service.update_review(review_id, update_data)

    assert response == update_data


def test_update_review_failure(review_service):
    """
    Test case for the failure scenario of updating a review.
    This test simulates a failure when attempting to update a review in the review service.
    It sets up the `review_service` mock to raise an exception when the update operation is executed.
    The test then verifies that the `update_review` method raises a `ValueError` with the expected error message.
    Args:
        review_service (Mock): A mock instance of the review service.
    Raises:
        ValueError: If the update operation fails, a ValueError with the message "Error updating review: Update failed" is expected to be raised.
    """
    review_id = 1
    update_data = {"rating": 4, "comment": "Good product"}
    review_service.supabase.table().update().eq().execute.side_effect = Exception(
        "Update failed"
    )

    with pytest.raises(ValueError, match="Error updating review: Update failed"):
        review_service.update_review(review_id, update_data)


def test_delete_review_success(review_service):
    """
    Test the successful deletion of a review.
    This test verifies that the `delete_review` method of the `review_service` correctly deletes a review
    and returns the expected response when the deletion is successful.
    Args:
        review_service (ReviewService): The review service instance to be tested.
    Setup:
        - Mocks the `execute` method of the `supabase.table().delete().eq()` chain to return a MagicMock
          with the expected data indicating the review has been deleted.
    Test Steps:
        1. Define a review ID to be deleted.
        2. Mock the `execute` method to return a response indicating the review with the given ID has been deleted.
        3. Call the `delete_review` method with the review ID.
        4. Assert that the response from `delete_review` matches the expected response.
    Asserts:
        - The response from `delete_review` should be a list containing a dictionary with the deleted review's ID.
    """
    review_id = 1
    review_service.supabase.table().delete().eq().execute.return_value = MagicMock(
        data=[{"id": review_id}]
    )

    response = review_service.delete_review(review_id)

    assert response == [{"id": review_id}]


def test_delete_review_failure(review_service):
    """
    Test case for the failure scenario of deleting a review.
    This test verifies that the `delete_review` method of the `review_service` raises a `ValueError`
    with the appropriate error message when the deletion operation fails.
    Args:
        review_service (ReviewService): The review service instance to be tested.
    Raises:
        ValueError: If the deletion operation fails, a `ValueError` with the message 
        "Error deleting review: Delete failed" is expected to be raised.
    """
    review_id = 1
    review_service.supabase.table().delete().eq().execute.side_effect = Exception(
        "Delete failed"
    )

    with pytest.raises(ValueError, match="Error deleting review: Delete failed"):
        review_service.delete_review(review_id)


def test_get_product_reviews_success(review_service):
    """
    Test the successful retrieval of product reviews.
    This test verifies that the `get_product_reviews` method of the `review_service`
    correctly retrieves and returns the reviews for a given product ID.
    Args:
        review_service (ReviewService): An instance of the review service being tested.
    Setup:
        - Mocks the `supabase.table().select().eq().execute` method to return a predefined
          list of reviews for the specified product ID.
    Test Steps:
        1. Define a product ID and a list of reviews associated with that product ID.
        2. Mock the `execute` method to return the predefined list of reviews.
        3. Call the `get_product_reviews` method with the product ID.
        4. Assert that the response from the method matches the predefined list of reviews.
    """
    product_id = 1
    reviews = [{"product_id": product_id, "rating": 5, "comment": "Great product!"}]
    review_service.supabase.table().select().eq().execute.return_value = MagicMock(
        data=reviews
    )

    response = review_service.get_product_reviews(product_id)

    assert response == reviews


def test_get_product_reviews_failure(review_service):
    """
    Test case for the `get_product_reviews` method in the `review_service` when it fails to retrieve product reviews.
    This test simulates a failure scenario where the `supabase.table().select().eq().execute` method raises an exception.
    It verifies that the `get_product_reviews` method raises a `ValueError` with the appropriate error message.
    Args:
        review_service: An instance of the review service to be tested.
    Raises:
        ValueError: If there is an error retrieving product reviews.
    """
    product_id = 1
    review_service.supabase.table().select().eq().execute.side_effect = Exception(
        "Select failed"
    )

    with pytest.raises(
        ValueError, match="Error retrieving product reviews: Select failed"
    ):
        review_service.get_product_reviews(product_id)


def test_get_customer_reviews_success(review_service):
    """
    Test the successful retrieval of customer reviews.
    This test verifies that the `get_customer_reviews` method of the `review_service`
    correctly retrieves and returns the reviews for a given customer ID.
    Args:
        review_service (ReviewService): An instance of the review service to be tested.
    Setup:
        - Mocks the `supabase.table().select().eq().execute` method to return a predefined
          list of reviews for the specified customer ID.
    Test Steps:
        1. Define a customer ID and a list of reviews associated with that customer.
        2. Mock the `execute` method of the `supabase` query to return the predefined reviews.
        3. Call the `get_customer_reviews` method with the customer ID.
        4. Assert that the response from the method matches the predefined list of reviews.
    Asserts:
        - The response from `get_customer_reviews` should match the predefined list of reviews.
    """
    customer_id = 1
    reviews = [{"customer_id": customer_id, "rating": 5, "comment": "Great product!"}]
    review_service.supabase.table().select().eq().execute.return_value = MagicMock(
        data=reviews
    )

    response = review_service.get_customer_reviews(customer_id)

    assert response == reviews


def test_get_customer_reviews_failure(review_service):
    """
    Test case for the `get_customer_reviews` method in the `review_service` when it fails to retrieve customer reviews.
    This test simulates a failure scenario where the `select` operation on the Supabase table raises an exception. It verifies that the `get_customer_reviews` method raises a `ValueError` with the appropriate error message when the `select` operation fails.
    Args:
        review_service: The review service instance being tested.
    Raises:
        ValueError: If the `get_customer_reviews` method raises a `ValueError` with the message "Error retrieving customer reviews: Select failed".
    """
    customer_id = 1
    review_service.supabase.table().select().eq().execute.side_effect = Exception(
        "Select failed"
    )

    with pytest.raises(
        ValueError, match="Error retrieving customer reviews: Select failed"
    ):
        review_service.get_customer_reviews(customer_id)


def test_moderate_review_success(review_service):
    """
    Test the moderate_review method of the review_service for a successful moderation.
    This test verifies that the moderate_review method correctly updates the moderation status
    of a review and returns the expected response.
    Args:
        review_service (MagicMock): A mock instance of the review service.
    Setup:
        - Mocks the return value of the supabase table update method to simulate a successful
          moderation update with the given review_id and moderation_status.
    Test Steps:
        1. Define the review_id and moderation_status to be used for the test.
        2. Mock the supabase table update method to return a response with the expected
           review_id and moderation_status.
        3. Call the moderate_review method with the review_id and moderation_status.
        4. Assert that the response from the moderate_review method matches the expected
           result.
    Asserts:
        - The response from the moderate_review method should be a dictionary containing
          the review_id and the updated moderation_status.
    """
    review_id = 1
    moderation_status = "approved"
    review_service.supabase.table().update().eq().execute.return_value = MagicMock(
        data=[{"id": review_id, "moderation_status": moderation_status}]
    )

    response = review_service.moderate_review(review_id, moderation_status)

    assert response == {"id": review_id, "moderation_status": moderation_status}


def test_moderate_review_failure(review_service):
    """
    Test the failure scenario of the `moderate_review` method in the `review_service`.
    This test verifies that when the `moderate_review` method encounters an exception
    during the update operation, it raises a `ValueError` with the appropriate error message.
    Args:
        review_service: A fixture that provides an instance of the review service.
    Raises:
        ValueError: If the `moderate_review` method fails to update the review status.
    """
    review_id = 1
    moderation_status = "approved"
    review_service.supabase.table().update().eq().execute.side_effect = Exception(
        "Update failed"
    )

    with pytest.raises(ValueError, match="Error moderating review: Update failed"):
        review_service.moderate_review(review_id, moderation_status)


def test_get_review_details_success(review_service):
    """
    Test the successful retrieval of review details.
    This test verifies that the `get_review_details` method of the 
    `review_service` correctly retrieves and returns the details of a 
    review when provided with a valid review ID.
    Args:
        review_service (ReviewService): An instance of the review service 
        being tested.
    Setup:
        - Mocks the response of the `supabase.table().select().eq().execute` 
          method to return a predefined review detail.
    Test Steps:
        1. Define a review ID and corresponding review details.
        2. Mock the `execute` method of the `supabase.table().select().eq()` 
           chain to return the predefined review details.
        3. Call the `get_review_details` method with the review ID.
        4. Assert that the response matches the predefined review details.
    Asserts:
        - The response from `get_review_details` matches the predefined 
          review details.
    """
    review_id = 1
    review_details = {"id": review_id, "rating": 5, "comment": "Great product!"}
    review_service.supabase.table().select().eq().execute.return_value = MagicMock(
        data=[review_details]
    )

    response = review_service.get_review_details(review_id)

    assert response == review_details


def test_get_review_details_failure(review_service):
    """
    Test case for the failure scenario of the `get_review_details` method in the `review_service`.
    This test simulates a failure when attempting to retrieve review details from the database.
    It mocks the `supabase.table().select().eq().execute` method to raise an exception with the message "Select failed".
    The test then asserts that the `get_review_details` method raises a `ValueError` with the expected error message.
    Args:
        review_service: The review service instance being tested.
    Raises:
        ValueError: If the `get_review_details` method does not raise a `ValueError` with the expected message.
    """
    review_id = 1
    review_service.supabase.table().select().eq().execute.side_effect = Exception(
        "Select failed"
    )

    with pytest.raises(
        ValueError, match="Error retrieving review details: Select failed"
    ):
        review_service.get_review_details(review_id)
