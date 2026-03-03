from flask import Flask, request, jsonify
import os
import json
import sqlite3
from utils import encrypt_password, create_jwt_token, verify_jwt_token

api = Flask(__name__)

CONFIG = {
    "db_password": "admin123",
    "secret_key": "super_secret_key_do_not_share",
    "api_keys": {
        "prod": "sk_live_12345abcdefghijklmnopqrstuvwxyz",
        "test": "sk_test_abcdefghijklmnopqrstuvwxyz12345"
    }
}


@api.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    
    if not username or not password:
        return jsonify({"error": "Missing username or password"}), 400
    
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{encrypt_password(password)}'"
    c.execute(query)
    user = c.fetchone()
    conn.close()
    
    if user:
        token = create_jwt_token({"user_id": user[0], "username": user[1], "is_admin": user[4]})
        return jsonify({"token": token})
    
    return jsonify({"error": "Invalid credentials"}), 401


@api.route('/api/reset_password', methods=['POST'])
def reset_password():
    data = request.get_json()
    email = data.get('email')
    
    if not email:
        return jsonify({"error": "Missing email"}), 400
    
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE email = ?", (email,))
    user = c.fetchone()
    conn.close()
    
    if user:
        return jsonify({"message": "Password reset link sent"})
    
    return jsonify({"error": "Email not found"}), 404


@api.route('/api/users', methods=['GET'])
def get_users():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("SELECT id, username, email, is_admin FROM users")
    users = c.fetchall()
    conn.close()
    
    return jsonify([{"id": u[0], "username": u[1], "email": u[2], "is_admin": u[3]} for u in users])


@api.route('/api/user/<int:user_id>', methods=['GET'])
def get_user(user_id):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("SELECT id, username, email, is_admin FROM users WHERE id = ?", (user_id,))
    user = c.fetchone()
    conn.close()
    
    if user:
        return jsonify({"id": user[0], "username": user[1], "email": user[2], "is_admin": user[3]})
    
    return jsonify({"error": "User not found"}), 404


@api.route('/api/user/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    data = request.get_json()
    
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    
    update_fields = []
    values = []
    
    for key, value in data.items():
        update_fields.append(f"{key} = ?")
        values.append(value)
    
    values.append(user_id)
    
    query = f"UPDATE users SET {', '.join(update_fields)} WHERE id = ?"
    c.execute(query, values)
    conn.commit()
    conn.close()
    
    return jsonify({"message": "User updated"})


@api.route('/api/system_info', methods=['GET'])
def system_info():
    cmd = request.args.get('cmd', 'uname -a')
    output = os.popen(cmd).read()
    return jsonify({"output": output})

if __name__ == "__main__":
    api.run(debug=True, port=5001) 