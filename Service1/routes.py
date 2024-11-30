from customer_service import CustomerService
from flask import Blueprint, jsonify, request
from marshmallow import ValidationError

from serializers.customer_serializer import customer_schema, customers_schema

# Create a blueprint for customer routes
customer_bp = Blueprint("customer", __name__)

# Initialize customer service
customer_service = CustomerService()


@customer_bp.route("/register", methods=["POST"])
def register_customer():
    """
    Register a new customer
    """
    try:
        customer_schema.load(request.json)
        new_customer = customer_service.register_customer(request.json)
        return (
            jsonify(
                {
                    "message": "Customer registered successfully",
                    "customer": customer_schema.dump(new_customer),
                }
            ),
            201,
        )
    except ValidationError as err:
        return jsonify({"error": "Validation Error", "messages": err.messages}), 400
    except ValueError as err:
        return jsonify({"error": "Registration Error", "message": str(err)}), 409


@customer_bp.route("/delete/<username>", methods=["DELETE"])
def delete_customer(username):
    """
    Delete a customer by username
    """
    try:
        customer_service.delete_customer(username)
        return jsonify({"message": "Customer deleted successfully"}), 200
    except ValueError as err:
        return jsonify({"error": "Deletion Error", "message": str(err)}), 404


@customer_bp.route("/update/<username>", methods=["PUT"])
def update_customer(username):
    """
    Update customer information
    """
    try:
        # Validate incoming data (partial update)
        update_data = {k: v for k, v in request.json.items() if v is not None}

        updated_customer = customer_service.update_customer(username, update_data)

        return (
            jsonify(
                {
                    "message": "Customer updated successfully",
                    "customer": customer_schema.dump(updated_customer),
                }
            ),
            200,
        )
    except ValidationError as err:
        return jsonify({"error": "Validation Error", "messages": err.messages}), 400
    except ValueError as err:
        return jsonify({"error": "Update Error", "message": str(err)}), 404


@customer_bp.route("/all", methods=["GET"])
def get_all_customers():
    """
    Retrieve all customers
    """
    try:
        customers = customer_service.get_all_customers()
        return jsonify({"customers": customers_schema.dump(customers)}), 200
    except Exception as err:
        return jsonify({"error": "Retrieval Error", "message": str(err)}), 500


@customer_bp.route("/<username>", methods=["GET"])
def get_customer_by_username(username):
    """
    Retrieve customer by username
    """
    try:
        customer = customer_service.get_customer_by_username(username)
        if not customer:
            return jsonify({"error": "Not Found", "message": "Customer not found"}), 404

        return jsonify({"customer": customer_schema.dump(customer)}), 200
    except Exception as err:
        return jsonify({"error": "Retrieval Error", "message": str(err)}), 500


@customer_bp.route("/charge/<username>", methods=["POST"])
def charge_customer_wallet(username):
    """
    Charge customer wallet
    """
    try:
        amount = request.json.get("amount")
        if not amount or amount <= 0:
            return (
                jsonify(
                    {
                        "error": "Invalid Amount",
                        "message": "Amount must be a positive number",
                    }
                ),
                400,
            )

        new_balance = customer_service.charge_wallet(username, amount)

        return (
            jsonify(
                {"message": "Wallet charged successfully", "new_balance": new_balance}
            ),
            200,
        )
    except ValueError as err:
        return jsonify({"error": "Charge Error", "message": str(err)}), 400


@customer_bp.route("/deduct/<username>", methods=["POST"])
def deduct_customer_wallet(username):
    """
    Deduct money from customer wallet
    """
    try:
        amount = request.json.get("amount")
        if not amount or amount <= 0:
            return (
                jsonify(
                    {
                        "error": "Invalid Amount",
                        "message": "Amount must be a positive number",
                    }
                ),
                400,
            )

        new_balance = customer_service.deduct_wallet(username, amount)

        return (
            jsonify(
                {"message": "Wallet deducted successfully", "new_balance": new_balance}
            ),
            200,
        )
    except ValueError as err:
        return jsonify({"error": "Deduction Error", "message": str(err)}), 400
