from app.routes.integration_routes import integration_bp
from app.routes.webhook_routes import webhook_bp
from app.routes.product_routes import product_bp
from app.routes.status_routes import status_bp
from app.routes.order_routes import order_bp
from .extensions import db
from .config import Config
from flask import Flask


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)

    from app.routes.health import health_bp
    app.register_blueprint(health_bp)


    app.register_blueprint(integration_bp)
    app.register_blueprint(product_bp)
    app.register_blueprint(order_bp)
    app.register_blueprint(status_bp)
    app.register_blueprint(webhook_bp)
    return app
