from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os
import logging

from predict_api import predict_with_confidence, FEATURES
from utils.db import save_prediction, get_predictions
from utils.report_generator import generate_pdf_report
from utils.auth import token_required
from routes.auth_routes import auth_bp

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)

app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "dev-secret-key-change-in-production")

app.register_blueprint(auth_bp)

REPORTS_DIR = os.path.join(os.getcwd(), "reports")
os.makedirs(REPORTS_DIR, exist_ok=True)


@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "message": "Smart Plant Health Monitoring API",
        "status": "running"
    })


def validate_input_data(input_data):
    if not input_data:
        return False, "No input data provided"
    
    if not isinstance(input_data, dict):
        return False, "Input data must be a JSON object"
    
    missing_features = [f for f in FEATURES if f not in input_data]
    if missing_features:
        return False, f"Missing required features: {', '.join(missing_features)}"
    
    for feature in FEATURES:
        if feature not in input_data:
            continue
            
        value = input_data[feature]
        try:
            float_value = float(value)
            input_data[feature] = float_value
        except (ValueError, TypeError):
            return False, f"Invalid value for {feature}: must be a number"
    
    return True, None


@app.route("/predict", methods=["POST"])
@token_required
def predict():
    try:
        input_data = request.get_json()

        is_valid, error_message = validate_input_data(input_data)
        if not is_valid:
            return jsonify({"error": error_message}), 400

        user_id = request.user["user_id"]
        result = predict_with_confidence(input_data)

        report_path = generate_pdf_report({
            "prediction": result["prediction"],
            "confidence": result["confidence"],
            "explanation": result["explanation"],
            "plant_message": result.get("plant_message")
        })

        result["report"] = f"/reports/{os.path.basename(report_path)}"

        save_prediction({
            "user_id": user_id,
            "input": input_data,
            "prediction": result["prediction"],
            "confidence": result["confidence"],
            "explanation": result["explanation"],
            "plant_message": result.get("plant_message"),
            "report": result["report"]
        })

        return jsonify(result)

    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": "An internal error occurred"}), 500


@app.route("/history", methods=["GET"])
@token_required
def history():
    try:
        user_id = request.user["user_id"]
        limit = request.args.get("limit", 100, type=int)
        
        if limit < 1 or limit > 500:
            return jsonify({"error": "Limit must be between 1 and 500"}), 400
        
        records = get_predictions(user_id=user_id, limit=limit)
        return jsonify(records)
    except Exception as e:
        return jsonify({"error": "Failed to retrieve history"}), 500


@app.route("/reports/<filename>", methods=["GET"])
def download_report(filename):
    try:
        if ".." in filename or "/" in filename or "\\" in filename:
            return jsonify({"error": "Invalid filename"}), 400
        
        file_path = os.path.join(REPORTS_DIR, filename)
        if not os.path.exists(file_path):
            return jsonify({"error": "Report not found"}), 404
        
        return send_from_directory(REPORTS_DIR, filename, as_attachment=True)
    except Exception as e:
        return jsonify({"error": "Failed to download report"}), 500


if __name__ == "__main__":
    app.run(debug=True, use_reloader=False)
