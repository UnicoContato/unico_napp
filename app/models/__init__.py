from app.extensions import db
from app.config import Config
from flask import Flask


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)

    from app.routes.health import health_bp
    app.register_blueprint(health_bp)

    return app