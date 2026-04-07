from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/health")
def health():
    return jsonify({"status": "ok"}), 200

@app.route("/add", methods=["POST"])
def add():
    data = request.json
    # Bug: No input validation, allows non-numeric input and missing keys
    a = data.get("a")
    b = data.get("b")
    result = a + b  # Can error (TypeError) or produce string concat
    return jsonify({"result": result}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)