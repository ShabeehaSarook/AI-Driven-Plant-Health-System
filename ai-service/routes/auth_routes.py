from flask import Blueprint, request, jsonify
import bcrypt
import re

from utils.db import create_user, find_user_by_email
from utils.auth import create_token

auth_bp = Blueprint("auth", __name__)


def validate_email(email):
    if not email or not isinstance(email, str):
        return False
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None


def validate_password(password):
    if not password or not isinstance(password, str):
        return False, "Password is required"
    
    if len(password) < 8:
        return False, "Password must be at least 8 characters long"
    
    if len(password) > 128:
        return False, "Password must be less than 128 characters"
    
    return True, None


@auth_bp.route("/register", methods=["POST"])
def register():
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({"error": "Request body is required"}), 400
        
        email = data.get("email")
        password = data.get("password")

        if not validate_email(email):
            return jsonify({"error": "Invalid email format"}), 400
        
        is_valid, error_msg = validate_password(password)
        if not is_valid:
            return jsonify({"error": error_msg}), 400

        if find_user_by_email(email):
            return jsonify({"error": "User already exists"}), 409

        pw_hash = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
        user_id = create_user(email, pw_hash)

        token = create_token(user_id, email)
        return jsonify({"message": "Registered successfully", "token": token}), 201
    
    except Exception as e:
        return jsonify({"error": "Registration failed"}), 500


@auth_bp.route("/login", methods=["POST"])
def login():
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({"error": "Request body is required"}), 400
        
        email = data.get("email")
        password = data.get("password")

        if not email or not password:
            return jsonify({"error": "email and password are required"}), 400

        if not validate_email(email):
            return jsonify({"error": "Invalid email format"}), 400

        user = find_user_by_email(email)
        if not user:
            return jsonify({"error": "Invalid credentials"}), 401

        if not bcrypt.checkpw(password.encode("utf-8"), user["password_hash"]):
            return jsonify({"error": "Invalid credentials"}), 401

        token = create_token(str(user["_id"]), user["email"])
        return jsonify({"message": "Login successful", "token": token})
    
    except Exception as e:
        return jsonify({"error": "Login failed"}), 500
