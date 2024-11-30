from flask import Blueprint, jsonify, request
from inventory_service import InventoryService
from marshmallow import ValidationError

from serializers.product_serializer import product_schema

# Create a blueprint for inventory routes
inventory_bp = Blueprint("inventory", __name__)

# Initialize inventory service
inventory_service = InventoryService()


@inventory_bp.route("/add", methods=["POST"])
def add_goods():
    """
    Add a new product to inventory
    """
    try:
        product_schema.load(request.json)
        print(1)
        new_product = inventory_service.add_goods(request.json)
        print(2)
        return (
            jsonify(
                {
                    "message": "Product added successfully",
                    "product": product_schema.dump(new_product),
                }
            ),
            201,
        )
    except ValidationError as err:
        return jsonify({"error": "Validation Error", "messages": err.messages}), 400
    except ValueError as err:
        return jsonify({"error": "Addition Error", "message": str(err)}), 400


@inventory_bp.route("/deduct/<int:product_id>", methods=["POST"])
def deduct_goods(product_id):
    """
    Deduct a product from inventory
    """
    try:
        updated_product = inventory_service.deduct_goods(product_id)
        return (
            jsonify(
                {
                    "message": "Product deducted successfully",
                    "product": product_schema.dump(updated_product),
                }
            ),
            200,
        )
    except ValueError as err:
        return jsonify({"error": "Deduction Error", "message": str(err)}), 400


@inventory_bp.route("/update/<int:product_id>", methods=["PUT"])
def update_goods(product_id):
    """
    Update product fields
    """
    try:
        # Validate incoming data (partial update)
        update_data = {k: v for k, v in request.json.items() if v is not None}
        updated_product = inventory_service.update_goods(product_id, update_data)
        return (
            jsonify(
                {
                    "message": "Product updated successfully",
                    "product": product_schema.dump(updated_product),
                }
            ),
            200,
        )
    except ValidationError as err:
        return jsonify({"error": "Validation Error", "messages": err.messages}), 400
    except ValueError as err:
        return jsonify({"error": "Update Error", "message": str(err)}), 400
