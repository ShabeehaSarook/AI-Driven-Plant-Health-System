"""API error/response helpers.

Goal: provide consistent JSON response shape across the Flask API.

We keep an `error` string field for backward compatibility with the frontend,
while also providing a structured envelope.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, Optional


@dataclass
class ApiError(Exception):
    message: str
    status_code: int = 400
    code: str = "bad_request"
    details: Optional[Dict[str, Any]] = None


def error_response(message: str, status_code: int = 400, code: str = "bad_request", details: Optional[Dict[str, Any]] = None):
    """Standard error JSON.

    Includes `error` for existing frontend code and a structured payload.
    """
    payload: Dict[str, Any] = {
        "success": False,
        "error": message,
        "code": code,
    }
    if details:
        payload["details"] = details
    return payload, status_code


def success_response(data: Any = None, status_code: int = 200):
    payload: Dict[str, Any] = {"success": True}
    if data is not None:
        payload["data"] = data
    return payload, status_code
