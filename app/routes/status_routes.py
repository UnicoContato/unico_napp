from flask import Blueprint, request, jsonify
from app.models.order_status import OrderStatus
from app.extensions import db

status_bp = Blueprint("status", __name__, url_prefix="/api/v1/orders")

@status_bp.route("/<int:id>/status", methods=["GET"])
def get_status(id):
    status = OrderStatus.query.filter_by(order_id=id).all()
    return jsonify([s.status for s in status])

@status_bp.route("/<int:id>/status", methods=["POST"])
def create_status(id):
    data = request.json

    status = OrderStatus(
        order_id=id,
        status=data.get("status"),
        quantity=data.get("quantity")
    )

    db.session.add(status)
    db.session.commit()

    return jsonify({"message": "created"})

@status_bp.route("/<int:id>/status", methods=["PUT"])
def update_status(id):
    s = OrderStatus.query.filter_by(order_id=id).first_or_404()
    data = request.json

    s.status = data.get("status", s.status)

    db.session.commit()
    return jsonify({"message": "updated"})
