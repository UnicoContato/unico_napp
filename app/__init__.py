import os

from flask import Flask, jsonify, send_file
from flask_swagger_ui import get_swaggerui_blueprint

from app.models.seller import Seller
from app.models.produto import Produto
from app.models.order import Order
from app.models.order_status import OrderStatus
from app.models.atributos import Atributo
from app.models.valores_atributos import ValoresAtributos
from app.models.produto_valor_atributo import ProdutoValorAtributo
from app.models.imagens import Imagem
from app.models.user import User
from app.routes.integration_routes import integration_bp
from app.routes.webhook_routes import webhook_bp
from app.routes.product_routes import product_bp
from app.routes.status_routes import status_bp
from app.routes.order_routes import order_bp
from app.routes.seller_routes import seller_bp
from app.routes.imagens_routes import imagens_bp
from app.routes.auth_routes import auth_bp
from .extensions import db
from .config import Config
from app.models import *



def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)

    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    openapi_path = os.path.join(project_root, "openapi.yaml")

    swagger_ui_blueprint = get_swaggerui_blueprint(
        "/docs",
        "/docs/openapi.yaml",
        config={
            "app_name": "Unico Napp API",
        },
    )
    app.register_blueprint(swagger_ui_blueprint, url_prefix="/docs")

    @app.route("/docs/openapi.yaml", methods=["GET"])
    def serve_openapi_spec():
        return send_file(openapi_path, mimetype="application/x-yaml")

    from app.routes.health import health_bp
    app.register_blueprint(health_bp)


    app.register_blueprint(integration_bp)
    app.register_blueprint(product_bp)
    app.register_blueprint(order_bp)
    app.register_blueprint(status_bp)
    app.register_blueprint(seller_bp)
    app.register_blueprint(imagens_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(webhook_bp)
    
    # Debug endpoint to list all routes
    @app.route("/debug/routes", methods=["GET"])
    def list_routes():
        routes = []
        for rule in app.url_map.iter_rules():
            routes.append({
                "endpoint": rule.endpoint,
                "methods": list(rule.methods - {"HEAD", "OPTIONS"}),
                "path": rule.rule
            })
        return jsonify(routes)

    @app.errorhandler(404)
    def handle_not_found(error):
        return jsonify({"errors": [{"codigo_erro": 1022, "descricao": "Recurso não encontrado"}]}), 404

    return app
