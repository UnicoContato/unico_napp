from flask import Blueprint, request, jsonify, g
from app.models.user import User
from app.services.auth_service import require_api_key
from app.extensions import db
import secrets
import os

auth_bp = Blueprint("auth", __name__, url_prefix="/api/v1/auth")

@auth_bp.route("/register", methods=["POST"])
def register():
    admin_key = request.headers.get('X-Admin-Key')
    required_admin_key = os.getenv('ADMIN_API_KEY', 'default_admin_key_change_this')
    
    if admin_key != required_admin_key:
        return jsonify({"error": "Admin key required for registration"}), 403
    
    data = request.json or {}
    username = data.get("username")
    if not username:
        return jsonify({"error": "username required"}), 400
    
    existing = User.query.filter_by(username=username).first()
    if existing:
        return jsonify({"error": "username exists"}), 400
    
    api_key = secrets.token_hex(32)
    user = User(username=username, api_key=api_key)
    db.session.add(user)
    db.session.commit()
    
    return jsonify({"api_key": api_key, "user_id": user.id}), 201

@auth_bp.route("/me", methods=["GET"])
def me():
    api_key = request.headers.get('X-API-Key')
    user = User.query.filter_by(api_key=api_key, ativo=True).first()
    if not user:
        return jsonify({"error": "Invalid API key"}), 401
    
    return jsonify({
        "id": user.id,
        "username": user.username,
        "webhook_url": user.webhook_url
    }), 200

@auth_bp.route("/webhook", methods=["POST"])
@require_api_key
def set_webhook_url():
    data = request.json or {}
    webhook_url = data.get("webhook_url") or data.get("url")
    if not webhook_url:
        return jsonify({"error": "webhook_url is required"}), 400

    user = g.current_user
    user.webhook_url = webhook_url
    db.session.commit()

    return jsonify({"message": "webhook_url set", "webhook_url": user.webhook_url}), 200