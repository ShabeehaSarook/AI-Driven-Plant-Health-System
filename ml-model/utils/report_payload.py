"""Build report payloads from prediction records."""

from __future__ import annotations

from typing import Any, Dict


def build_report_payload_from_prediction(pred: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "prediction": pred.get("prediction"),
        "confidence": pred.get("confidence_text") or pred.get("confidence"),
        "explanation": pred.get("explanation") or [],
        "plant_message": pred.get("plant_message"),
    }
