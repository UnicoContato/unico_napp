from flask import Blueprint, request, jsonify
from app.services.integration_service import process_products_bulk

integration_bp = Blueprint("integration", __name__, url_prefix="/api/v1/integration")

@integration_bp.route("/products/bulk", methods=["POST"])
def bulk_products():
    data = request.get_json()
    result = process_products_bulk(data)
    return jsonify(result), 200
