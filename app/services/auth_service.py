from functools import wraps
from flask import request, jsonify, g
from app.models.user import User

def require_api_key(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        api_key = request.headers.get('X-API-Key')
        if not api_key:
            return jsonify({"error": "API key required"}), 401
        
        user = User.query.filter_by(api_key=api_key, ativo=True).first()
        if not user:
            return jsonify({"error": "Invalid API key"}), 401
        
        g.current_user = user
        return f(*args, **kwargs)
    return decorated_function