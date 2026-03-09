from flask import Blueprint, request, jsonify
from bson import ObjectId

from utils.auth import admin_required
from utils.api_errors import ApiError
from utils.db import predictions_col, to_object_id
from datetime import datetime

admin_bp = Blueprint("admin", __name__)


@admin_bp.route("/admin/predictions", methods=["GET"])
@admin_required
def get_all_predictions():
    """Get all predictions (admin only)"""
    try:
        if predictions_col is None:
            raise ApiError("Database not available", status_code=500, code="db_unavailable")
        
        limit = request.args.get("limit", 100, type=int)
        skip = request.args.get("skip", 0, type=int)
        
        # Limit to reasonable bounds
        if limit > 500:
            limit = 500
        
        predictions = list(
            predictions_col.find()
            .sort("timestamp", -1)
            .skip(skip)
            .limit(limit)
        )
        
        # Convert ObjectId and datetime to string
        for pred in predictions:
            pred["_id"] = str(pred["_id"])
            if "timestamp" in pred and isinstance(pred["timestamp"], datetime):
                pred["timestamp"] = pred["timestamp"].isoformat()
        
        total_count = predictions_col.count_documents({})
        
        return jsonify({
            "predictions": predictions,
            "total": total_count,
            "limit": limit,
            "skip": skip
        }), 200
    
    except ApiError:
        raise
    except Exception as e:
        raise ApiError(f"Failed to retrieve predictions: {str(e)}", status_code=500, code="db_read_failed")


@admin_bp.route("/admin/predictions/<prediction_id>", methods=["DELETE"])
@admin_required
def delete_prediction(prediction_id):
    """Delete a prediction (admin only)"""
    try:
        if predictions_col is None:
            raise ApiError("Database not available", status_code=500, code="db_unavailable")
        
        oid = to_object_id(prediction_id)
        if not oid:
            raise ApiError("Invalid prediction ID", status_code=400, code="validation_error")
        
        result = predictions_col.delete_one({"_id": oid})
        
        if result.deleted_count == 0:
            raise ApiError("Prediction not found", status_code=404, code="not_found")
        
        return jsonify({"message": "Prediction deleted successfully"}), 200
    
    except ApiError:
        raise
    except Exception as e:
        raise ApiError(f"Failed to delete prediction: {str(e)}", status_code=500, code="db_delete_failed")


@admin_bp.route("/admin/predictions/<prediction_id>", methods=["PUT"])
@admin_required
def update_prediction(prediction_id):
    """Update a prediction (admin only)"""
    try:
        if predictions_col is None:
            raise ApiError("Database not available", status_code=500, code="db_unavailable")
        
        oid = to_object_id(prediction_id)
        if not oid:
            raise ApiError("Invalid prediction ID", status_code=400, code="validation_error")
        
        data = request.get_json()
        if not data:
            raise ApiError("Request body is required", status_code=400, code="validation_error")
        
        # Fields that can be updated
        allowed_fields = ["prediction", "confidence", "confidence_percent", "confidence_text", "explanation", "plant_message"]
        
        update_data = {}
        for field in allowed_fields:
            if field in data:
                update_data[field] = data[field]
        
        if not update_data:
            raise ApiError("No valid fields to update", status_code=400, code="validation_error")
        
        result = predictions_col.update_one(
            {"_id": oid},
            {"$set": update_data}
        )
        
        if result.matched_count == 0:
            raise ApiError("Prediction not found", status_code=404, code="not_found")
        
        # Get updated prediction
        updated_pred = predictions_col.find_one({"_id": oid})
        if updated_pred:
            updated_pred["_id"] = str(updated_pred["_id"])
            if "timestamp" in updated_pred and isinstance(updated_pred["timestamp"], datetime):
                updated_pred["timestamp"] = updated_pred["timestamp"].isoformat()
        
        return jsonify({
            "message": "Prediction updated successfully",
            "prediction": updated_pred
        }), 200
    
    except ApiError:
        raise
    except Exception as e:
        raise ApiError(f"Failed to update prediction: {str(e)}", status_code=500, code="db_update_failed")


@admin_bp.route("/admin/predictions", methods=["POST"])
@admin_required
def create_prediction():
    """Create a new prediction manually (admin only)"""
    try:
        if predictions_col is None:
            raise ApiError("Database not available", status_code=500, code="db_unavailable")
        
        data = request.get_json()
        if not data:
            raise ApiError("Request body is required", status_code=400, code="validation_error")
        
        # Required fields
        required_fields = ["user_id", "prediction", "input"]
        for field in required_fields:
            if field not in data:
                raise ApiError(f"Missing required field: {field}", status_code=400, code="validation_error")
        
        # Create prediction record
        record = {
            "user_id": str(data["user_id"]),
            "input": data["input"],
            "prediction": data["prediction"],
            "confidence": data.get("confidence", 0.0),
            "confidence_percent": data.get("confidence_percent", "0%"),
            "confidence_text": data.get("confidence_text", "Unknown"),
            "model_version": data.get("model_version", "manual"),
            "model_trained_at_utc": data.get("model_trained_at_utc", ""),
            "explanation": data.get("explanation", {}),
            "plant_message": data.get("plant_message", ""),
            "report": data.get("report", ""),
            "timestamp": datetime.now()
        }
        
        result = predictions_col.insert_one(record)
        record["_id"] = str(result.inserted_id)
        record["timestamp"] = record["timestamp"].isoformat()
        
        return jsonify({
            "message": "Prediction created successfully",
            "prediction": record
        }), 201
    
    except ApiError:
        raise
    except Exception as e:
        raise ApiError(f"Failed to create prediction: {str(e)}", status_code=500, code="db_create_failed")
