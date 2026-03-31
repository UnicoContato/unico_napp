from flask import Blueprint, request, jsonify

webhook_bp = Blueprint("webhook", __name__, url_prefix="/api/v1/webhooks")

@webhook_bp.route("/order-status", methods=["POST"])
def webhook():
    print("Webhook received:", request.json)
    return jsonify({"message": "received"})
