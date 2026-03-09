from flask import Blueprint, request, jsonify
import bcrypt
import re

from utils.db import create_user, find_user_by_email
from utils.auth import create_token
from utils.api_errors import ApiError
from extensions import limiter

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
@limiter.limit("5 per minute")
def register():
    try:
        data = request.get_json()
        
        if not data:
            raise ApiError("Request body is required", status_code=400, code="validation_error")
        
        email = data.get("email")
        password = data.get("password")

        if not validate_email(email):
            raise ApiError("Invalid email format", status_code=400, code="validation_error")
        
        is_valid, error_msg = validate_password(password)
        if not is_valid:
            raise ApiError(error_msg, status_code=400, code="validation_error")

        if find_user_by_email(email):
            raise ApiError("User already exists", status_code=409, code="conflict")

        pw_hash = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
        role = data.get("role", "user")  # Allow role in registration, default to "user"
        
        # Only allow "user" or "admin" roles
        if role not in ["user", "admin"]:
            role = "user"
        
        user_id = create_user(email, pw_hash, role)

        token = create_token(user_id, email, role)
        return jsonify({"message": "Registered successfully", "token": token, "user": {"id": user_id, "email": email, "role": role}}), 201
    
    except ApiError:
        raise
    except Exception:
        raise ApiError("Registration failed", status_code=500, code="registration_failed")


@auth_bp.route("/login", methods=["POST"])
@limiter.limit("10 per minute")
def login():
    try:
        data = request.get_json()
        
        if not data:
            raise ApiError("Request body is required", status_code=400, code="validation_error")
        
        email = data.get("email")
        password = data.get("password")

        if not email or not password:
            raise ApiError("email and password are required", status_code=400, code="validation_error")

        if not validate_email(email):
            raise ApiError("Invalid email format", status_code=400, code="validation_error")

        user = find_user_by_email(email)
        if not user:
            raise ApiError("Invalid credentials", status_code=401, code="unauthorized")

        if not bcrypt.checkpw(password.encode("utf-8"), user["password_hash"]):
            raise ApiError("Invalid credentials", status_code=401, code="unauthorized")

        role = user.get("role", "user")
        token = create_token(str(user["_id"]), user["email"], role)
        return jsonify({"message": "Login successful", "token": token, "user": {"id": str(user["_id"]), "email": user["email"], "role": role}}), 200
    
    except ApiError:
        raise
    except Exception:
        raise ApiError("Login failed", status_code=500, code="login_failed")
