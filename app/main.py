import os
from flask import Flask, request, jsonify
import re
from urllib.parse import urlparse

app = Flask(__name__)

DEBUG_MODE = os.getenv("FLASK_DEBUG", "False").lower() == "true"

def is_valid_url(url: str) -> bool:
    """Validates URL format to prevent SSRF."""
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc]) and result.scheme in ("http", "https")
    except Exception:
        return False

def sanitize_input(user_input: str) -> str:
    """Removes common XSS and injection characters."""
    return re.sub(r'[<>"\'%;()&+]', '', user_input)

@app.route("/health")
def health_check():
    return jsonify({"status": "healthy"}), 200

@app.route("/greet", methods=["GET"])
def greet():
    name = request.args.get("name", "World")
    if name:
        if len(name) > 50:
            return jsonify({"error": "Name too long"}), 400
        name = sanitize_input(name)
    return jsonify({"message": f"Hello, {name}!"})

@app.route("/validate-url", methods=["POST"])
def validate_url():
    data = request.get_json()
    if not data or "url" not in data:
        return jsonify({"error": "Missing URL"}), 400
    url = data["url"]
    if not isinstance(url, str):
        return jsonify({"error": "Invalid input type"}), 400
    valid = is_valid_url(url)
    return jsonify({"url": url, "valid": valid})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=DEBUG_MODE)
