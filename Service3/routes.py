from datetime import datetime

from flask import Blueprint, jsonify, request
from marshmallow import ValidationError
from sale_service import SaleService

from serializers.sales_serializer import sale_list_schema, sale_schema

# Create a blueprint for sales routes
sales_bp = Blueprint("sales", __name__)

# Initialize sale service
sale_service = SaleService()


@sales_bp.route("/submit", methods=["POST"])
def submit_sale():
    """
    Submit a new sale
    """
    try:
        # Validate request data using the schema
        sale_schema.load(request.json)
        sale = sale_service.submit_sale(request.json)
        sale["sale_date"] = datetime.strptime(sale["sale_date"], "%Y-%m-%d")
        return (
            jsonify(
                {
                    "message": "Sale submitted successfully",
                    "sale": sale_schema.dump(sale),
                }
            ),
            201,
        )
    except ValidationError as err:
        return jsonify({"error": "Validation Error", "messages": err.messages}), 400
    except ValueError as err:
        return jsonify({"error": str(err)}), 400


@sales_bp.route("/update/<int:sale_id>", methods=["PUT"])
def update_sale(sale_id):
    """
    Update an existing sale
    """
    try:
        # Validate partial updates
        validated_data = sale_schema.load(request.json, partial=True)
        updated_sale = sale_service.update_sale(sale_id, request.json)
        if not updated_sale:
            return jsonify({"error": "Sale not found"}), 404
        updated_sale["sale_date"] = datetime.strptime(
            updated_sale["sale_date"], "%Y-%m-%d"
        )
        return (
            jsonify(
                {
                    "message": "Sale updated successfully",
                    "sale": sale_schema.dump(updated_sale),
                }
            ),
            200,
        )
    except ValidationError as err:
        return jsonify({"error": "Validation Error", "messages": err.messages}), 400
    except ValueError as err:
        return jsonify({"error": str(err)}), 400


@sales_bp.route("/delete/<int:sale_id>", methods=["DELETE"])
def delete_sale(sale_id):
    """
    Delete a sale by its ID
    """
    try:
        deleted_sale = sale_service.delete_sale(sale_id)
        if not deleted_sale:
            return jsonify({"error": "Sale not found"}), 404
        return jsonify(
            {
                "message": "Sale deleted successfully",
                "sale": sale_schema.dump(deleted_sale),
            }
        )
    except ValueError as err:
        return jsonify({"error": str(err)}), 400


@sales_bp.route("/customer/<int:customer_id>", methods=["GET"])
def get_customer_sales(customer_id):
    """
    Retrieve all sales for a specific customer
    """
    try:
        sales = sale_service.get_customer_sales(customer_id)
        return jsonify({"sales": sale_list_schema.dump(sales)})
    except ValueError as err:
        return jsonify({"error": str(err)}), 400


@sales_bp.route("/goods", methods=["GET"])
def get_available_goods():
    """
    Retrieve all available goods
    """
    try:
        goods = sale_service.get_available_goods()
        return jsonify({"goods": sale_list_schema.dump(goods)})
    except ValueError as err:
        return jsonify({"error": str(err)}), 400
