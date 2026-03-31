from flask import Blueprint, jsonify, request
from app.models.produto import Produto
from app.extensions import db

product_bp = Blueprint("product", __name__, url_prefix="/api/v1/products")

@product_bp.route("", methods=["GET"])
def list_products():
    products = Produto.query.all()
    return jsonify([{"id": p.id, "sku": p.sku, "name": p.name} for p in products])

@product_bp.route("/<int:id>", methods=["GET"])
def get_product(id):
    p = Produto.query.get_or_404(id)
    return jsonify({"id": p.id, "sku": p.sku, "name": p.name})

@product_bp.route("/<int:id>", methods=["PUT"])
def update_product(id):
    p = Produto.query.get_or_404(id)
    data = request.json

    p.name = data.get("name", p.name)
    p.status = data.get("status", p.status)

    db.session.commit()
    return jsonify({"message": "updated"})
