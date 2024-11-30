from datetime import datetime

from flask import Blueprint, jsonify, request
from marshmallow import ValidationError
from review_service import ReviewService

from serializers.review_serializer import review_list_schema, review_schema

# Create a blueprint for reviews routes
reviews_bp = Blueprint("reviews", __name__)

# Initialize review service
review_service = ReviewService()


@reviews_bp.route("/submit", methods=["POST"])
def submit_review():
    """
    Submit a new review
    """
    try:
        # Validate request data using the schema
        review_schema.load(request.json)
        print(1)

        review = review_service.submit_review(request.json)
        print(2)
        print(review)
        review["review_date"] = datetime.strptime(review["review_date"], "%Y-%m-%d")
        return (
            jsonify(
                {
                    "message": "Review submitted successfully",
                    "review": review_schema.dump(review),
                }
            ),
            201,
        )
    except ValidationError as err:
        return jsonify({"error": "Validation Error", "messages": err.messages}), 400
    except ValueError as err:
        return jsonify({"error": str(err)}), 400


@reviews_bp.route("/update/<int:review_id>", methods=["PUT"])
def update_review(review_id):
    """
    Update an existing review
    """
    try:
        # Validate partial updates
        validated_data = review_schema.load(request.json, partial=True)
        updated_review = review_service.update_review(review_id, request.json)
        if not updated_review:
            return jsonify({"error": "Review not found"}), 404
        print(updated_review)
        updated_review["review_date"] = datetime.strptime(
            updated_review["review_date"], "%Y-%m-%d"
        )
        return (
            jsonify(
                {
                    "message": "Review updated successfully",
                    "review": review_schema.dump(updated_review),
                }
            ),
            200,
        )
    except ValidationError as err:
        return jsonify({"error": "Validation Error", "messages": err.messages}), 400
    except ValueError as err:
        return jsonify({"error": str(err)}), 400


@reviews_bp.route("/delete/<int:review_id>", methods=["DELETE"])
def delete_review(review_id):
    """
    Delete a review
    """
    try:
        deleted_review = review_service.delete_review(review_id)
        if not deleted_review:
            return jsonify({"error": "Review not found"}), 404

        return jsonify({"message": "Review deleted successfully"}), 200
    except ValueError as err:
        return jsonify({"error": str(err)}), 400


@reviews_bp.route("/product/<int:product_id>", methods=["GET"])
def get_product_reviews(product_id):
    """
    Retrieve all reviews for a specific product
    """
    try:
        reviews = review_service.get_product_reviews(product_id)
        for review in reviews:
            print(review)
            review["review_date"] = datetime.strptime(review["review_date"], "%Y-%m-%d")
        return jsonify(review_list_schema.dump(reviews)), 200
    except ValueError as err:
        return jsonify({"error": str(err)}), 400


@reviews_bp.route("/customer/<int:customer_id>", methods=["GET"])
def get_customer_reviews(customer_id):
    """
    Retrieve all reviews submitted by a specific customer
    """
    try:
        reviews = review_service.get_customer_reviews(customer_id)
        for review in reviews:
            print(review)
            review["review_date"] = datetime.strptime(review["review_date"], "%Y-%m-%d")
        return jsonify(review_list_schema.dump(reviews)), 200
    except ValueError as err:
        return jsonify({"error": str(err)}), 400
