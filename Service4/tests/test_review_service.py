from unittest.mock import MagicMock, patch

import pytest
from review_service import ReviewService


@pytest.fixture
def review_service():
    with patch("review_service.get_supabase_client") as mock_get_supabase_client:
        mock_supabase_client = MagicMock()
        mock_get_supabase_client.return_value = mock_supabase_client
        service = ReviewService()
        yield service


def test_submit_review_success(review_service):
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
    review_id = 1
    update_data = {"rating": 4, "comment": "Good product"}
    review_service.supabase.table().update().eq().execute.return_value = MagicMock(
        data=[update_data]
    )

    response = review_service.update_review(review_id, update_data)

    assert response == update_data


def test_update_review_failure(review_service):
    review_id = 1
    update_data = {"rating": 4, "comment": "Good product"}
    review_service.supabase.table().update().eq().execute.side_effect = Exception(
        "Update failed"
    )

    with pytest.raises(ValueError, match="Error updating review: Update failed"):
        review_service.update_review(review_id, update_data)


def test_delete_review_success(review_service):
    review_id = 1
    review_service.supabase.table().delete().eq().execute.return_value = MagicMock(
        data=[{"id": review_id}]
    )

    response = review_service.delete_review(review_id)

    assert response == [{"id": review_id}]


def test_delete_review_failure(review_service):
    review_id = 1
    review_service.supabase.table().delete().eq().execute.side_effect = Exception(
        "Delete failed"
    )

    with pytest.raises(ValueError, match="Error deleting review: Delete failed"):
        review_service.delete_review(review_id)


def test_get_product_reviews_success(review_service):
    product_id = 1
    reviews = [{"product_id": product_id, "rating": 5, "comment": "Great product!"}]
    review_service.supabase.table().select().eq().execute.return_value = MagicMock(
        data=reviews
    )

    response = review_service.get_product_reviews(product_id)

    assert response == reviews


def test_get_product_reviews_failure(review_service):
    product_id = 1
    review_service.supabase.table().select().eq().execute.side_effect = Exception(
        "Select failed"
    )

    with pytest.raises(
        ValueError, match="Error retrieving product reviews: Select failed"
    ):
        review_service.get_product_reviews(product_id)


def test_get_customer_reviews_success(review_service):
    customer_id = 1
    reviews = [{"customer_id": customer_id, "rating": 5, "comment": "Great product!"}]
    review_service.supabase.table().select().eq().execute.return_value = MagicMock(
        data=reviews
    )

    response = review_service.get_customer_reviews(customer_id)

    assert response == reviews


def test_get_customer_reviews_failure(review_service):
    customer_id = 1
    review_service.supabase.table().select().eq().execute.side_effect = Exception(
        "Select failed"
    )

    with pytest.raises(
        ValueError, match="Error retrieving customer reviews: Select failed"
    ):
        review_service.get_customer_reviews(customer_id)


def test_moderate_review_success(review_service):
    review_id = 1
    moderation_status = "approved"
    review_service.supabase.table().update().eq().execute.return_value = MagicMock(
        data=[{"id": review_id, "moderation_status": moderation_status}]
    )

    response = review_service.moderate_review(review_id, moderation_status)

    assert response == {"id": review_id, "moderation_status": moderation_status}


def test_moderate_review_failure(review_service):
    review_id = 1
    moderation_status = "approved"
    review_service.supabase.table().update().eq().execute.side_effect = Exception(
        "Update failed"
    )

    with pytest.raises(ValueError, match="Error moderating review: Update failed"):
        review_service.moderate_review(review_id, moderation_status)


def test_get_review_details_success(review_service):
    review_id = 1
    review_details = {"id": review_id, "rating": 5, "comment": "Great product!"}
    review_service.supabase.table().select().eq().execute.return_value = MagicMock(
        data=[review_details]
    )

    response = review_service.get_review_details(review_id)

    assert response == review_details


def test_get_review_details_failure(review_service):
    review_id = 1
    review_service.supabase.table().select().eq().execute.side_effect = Exception(
        "Select failed"
    )

    with pytest.raises(
        ValueError, match="Error retrieving review details: Select failed"
    ):
        review_service.get_review_details(review_id)
