from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os

# AI logic
from predict_api import predict_with_confidence

# MongoDB
from utils.db import save_prediction

# PDF Report
from utils.report_generator import generate_pdf_report

app = Flask(__name__)
CORS(app)

# 📂 Reports directory
REPORTS_DIR = os.path.join(os.getcwd(), "reports")


# -------------------------------
# HOME
# -------------------------------
@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "message": "AI-Driven Smart Plant Health API",
        "status": "running"
    })


# -------------------------------
# PREDICT
# -------------------------------
@app.route("/predict", methods=["POST"])
def predict():
    try:
        input_data = request.get_json()

        if not input_data:
            return jsonify({"error": "No input data provided"}), 400

        # 🔹 AI Prediction
        result = predict_with_confidence(input_data)

        # 🔹 Save to MongoDB
        save_prediction({
            "input": input_data,
            "prediction": result["prediction"],
            "confidence": result["confidence"],
            "explanation": result["explanation"],
            "plant_message": result.get("plant_message")
        })

        # 🔹 Generate PDF
        report_path = generate_pdf_report({
            "prediction": result["prediction"],
            "confidence": result["confidence"],
            "explanation": result["explanation"],
            "plant_message": result.get("plant_message")
        })

        # Attach relative URL
        result["report"] = f"/reports/{os.path.basename(report_path)}"

        return jsonify(result)

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# -------------------------------
# 📥 SERVE PDF FILES
# -------------------------------
@app.route("/reports/<filename>", methods=["GET"])
def download_report(filename):
    return send_from_directory(REPORTS_DIR, filename, as_attachment=True)


# -------------------------------
# RUN SERVER
# -------------------------------
if __name__ == "__main__":
    app.run(debug=True)
