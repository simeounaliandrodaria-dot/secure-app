from flask import Flask, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

# In-memory user storage (for demonstration purpose)
users = {}

@app.route('/register', methods=['POST'])
def register():
    username = request.json['username']
    password = request.json['password']
    if username in users:
        return jsonify({'message': 'User already exists!'}), 400
    # Hash the password
    users[username] = generate_password_hash(password)
    return jsonify({'message': 'User registered successfully!'}), 201

@app.route('/login', methods=['POST'])
def login():
    username = request.json['username']
    password = request.json['password']
    if username not in users or not check_password_hash(users[username], password):
        return jsonify({'message': 'Invalid username or password!'}), 401
    return jsonify({'message': 'Logged in successfully!'}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)