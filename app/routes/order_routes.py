from flask import Blueprint, jsonify, request
from app.models.order import Order
from app.models.order_status import OrderStatus
from app.models.produto import Produto
from app.services.validation_service import ValidationService
from app.services.auth_service import require_api_key
from app.extensions import db

order_bp = Blueprint("order", __name__, url_prefix="/api/v1/orders")

@order_bp.route("", methods=["GET"])
@require_api_key
def list_orders():
    status = request.args.get("status")
    offset = int(request.args.get("offset", 0))
    limit = int(request.args.get("limit", 10))
    
    if status:
        orders = Order.query.join(OrderStatus, Order.id == OrderStatus.id_order).filter(OrderStatus.status == status).distinct()
    else:
        orders = Order.query
    
    orders = orders.offset(offset).limit(limit).all()
    
    return jsonify([{
        "id": o.id,
        "id_seller_contato": o.id_seller_contato,
        "id_produto": o.id_produto,
        "estoque": o.estoque,
        "preco": float(o.preco)
    } for o in orders])

@order_bp.route("", methods=["POST"])
def create_order():
    data = request.json or {}
    validation = ValidationService()
    validated_data, is_valid = validation.validate_payload(data, Order)
    if not is_valid:
        return jsonify({"errors": validated_data}), 400

    produto = Produto.query.get(validated_data.get("id_produto"))
    if not produto:
        return jsonify({"errors": [{"codigo_erro": 1013, "descricao": "id_produto - produto não encontrado"}]}), 400

    order = Order(**validated_data)
    db.session.add(order)
    db.session.flush()
    db.session.commit()

    return jsonify({"id": order.id, "message": "created"}), 201

@order_bp.route("/<int:id>", methods=["GET"])
def get_order(id):
    o = Order.query.get_or_404(id)
    return jsonify({
        "id": o.id,
        "id_seller_contato": o.id_seller_contato,
        "id_produto": o.id_produto,
        "estoque": o.estoque,
        "preco": float(o.preco)
    })

@order_bp.route("/seller/<int:seller_id>", methods=["GET"])
def get_orders_by_seller(seller_id):
    orders = Order.query.filter_by(id_seller_contato=seller_id).all()
    return jsonify([{
        "id": o.id,
        "id_seller_contato": o.id_seller_contato,
        "id_produto": o.id_produto,
        "estoque": o.estoque,
        "preco": float(o.preco)
    } for o in orders])

@order_bp.route("/produto/<int:produto_id>", methods=["GET"])
def get_orders_by_produto(produto_id):
    orders = Order.query.filter_by(id_produto=produto_id).all()
    return jsonify([{
        "id": o.id,
        "id_seller_contato": o.id_seller_contato,
        "id_produto": o.id_produto,
        "estoque": o.estoque,
        "preco": float(o.preco)
    } for o in orders])

@order_bp.route("/<int:id>", methods=["PUT"])
def update_order(id):
    o = Order.query.get_or_404(id)
    data = request.json
    validation = ValidationService()
    validated_data, is_valid = validation.validate_payload(data, Order)
    if not is_valid:
        return jsonify({"errors": validated_data}), 400

    if "id_produto" in validated_data:
        produto = Produto.query.get(validated_data.get("id_produto"))
        if not produto:
            return jsonify({"errors": [{"codigo_erro": 1013, "descricao": "id_produto - produto não encontrado"}]}), 400

    for key, value in validated_data.items():
        setattr(o, key, value)

    db.session.commit()
    return jsonify({"message": "updated"})

@order_bp.route("/<int:id>", methods=["PATCH"])
def patch_order(id):
    o = Order.query.get_or_404(id)
    data = request.json
    if "id_produto" in data:
        produto = Produto.query.get(data.get("id_produto"))
        if not produto:
            return jsonify({"errors": [{"codigo_erro": 1013, "descricao": "id_produto - produto não encontrado"}]}), 400

    # For PATCH, update only provided fields
    for key, value in data.items():
        if hasattr(o, key) and key not in ["id", "criado_em", "atualizado_em"]:
            setattr(o, key, value)

    db.session.commit()
    return jsonify({"message": "updated"})
