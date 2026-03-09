from __future__ import annotations

import math
from typing import Dict, Tuple, Any

from predict_api import FEATURES
FEATURE_RULES = {
    "Plant_ID": (1, 9999),
    "Soil_Moisture": (0.0, 100.0),
    "Ambient_Temperature": (-10.0, 60.0),
    "Soil_Temperature": (-5.0, 60.0),
    "Humidity": (0.0, 100.0),
    "Light_Intensity": (0.0, 200000.0),
    "Soil_pH": (0.0, 14.0),
    "Nitrogen_Level": (0.0, 500.0),
    "Phosphorus_Level": (0.0, 500.0),
    "Potassium_Level": (0.0, 500.0),
    "Chlorophyll_Content": (0.0, 100.0),
    "Electrochemical_Signal": (0.0, 10.0),
}


def validate_prediction_input(input_data: Any) -> Tuple[bool, str | None, Dict[str, float] | None, Dict[str, str] | None]:
    """Validate and coerce input JSON for prediction.

    Returns:
      (is_valid, error_message, coerced_input, field_errors)

    - coerces feature values to float
    - rejects NaN/Infinity
    - range checks for known features
    """
    if not input_data:
        return False, "No input data provided", None, None

    if not isinstance(input_data, dict):
        return False, "Input data must be a JSON object", None, None

    missing = [f for f in FEATURES if f not in input_data]
    if missing:
        return False, f"Missing required features: {', '.join(missing)}", None, {f: "Missing" for f in missing}

    coerced: Dict[str, float] = {}
    field_errors: Dict[str, str] = {}

    for feature in FEATURES:
        raw = input_data.get(feature)
        try:
            val = float(raw)
        except (TypeError, ValueError):
            field_errors[feature] = "Must be a number"
            continue

        if not math.isfinite(val):
            field_errors[feature] = "Must be a finite number"
            continue

        if feature in FEATURE_RULES:
            mn, mx = FEATURE_RULES[feature]
            if val < mn or val > mx:
                field_errors[feature] = f"Must be between {mn} and {mx}"
                continue

        coerced[feature] = val

    if field_errors:
        return False, "Invalid input data", None, field_errors

    return True, None, coerced, None


def validate_history_limit(value: Any, default: int = 100) -> Tuple[bool, str | None, int | None]:
    """Validate history limit query param."""
    if value is None:
        return True, None, default

    try:
        limit = int(value)
    except (TypeError, ValueError):
        return False, "limit must be an integer", None

    if limit < 1 or limit > 500:
        return False, "Limit must be between 1 and 500", None

    return True, None, limit
