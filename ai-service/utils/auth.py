import jwt
from functools import wraps
from flask import request, jsonify, current_app
from datetime import datetime, timedelta, timezone


def create_token(user_id: str, email: str, role: str = "user", expires_in_hours: int = 24):
    secret = current_app.config.get("SECRET_KEY")
    if not secret:
        raise ValueError("SECRET_KEY not configured")
    
    payload = {
        "user_id": user_id,
        "email": email,
        "role": role,
        "iat": datetime.now(timezone.utc),
        "exp": datetime.now(timezone.utc) + timedelta(hours=expires_in_hours)
    }
    
    token = jwt.encode(payload, secret, algorithm="HS256")
    return token


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth_header = request.headers.get("Authorization")

        if not auth_header or not auth_header.startswith("Bearer "):
            return jsonify({"error": "Missing or invalid Authorization header"}), 401

        token = auth_header.split(" ")[1].strip()

        try:
            secret = current_app.config.get("SECRET_KEY")
            decoded = jwt.decode(token, secret, algorithms=["HS256"])

            user_id = decoded.get("id") or decoded.get("user_id")
            role = decoded.get("role", "user")

            if not user_id:
                return jsonify({"error": "Invalid token payload"}), 401

            request.user = {
                "user_id": user_id,
                "role": role
            }

        except jwt.ExpiredSignatureError:
            return jsonify({"error": "Token expired"}), 401
        except jwt.InvalidTokenError:
            return jsonify({"error": "Invalid token"}), 401
        except Exception as e:
            return jsonify({"error": str(e)}), 401

        return f(*args, **kwargs)

    return decorated
