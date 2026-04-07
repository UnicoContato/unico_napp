from flask import Blueprint

health_bp = Blueprint("health", __name__, url_prefix="/api/v1/integration")

@health_bp.route("/health", methods=["GET"])
def health():
    return {"status": "ok"}