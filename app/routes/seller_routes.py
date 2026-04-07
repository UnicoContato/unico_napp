from flask import Blueprint, request, jsonify
from app.models.seller import Seller
from app.services.validation_service import ValidationService
from app.extensions import db
from validate_docbr import CNPJ

seller_bp = Blueprint("seller", __name__, url_prefix="/api/v1/sellers")

@seller_bp.route("", methods=["GET"])
def list_sellers():
    cnpj = request.args.get("cnpj")
    nome = request.args.get("nome")
    offset = int(request.args.get("offset", 0))
    limit = int(request.args.get("limit", 10))

    query = Seller.query
    if cnpj:
        query = query.filter_by(cnpj=cnpj)
    if nome:
        query = query.filter(Seller.nome.ilike(f"%{nome}%"))

    sellers = query.offset(offset).limit(limit).all()
    return jsonify([{
        "id": s.id,
        "cnpj": s.cnpj,
        "nome": s.nome
    } for s in sellers])

@seller_bp.route("", methods=["POST"])
def create_seller():
    data = request.json or {}
    validation = ValidationService()
    validated_data, is_valid = validation.validate_payload(data, Seller)
    if not is_valid:
        return jsonify({"errors": validated_data}), 400

    # Validate CNPJ
    cnpj_validator = CNPJ()
    if not cnpj_validator.validate(validated_data.get("cnpj", "")):
        return jsonify({"errors": [{"codigo_erro": 1006, "descricao": "CNPJ inválido"}]}), 400

    # Check if CNPJ already exists
    existing_seller = Seller.query.filter_by(cnpj=validated_data["cnpj"]).first()
    if existing_seller:
        return jsonify({"errors": [{"codigo_erro": 1012, "descricao": "CNPJ já cadastrado"}]}), 409

    seller = Seller(**validated_data)
    db.session.add(seller)
    db.session.flush()
    db.session.commit()

    return jsonify({
        "id": seller.id,
        "cnpj": seller.cnpj,
        "nome": seller.nome,
        "message": "created"
    }), 201

@seller_bp.route("/<int:id>", methods=["GET"])
def get_seller(id):
    s = Seller.query.get_or_404(id)
    return jsonify({
        "id": s.id,
        "cnpj": s.cnpj,
        "nome": s.nome
    })
