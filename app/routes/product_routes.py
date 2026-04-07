from flask import Blueprint, jsonify, request
from app.models.produto import Produto
from app.models.imagens import Imagem
from app.models.produto_valor_atributo import ProdutoValorAtributo
from app.models.atributos import Atributo
from app.models.valores_atributos import ValoresAtributos
from app.services.validation_service import ValidationService
from app.services.auth_service import require_api_key
from app.extensions import db

product_bp = Blueprint("product", __name__, url_prefix="/api/v1/produtos")

@product_bp.route("", methods=["POST"])
@require_api_key
def create_product():
    data = request.json
    validation = ValidationService()
    validated_data, is_valid = validation.validate_payload(data, Produto)
    if not is_valid:
        return jsonify({"errors": validated_data}), 400
    
    # Check if product with same SKU already exists
    existing_product = Produto.query.filter_by(sku=validated_data["sku"]).first()
    if existing_product:
        return jsonify({"error": "Product with this SKU already exists"}), 409
    
    product = Produto(**validated_data)
    db.session.add(product)
    db.session.commit()
    
    return jsonify({
        "id": product.id,
        "sku": product.sku,
        "ean": product.ean,
        "nome": product.nome,
        "marca": product.marca,
        "descricao": product.descricao,
        "status": product.status,
        "message": "created"
    }), 201

@product_bp.route("", methods=["GET"])
@require_api_key
def list_products():
    sku = request.args.get("sku")
    status = request.args.get("status")
    offset = int(request.args.get("offset", 0))
    limit = int(request.args.get("limit", 10))
    
    query = Produto.query
    if sku:
        query = query.filter_by(sku=sku)
    if status:
        query = query.filter_by(status=status)
    
    products = query.offset(offset).limit(limit).all()
    return jsonify([{
        "id": p.id,
        "sku": p.sku,
        "ean": p.ean,
        "nome": p.nome,
        "marca": p.marca,
        "descricao": p.descricao,
        "status": p.status
    } for p in products])

@product_bp.route("/<int:id>", methods=["GET"])
@require_api_key
def get_product(id):
    p = Produto.query.get_or_404(id)
    
    # Get product images
    images = Imagem.query.filter_by(id_produto=id).order_by(Imagem.ordem).all()
    images_data = [{
        "id": img.id,
        "link": img.link,
        "ordem": img.ordem
    } for img in images]
    
    # Get product attributes
    attributes_data = {}
    product_attributes = ProdutoValorAtributo.query.filter_by(id_produto=id).all()
    for pa in product_attributes:
        attribute = Atributo.query.get(pa.id_atributo)
        value = ValoresAtributos.query.get(pa.id_valor_atributo)
        if attribute and value:
            attributes_data[attribute.nome] = value.valor
    
    return jsonify({
        "id": p.id,
        "sku": p.sku,
        "ean": p.ean,
        "nome": p.nome,
        "marca": p.marca,
        "descricao": p.descricao,
        "status": p.status,
        "imagens": images_data,
        "atributos": attributes_data
    })

@product_bp.route("/sku/<sku>", methods=["GET"])
@require_api_key
def get_product_by_sku(sku):
    p = Produto.query.filter_by(sku=sku).first_or_404()
    
    # Get product images
    images = Imagem.query.filter_by(id_produto=p.id).order_by(Imagem.ordem).all()
    images_data = [{
        "id": img.id,
        "link": img.link,
        "ordem": img.ordem
    } for img in images]
    
    # Get product attributes
    attributes_data = {}
    product_attributes = ProdutoValorAtributo.query.filter_by(id_produto=p.id).all()
    for pa in product_attributes:
        attribute = Atributo.query.get(pa.id_atributo)
        value = ValoresAtributos.query.get(pa.id_valor_atributo)
        if attribute and value:
            attributes_data[attribute.nome] = value.valor
    
    return jsonify({
        "id": p.id,
        "sku": p.sku,
        "ean": p.ean,
        "nome": p.nome,
        "marca": p.marca,
        "descricao": p.descricao,
        "status": p.status,
        "imagens": images_data,
        "atributos": attributes_data
    })

@product_bp.route("/ean/<ean>", methods=["GET"])
@require_api_key
def get_product_by_ean(ean):
    p = Produto.query.filter_by(ean=ean).first_or_404()
    
    # Get product images
    images = Imagem.query.filter_by(id_produto=p.id).order_by(Imagem.ordem).all()
    images_data = [{
        "id": img.id,
        "link": img.link,
        "ordem": img.ordem
    } for img in images]
    
    # Get product attributes
    attributes_data = {}
    product_attributes = ProdutoValorAtributo.query.filter_by(id_produto=p.id).all()
    for pa in product_attributes:
        attribute = Atributo.query.get(pa.id_atributo)
        value = ValoresAtributos.query.get(pa.id_valor_atributo)
        if attribute and value:
            attributes_data[attribute.nome] = value.valor
    
    return jsonify({
        "id": p.id,
        "sku": p.sku,
        "ean": p.ean,
        "nome": p.nome,
        "marca": p.marca,
        "descricao": p.descricao,
        "status": p.status,
        "imagens": images_data,
        "atributos": attributes_data
    })

@product_bp.route("/<int:id>", methods=["PUT"])
@require_api_key
def update_product(id):
    p = Produto.query.get_or_404(id)
    data = request.json
    validation = ValidationService()
    validated_data, is_valid = validation.validate_payload(data, Produto)
    if not is_valid:
        return jsonify({"errors": validated_data}), 400
    
    for key, value in validated_data.items():
        setattr(p, key, value)
    
    db.session.commit()
    return jsonify({"message": "updated"})

@product_bp.route("/<int:id>", methods=["PATCH"])
@require_api_key
def patch_product(id):
    p = Produto.query.get_or_404(id)
    data = request.json
    # For PATCH, we don't require all fields, so we'll update only provided fields
    for key, value in data.items():
        if hasattr(p, key) and key not in ["id", "criado_em", "atualizado_em"]:
            setattr(p, key, value)
    
    db.session.commit()
    return jsonify({"message": "updated"})

@product_bp.route("/<int:id>", methods=["DELETE"])
@require_api_key
def delete_product(id):
    p = Produto.query.get_or_404(id)
    db.session.delete(p)
    db.session.commit()
    return jsonify({"message": "deleted"})
