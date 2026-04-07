from flask import Blueprint, request, jsonify, g
from app.models.order_status import OrderStatus
from app.services.validation_service import ValidationService
from app.services.auth_service import require_api_key
from app.services.webhook_service import send_order_status_webhook
from app.extensions import db

status_bp = Blueprint("status", __name__, url_prefix="/api/v1/orders")

@status_bp.route("/<int:id>/status", methods=["GET"])
def get_status(id):
    statuses = OrderStatus.query.filter_by(id_order=id).all()
    return jsonify([{
        "id": s.id,
        "id_order": s.id_order,
        "quantidade": s.quantidade,
        "status": s.status
    } for s in statuses])

@status_bp.route("/<int:id>/status", methods=["POST"])
@require_api_key
def create_status(id):
    data = request.json or {}
    data["id_order"] = id  # Add the order id
    validation = ValidationService()
    validated_data, is_valid = validation.validate_payload(data, OrderStatus)
    if not is_valid:
        return jsonify({"errors": validated_data}), 400
    
    status_obj = OrderStatus(**validated_data)
    db.session.add(status_obj)
    db.session.flush()
    db.session.commit()

    send_order_status_webhook(g.current_user, {
        "event": "order_status.created",
        "order_status": {
            "id": status_obj.id,
            "id_order": status_obj.id_order,
            "quantidade": status_obj.quantidade,
            "status": status_obj.status
        }
    })
    
    return jsonify({"message": "created", "id": status_obj.id})

@status_bp.route("/<int:id>/status", methods=["PUT"])
@require_api_key
def update_status(id):
    s = OrderStatus.query.filter_by(id_order=id).first_or_404()
    data = request.json or {}
    # For update, update provided fields
    for key, value in data.items():
        if hasattr(s, key) and key not in ["id", "criado_em", "atualizado_em"]:
            setattr(s, key, value)
    
    db.session.commit()

    send_order_status_webhook(g.current_user, {
        "event": "order_status.updated",
        "order_status": {
            "id": s.id,
            "id_order": s.id_order,
            "quantidade": s.quantidade,
            "status": s.status
        }
    })

    return jsonify({"message": "updated"})
