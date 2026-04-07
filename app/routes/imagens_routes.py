from flask import Blueprint, request, jsonify
from app.models.imagens import Imagem
from app.models.produto import Produto
from app.services.validation_service import ValidationService
from app.extensions import db

imagens_bp = Blueprint("imagens", __name__, url_prefix="/api/v1/imagens")

@imagens_bp.route("", methods=["GET"])
def list_imagens():
    produto_id = request.args.get("produto_id")
    include_produto = request.args.get("include_produto", "false").lower() == "true"
    offset = int(request.args.get("offset", 0))
    limit = int(request.args.get("limit", 10))
    
    query = Imagem.query
    if produto_id:
        query = query.filter_by(id_produto=produto_id)
    
    imagens = query.offset(offset).limit(limit).all()
    
    result = []
    for i in imagens:
        img_data = {
            "id": i.id,
            "id_produto": i.id_produto,
            "link": i.link,
            "ordem": i.ordem
        }
        if include_produto:
            produto = Produto.query.get(i.id_produto)
            if produto:
                img_data["produto"] = {
                    "id": produto.id,
                    "nome": produto.nome,
                    "sku": produto.sku
                }
        result.append(img_data)
    
    return jsonify(result)

@imagens_bp.route("", methods=["POST"])
def create_imagem():
    data = request.json or {}
    validation = ValidationService()
    validated_data, is_valid = validation.validate_payload(data, Imagem)
    if not is_valid:
        return jsonify({"errors": validated_data}), 400

    produto = Produto.query.get(validated_data.get("id_produto"))
    if not produto:
        return jsonify({"errors": [{"codigo_erro": 1013, "descricao": "id_produto - produto não encontrado"}]}), 400

    imagem = Imagem(**validated_data)
    db.session.add(imagem)
    db.session.flush()
    db.session.commit()

    return jsonify({"id": imagem.id, "message": "created"}), 201

@imagens_bp.route("/<int:id>", methods=["GET"])
def get_imagem(id):
    i = Imagem.query.get_or_404(id)
    return jsonify({
        "id": i.id,
        "id_produto": i.id_produto,
        "link": i.link,
        "ordem": i.ordem
    })

@imagens_bp.route("/produto/<int:produto_id>", methods=["GET"])
def get_imagens_by_produto(produto_id):
    imagens = Imagem.query.filter_by(id_produto=produto_id).all()
    return jsonify([{
        "id": i.id,
        "id_produto": i.id_produto,
        "link": i.link,
        "ordem": i.ordem
    } for i in imagens])

@imagens_bp.route("/<int:id>", methods=["PUT"])
def update_image(id):
    image = Imagem.query.get_or_404(id)
    data = request.json or {}
    validation = ValidationService()
    validated_data, is_valid = validation.validate_payload(data, Imagem)
    if not is_valid:
        return jsonify({"errors": validated_data}), 400

    if "id_produto" in validated_data:
        produto = Produto.query.get(validated_data.get("id_produto"))
        if not produto:
            return jsonify({"errors": [{"codigo_erro": 1013, "descricao": "id_produto - produto não encontrado"}]}), 400

    for key, value in validated_data.items():
        setattr(image, key, value)

    db.session.commit()
    return jsonify({"message": "updated"})

@imagens_bp.route("/<int:id>", methods=["PATCH"])
def patch_image(id):
    image = Imagem.query.get_or_404(id)
    data = request.json or {}
    if "id_produto" in data:
        produto = Produto.query.get(data.get("id_produto"))
        if not produto:
            return jsonify({"errors": [{"codigo_erro": 1013, "descricao": "id_produto - produto não encontrado"}]}), 400

    for key, value in data.items():
        if hasattr(image, key) and key not in ["id", "criado_em", "atualizado_em"]:
            setattr(image, key, value)

    db.session.commit()
    return jsonify({"message": "updated"})

@imagens_bp.route("/<int:id>", methods=["DELETE"])
def delete_image(id):
    image = Imagem.query.get_or_404(id)
    db.session.delete(image)
    db.session.commit()
    return jsonify({"message": "deleted"})
