from flask import Blueprint, jsonify, request
from app.models.order import Order
from app.extensions import db

order_bp = Blueprint("order", __name__, url_prefix="/api/v1/orders")

@order_bp.route("", methods=["GET"])
def list_orders():
    orders = Order.query.all()
    return jsonify([{"id": o.id, "price": float(o.price)} for o in orders])

@order_bp.route("/<int:id>", methods=["GET"])
def get_order(id):
    o = Order.query.get_or_404(id)
    return jsonify({"id": o.id})

@order_bp.route("/<int:id>", methods=["PUT"])
def update_order(id):
    o = Order.query.get_or_404(id)
    data = request.json

    o.price = data.get("price", o.price)
    o.stock = data.get("stock", o.stock)

    db.session.commit()
    return jsonify({"message": "updated"})
