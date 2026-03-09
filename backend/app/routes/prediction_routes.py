from flask import Blueprint, request, jsonify, send_from_directory
import os
import logging

from app.services.prediction_service import PredictionService
from app.utils.auth import token_required
from app.utils.api_errors import ApiError
from app.utils.validation import validate_prediction_input, validate_history_limit
from config.settings import Config

logger = logging.getLogger(__name__)

prediction_bp = Blueprint("prediction", __name__)

REPORTS_DIR = Config.REPORTS_DIR
os.makedirs(REPORTS_DIR, exist_ok=True)

prediction_service = PredictionService()


@prediction_bp.route("/predict", methods=["POST"])
@token_required
def predict():
    """Make a plant health prediction."""
    input_data = request.get_json(silent=True)

    ok, msg, coerced, field_errors = validate_prediction_input(input_data)
    if not ok:
        raise ApiError(msg or "Invalid input", status_code=400, code="validation_error", 
                      details={"fields": field_errors} if field_errors else None)

    user_id = request.user["user_id"]

    try:
        result = prediction_service.make_prediction(user_id, coerced, REPORTS_DIR)
        return jsonify(result), 200
    except ValueError as e:
        raise ApiError(str(e), status_code=400, code="validation_error")
    except Exception as e:
        logger.error(f"Prediction failed: {e}")
        raise ApiError("Prediction failed", status_code=500, code="prediction_failed")


@prediction_bp.route("/history", methods=["GET"])
@token_required
def history():
    """Get prediction history for the authenticated user."""
    user_id = request.user["user_id"]

    ok, msg, limit = validate_history_limit(request.args.get("limit"), default=100)
    if not ok:
        raise ApiError(msg or "Invalid limit", status_code=400, code="validation_error")

    try:
        records = prediction_service.get_user_history(user_id, limit)
        return jsonify(records), 200
    except Exception as e:
        logger.error(f"Failed to retrieve history: {e}")
        raise ApiError("Failed to retrieve history", status_code=500, code="db_read_failed")


@prediction_bp.route("/predictions/<prediction_id>/report/regenerate", methods=["POST"])
@token_required
def regenerate_report(prediction_id):
    """Regenerate a PDF report from stored prediction data."""
    try:
        result = prediction_service.regenerate_report(prediction_id, request.user["user_id"], REPORTS_DIR)
        return jsonify(result), 200
    except ValueError as e:
        raise ApiError(str(e), status_code=404, code="not_found")
    except PermissionError:
        raise ApiError("Forbidden", status_code=403, code="forbidden")
    except Exception as e:
        logger.error(f"Failed to regenerate report: {e}")
        raise ApiError("Failed to regenerate report", status_code=500, code="report_failed")


@prediction_bp.route("/reports/<filename>", methods=["GET"])
@token_required
def download_report(filename):
    """Download a PDF report."""
    if ".." in filename or "/" in filename or "\\" in filename:
        raise ApiError("Invalid filename", status_code=400, code="validation_error")

    file_path = os.path.join(REPORTS_DIR, filename)
    if not os.path.exists(file_path):
        raise ApiError("Report not found", status_code=404, code="not_found")

    try:
        is_authorized = prediction_service.verify_report_access(filename, request.user["user_id"])
        if not is_authorized:
            raise ApiError("Forbidden", status_code=403, code="forbidden")
        
        return send_from_directory(REPORTS_DIR, filename, as_attachment=True)
    except ApiError:
        raise
    except Exception as e:
        logger.error(f"Failed to download report: {e}")
        raise ApiError("Failed to download report", status_code=500, code="report_download_failed")
