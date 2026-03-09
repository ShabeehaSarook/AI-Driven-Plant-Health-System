import joblib
import numpy as np
import pandas as pd
import json
import sys
from pathlib import Path
from config.settings import Config
from app.utils.explain_prediction import generate_explanation
from app.utils.plant_communication import generate_plant_message


class MLService:
    """Service for ML model operations."""
    
    FEATURES = [
        'Plant_ID',
        'Soil_Moisture',
        'Ambient_Temperature',
        'Soil_Temperature',
        'Humidity',
        'Light_Intensity',
        'Soil_pH',
        'Nitrogen_Level',
        'Phosphorus_Level',
        'Potassium_Level',
        'Chlorophyll_Content',
        'Electrochemical_Signal'
    ]
    
    def __init__(self):
        self.model = None
        self.model_meta = {}
        self.load_model()
    
    def load_model(self):
        """Load the trained ML model."""
        model_path = Path(Config.MODEL_PATH)
        model_meta_path = Path(Config.MODEL_META_PATH)
        
        try:
            self.model = joblib.load(model_path)
        except FileNotFoundError:
            raise FileNotFoundError("Model file not found. Please run 'python train_model.py' first.")
        except Exception as e:
            raise Exception(f"Failed to load model: {e}")
        
        # Load model metadata
        try:
            if model_meta_path.exists():
                with open(model_meta_path, "r", encoding="utf-8") as f:
                    self.model_meta = json.load(f) or {}
        except Exception:
            self.model_meta = {}
    
    def predict(self, input_data):
        """Make a prediction using the ML model."""
        # Validate features
        missing_features = [f for f in self.FEATURES if f not in input_data]
        if missing_features:
            raise ValueError(f"Missing required features: {missing_features}")
        
        try:
            # Prepare data
            values = [input_data[feature] for feature in self.FEATURES]
            X = pd.DataFrame([values], columns=self.FEATURES)
            
            # Make prediction
            prediction = self.model.predict(X)[0]
            probabilities = self.model.predict_proba(X)[0]
            confidence_percent = round(max(probabilities) * 100, 2)
            
            # Generate explanation and message
            explanation = generate_explanation(self.model, self.FEATURES, X)
            plant_message = generate_plant_message(prediction, explanation)
            
            model_version = self.model_meta.get("model_version") or self.model_meta.get("trained_at_utc") or "unknown"
            
            return {
                "prediction": prediction,
                "confidence": f"{confidence_percent}%",
                "confidence_percent": confidence_percent,
                "confidence_text": f"{confidence_percent}%",
                "model_version": model_version,
                "model_trained_at_utc": self.model_meta.get("trained_at_utc"),
                "explanation": explanation,
                "plant_message": plant_message
            }
        except Exception as e:
            raise Exception(f"Prediction failed: {str(e)}")
    
    def what_if_simulation(self, base_input, changes):
        """Run a what-if scenario simulation."""
        simulated_input = base_input.copy()
        
        for key, value in changes.items():
            if key in simulated_input:
                simulated_input[key] = value
        
        return self.predict(simulated_input)
