from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from extensions import limiter
import os
import logging

from predict_api import predict_with_confidence
from utils.db import save_prediction, get_predictions
from utils.db_reports import get_prediction_by_id, get_prediction_by_report_path, update_prediction_report
from utils.report_generator import generate_pdf_report
from utils.report_management import cleanup_reports
from utils.auth import token_required
from routes.auth_routes import auth_bp
from routes.admin_routes import admin_bp
from utils.api_errors import ApiError, error_response
from utils.validation import validate_prediction_input, validate_history_limit
from utils.report_payload import build_report_payload_from_prediction

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# --- Security / config ---
# In production, set these environment variables.
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "dev-secret-key-change-in-production")
app.config["JWT_EXPIRES_HOURS"] = int(os.environ.get("JWT_EXPIRES_HOURS", "24"))
app.config["ENV"] = os.environ.get("FLASK_ENV", os.environ.get("ENV", "production"))

# CORS: in development allow all origins to avoid localhost port mismatch issues.
# In production, set CORS_ORIGINS explicitly (comma-separated list).
# Example: CORS_ORIGINS=https://your-frontend.com,https://admin.your-frontend.com
cors_origins_raw = os.environ.get("CORS_ORIGINS")
if cors_origins_raw:
    cors_origins = [o.strip() for o in cors_origins_raw.split(",") if o.strip()]
else:
    # Local default: keep frontend unblocked even when React chooses another port.
    cors_origins = "*"

CORS(app, resources={r"/*": {"origins": cors_origins}})

# Rate limiting (memory storage by default). For multi-instance production, configure Redis.
# flask-limiter reads configuration from Flask app.config.
app.config["RATELIMIT_STORAGE_URI"] = os.environ.get("RATE_LIMIT_STORAGE_URI", "memory://")
limiter.init_app(app)

app.register_blueprint(auth_bp)
app.register_blueprint(admin_bp)

# Ensure MongoDB indexes (best-effort)
try:
    from utils.indexes import ensure_indexes

    ensure_indexes()
except Exception:
    logger.warning("Index initialization failed")

REPORTS_DIR = os.path.join(os.getcwd(), "reports")
os.makedirs(REPORTS_DIR, exist_ok=True)

# Report retention policy (days). Set to 0 to disable cleanup.
REPORT_RETENTION_DAYS = int(os.environ.get("REPORT_RETENTION_DAYS", "30"))

# Best-effort cleanup on startup
try:
    deleted = cleanup_reports(REPORTS_DIR, REPORT_RETENTION_DAYS)
    logger.info("Report cleanup deleted %s old file(s)", deleted)
except Exception:
    logger.warning("Report cleanup failed")


@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "message": "Smart Plant Health Monitoring API",
        "status": "running"
    }), 200


@app.errorhandler(ApiError)
def handle_api_error(err: ApiError):
    payload, status = error_response(err.message, status_code=err.status_code, code=err.code, details=err.details)
    return jsonify(payload), status


@app.errorhandler(404)
def not_found(_):
    payload, status = error_response("Not found", status_code=404, code="not_found")
    return jsonify(payload), status


@app.errorhandler(405)
def method_not_allowed(_):
    payload, status = error_response("Method not allowed", status_code=405, code="method_not_allowed")
    return jsonify(payload), status


@app.errorhandler(429)
def too_many_requests(_):
    payload, status = error_response("Too many requests", status_code=429, code="rate_limited")
    return jsonify(payload), status


@app.errorhandler(500)
def internal_error(_):
    payload, status = error_response("An internal error occurred", status_code=500, code="internal_error")
    return jsonify(payload), status


