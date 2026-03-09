"""Security-related helpers."""

from __future__ import annotations

import os


def is_debug_enabled() -> bool:
    return os.environ.get("FLASK_DEBUG", "0") == "1"
