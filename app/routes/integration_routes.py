from app.services.bulk_service import BulkService
from flask import Blueprint, request, jsonify


integration_bp = Blueprint("integration", __name__, url_prefix="/api/v1/integration")

@integration_bp.route("/products/bulk", methods=["POST"])
def bulk_products():
    data = request.get_json()
    result = BulkService().ingest(data)
    if result[1]:
        return jsonify(result[0]), 200
    return jsonify(result[0]), 400