@app.route("/predict", methods=["POST"])
@token_required
def predict():
    input_data = request.get_json(silent=True)

    ok, msg, coerced, field_errors = validate_prediction_input(input_data)
    if not ok:
        raise ApiError(msg or "Invalid input", status_code=400, code="validation_error", details={"fields": field_errors} if field_errors else None)

    user_id = request.user["user_id"]

    # predict_api may raise ValueError or generic Exception
    try:
        result = predict_with_confidence(coerced)
    except ValueError as e:
        raise ApiError(str(e), status_code=400, code="validation_error")
    except Exception:
        raise ApiError("Prediction failed", status_code=500, code="prediction_failed")

    # Report generation
    try:
        # Cleanup before generating new reports (best-effort)
        try:
            cleanup_reports(REPORTS_DIR, REPORT_RETENTION_DAYS)
        except Exception:
            pass

        report_path = generate_pdf_report({
            "prediction": result.get("prediction"),
            "confidence": result.get("confidence_text") or result.get("confidence"),
            "explanation": result.get("explanation"),
            "plant_message": result.get("plant_message")
        }, reports_dir=REPORTS_DIR)
        result["report"] = f"/reports/{os.path.basename(report_path)}"
    except Exception:
        raise ApiError("Failed to generate report", status_code=500, code="report_failed")

    # Save to DB
    try:
        save_prediction({
            "user_id": user_id,
            "input": coerced,
            "prediction": result.get("prediction"),
            "confidence": result.get("confidence"),
            "confidence_percent": result.get("confidence_percent"),
            "confidence_text": result.get("confidence_text"),
            "model_version": result.get("model_version"),
            "model_trained_at_utc": result.get("model_trained_at_utc"),
            "explanation": result.get("explanation"),
            "plant_message": result.get("plant_message"),
            "report": result.get("report")
        })
    except Exception:
        raise ApiError("Failed to save prediction", status_code=500, code="db_save_failed")

    return jsonify(result), 200


@app.route("/history", methods=["GET"])
@token_required
def history():
    user_id = request.user["user_id"]

    ok, msg, limit = validate_history_limit(request.args.get("limit"), default=100)
    if not ok:
        raise ApiError(msg or "Invalid limit", status_code=400, code="validation_error")

    try:
        records = get_predictions(user_id=user_id, limit=limit)
        return jsonify(records), 200
    except Exception:
        raise ApiError("Failed to retrieve history", status_code=500, code="db_read_failed")


@app.route("/predictions/<prediction_id>/report/regenerate", methods=["POST"])
@token_required
def regenerate_report(prediction_id):
    """Regenerate a PDF report from stored prediction data.

    Security: user must own the prediction.
    """
    try:
        pred = get_prediction_by_id(prediction_id)
    except Exception:
        raise ApiError("Failed to load prediction", status_code=500, code="db_read_failed")

    if not pred:
        raise ApiError("Prediction not found", status_code=404, code="not_found")

    if str(pred.get("user_id")) != str(request.user.get("user_id")):
        raise ApiError("Forbidden", status_code=403, code="forbidden")

    # Cleanup best-effort
    try:
        cleanup_reports(REPORTS_DIR, REPORT_RETENTION_DAYS)
    except Exception:
        pass

    try:
        report_path = generate_pdf_report(build_report_payload_from_prediction(pred), reports_dir=REPORTS_DIR)
        new_route_path = f"/reports/{os.path.basename(report_path)}"
        update_prediction_report(prediction_id, new_route_path)
    except Exception:
        raise ApiError("Failed to regenerate report", status_code=500, code="report_failed")

    return jsonify({"message": "Report regenerated", "report": new_route_path}), 200


@app.route("/reports/<filename>", methods=["GET"])
@token_required
def download_report(filename):
    # Secure report access: user must be authenticated and must own the prediction
    if ".." in filename or "/" in filename or "\\" in filename:
        raise ApiError("Invalid filename", status_code=400, code="validation_error")

    file_path = os.path.join(REPORTS_DIR, filename)
    if not os.path.exists(file_path):
        raise ApiError("Report not found", status_code=404, code="not_found")

    report_route_path = f"/reports/{filename}"

    try:
        pred = get_prediction_by_report_path(report_route_path, user_id=str(request.user.get("user_id")))
    except Exception:
        raise ApiError("Failed to validate report ownership", status_code=500, code="db_read_failed")

    if not pred:
        # If we can't map report to a prediction, do not expose it.
        raise ApiError("Report not found", status_code=404, code="not_found")

    if str(pred.get("user_id")) != str(request.user.get("user_id")):
        raise ApiError("Forbidden", status_code=403, code="forbidden")

    try:
        return send_from_directory(REPORTS_DIR, filename, as_attachment=True)
    except Exception:
        raise ApiError("Failed to download report", status_code=500, code="report_download_failed")


if __name__ == "__main__":
    # Safe defaults: debug disabled unless explicitly enabled.
    debug = os.environ.get("FLASK_DEBUG", "0") == "1"
    host = os.environ.get("HOST", "127.0.0.1")
    port = int(os.environ.get("PORT", "5000"))
    app.run(host=host, port=port, debug=debug, use_reloader=False)
