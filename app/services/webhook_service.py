import json
import urllib.request
import urllib.error


def send_order_status_webhook(user, payload):
    """Send order-status webhook if the user has a webhook URL configured."""
    if not user or not getattr(user, "webhook_url", None):
        return False

    url = user.webhook_url
    headers = {
        "Content-Type": "application/json",
    }
    if getattr(user, "api_key", None):
        headers["X-API-Key"] = user.api_key

    data = json.dumps(payload).encode("utf-8")
    request_obj = urllib.request.Request(url, data=data, headers=headers, method="POST")
    try:
        with urllib.request.urlopen(request_obj, timeout=10) as response:
            return 200 <= response.status < 300
    except urllib.error.HTTPError as exc:
        print(f"Webhook HTTP error for user {user.id}: {exc.code} - {exc.reason}")
    except urllib.error.URLError as exc:
        print(f"Webhook URL error for user {user.id}: {exc}")
    except Exception as exc:
        print(f"Webhook delivery failed for user {user.id}: {exc}")

    return False
