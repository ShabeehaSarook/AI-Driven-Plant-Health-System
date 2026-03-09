import jwt
from functools import wraps
from flask import request, current_app
from datetime import datetime, timedelta, timezone

from utils.api_errors import ApiError


def create_token(user_id: str, email: str, role: str = "user", expires_in_hours: int | None = None):
    secret = current_app.config.get("SECRET_KEY")
    if not secret:
        raise ValueError("SECRET_KEY not configured")
    
    if expires_in_hours is None:
        expires_in_hours = int(current_app.config.get("JWT_EXPIRES_HOURS", 24))

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
            raise ApiError("Missing or invalid Authorization header", status_code=401, code="unauthorized")

        token = auth_header.split(" ")[1].strip()

        try:
            secret = current_app.config.get("SECRET_KEY")
            decoded = jwt.decode(token, secret, algorithms=["HS256"])

            user_id = decoded.get("id") or decoded.get("user_id")
            role = decoded.get("role", "user")

            if not user_id:
                raise ApiError("Invalid token payload", status_code=401, code="unauthorized")

            request.user = {
                "user_id": user_id,
                "role": role
            }

        except jwt.ExpiredSignatureError:
            raise ApiError("Token expired", status_code=401, code="unauthorized")
        except jwt.InvalidTokenError:
            raise ApiError("Invalid token", status_code=401, code="unauthorized")
        except Exception:
            raise ApiError("Invalid token", status_code=401, code="unauthorized")

        return f(*args, **kwargs)

    return decorated


def admin_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth_header = request.headers.get("Authorization")

        if not auth_header or not auth_header.startswith("Bearer "):
            raise ApiError("Missing or invalid Authorization header", status_code=401, code="unauthorized")

        token = auth_header.split(" ")[1].strip()

        try:
            secret = current_app.config.get("SECRET_KEY")
            decoded = jwt.decode(token, secret, algorithms=["HS256"])

            user_id = decoded.get("id") or decoded.get("user_id")
            role = decoded.get("role", "user")

            if not user_id:
                raise ApiError("Invalid token payload", status_code=401, code="unauthorized")

            if role != "admin":
                raise ApiError("Admin access required", status_code=403, code="forbidden")

            request.user = {
                "user_id": user_id,
                "role": role
            }

        except jwt.ExpiredSignatureError:
            raise ApiError("Token expired", status_code=401, code="unauthorized")
        except jwt.InvalidTokenError:
            raise ApiError("Invalid token", status_code=401, code="unauthorized")
        except ApiError:
            raise
        except Exception:
            raise ApiError("Invalid token", status_code=401, code="unauthorized")

        return f(*args, **kwargs)

    return decorated
