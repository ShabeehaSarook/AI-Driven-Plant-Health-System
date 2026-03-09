import os
import logging
from app.services.ml_service import MLService
from app.utils.db import save_prediction, get_predictions
from app.utils.db_reports import get_prediction_by_id, get_prediction_by_report_path, update_prediction_report
from app.utils.report_generator import generate_pdf_report
from app.utils.report_management import cleanup_reports
from app.utils.report_payload import build_report_payload_from_prediction
from config.settings import Config

logger = logging.getLogger(__name__)


class PredictionService:
    """Service for handling plant health predictions."""
    
    def __init__(self):
        self.ml_service = MLService()
        self.report_retention_days = Config.REPORT_RETENTION_DAYS
    
    def make_prediction(self, user_id, input_data, reports_dir):
        """Make a prediction and generate report."""
        # Get ML prediction
        result = self.ml_service.predict(input_data)
        
        # Generate PDF report
        try:
            cleanup_reports(reports_dir, self.report_retention_days)
        except Exception as e:
            logger.warning(f"Report cleanup failed: {e}")
        
        try:
            report_path = generate_pdf_report({
                "prediction": result.get("prediction"),
                "confidence": result.get("confidence_text") or result.get("confidence"),
                "explanation": result.get("explanation"),
                "plant_message": result.get("plant_message")
            }, reports_dir=reports_dir)
            result["report"] = f"/reports/{os.path.basename(report_path)}"
        except Exception as e:
            logger.error(f"Report generation failed: {e}")
            raise Exception("Failed to generate report")
        
        # Save to database
        try:
            save_prediction({
                "user_id": user_id,
                "input": input_data,
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
        except Exception as e:
            logger.error(f"Failed to save prediction: {e}")
            raise Exception("Failed to save prediction")
        
        return result
    
    def get_user_history(self, user_id, limit=100):
        """Get prediction history for a user."""
        return get_predictions(user_id=user_id, limit=limit)
    
    def regenerate_report(self, prediction_id, user_id, reports_dir):
        """Regenerate a PDF report from stored prediction."""
        pred = get_prediction_by_id(prediction_id)
        
        if not pred:
            raise ValueError("Prediction not found")
        
        if str(pred.get("user_id")) != str(user_id):
            raise PermissionError("Forbidden")
        
        # Cleanup old reports
        try:
            cleanup_reports(reports_dir, self.report_retention_days)
        except Exception as e:
            logger.warning(f"Report cleanup failed: {e}")
        
        # Generate new report
        report_path = generate_pdf_report(
            build_report_payload_from_prediction(pred), 
            reports_dir=reports_dir
        )
        new_route_path = f"/reports/{os.path.basename(report_path)}"
        update_prediction_report(prediction_id, new_route_path)
        
        return {"message": "Report regenerated", "report": new_route_path}
    
    def verify_report_access(self, filename, user_id):
        """Verify if user has access to a report."""
        report_route_path = f"/reports/{filename}"
        pred = get_prediction_by_report_path(report_route_path, user_id=str(user_id))
        
        if not pred:
            return False
        
        if str(pred.get("user_id")) != str(user_id):
            return False
        
        return True
