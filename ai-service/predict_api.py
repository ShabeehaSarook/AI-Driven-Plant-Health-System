import joblib
import numpy as np
import pandas as pd
from pathlib import Path
import sys

from utils.explain_prediction import generate_explanation
from utils.plant_communication import generate_plant_message

BASE_DIR = Path(__file__).resolve().parent
MODEL_PATH = BASE_DIR / "models" / "plant_model.pkl"

try:
    model = joblib.load(MODEL_PATH)
except FileNotFoundError:
    print(f"Model file not found. Please run 'python train_model.py' first.")
    sys.exit(1)
except Exception as e:
    print(f"Failed to load model: {e}")
    sys.exit(1)

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


def predict_with_confidence(input_data: dict):
    missing_features = [f for f in FEATURES if f not in input_data]
    if missing_features:
        raise ValueError(f"Missing required features: {missing_features}")
    
    try:
        values = [input_data[feature] for feature in FEATURES]
        X = pd.DataFrame([values], columns=FEATURES)

        prediction = model.predict(X)[0]
        probabilities = model.predict_proba(X)[0]
        confidence = round(max(probabilities) * 100, 2)

        explanation = generate_explanation(model, FEATURES, X)
        plant_message = generate_plant_message(prediction, explanation)

        return {
            "prediction": prediction,
            "confidence": f"{confidence}%",
            "explanation": explanation,
            "plant_message": plant_message
        }
    except Exception as e:
        raise Exception(f"Prediction failed: {str(e)}")


def what_if_simulation(base_input: dict, changes: dict):
    simulated_input = base_input.copy()

    for key, value in changes.items():
        if key in simulated_input:
            simulated_input[key] = value

    return predict_with_confidence(simulated_input)


if __name__ == "__main__":
    print("\n--- ORIGINAL PREDICTION ---")

    sample_input = {
        "Plant_ID": 1,
        "Soil_Moisture": 22.5,
        "Ambient_Temperature": 34.0,
        "Soil_Temperature": 30.2,
        "Humidity": 40.0,
        "Light_Intensity": 780,
        "Soil_pH": 5.8,
        "Nitrogen_Level": 18,
        "Phosphorus_Level": 10,
        "Potassium_Level": 15,
        "Chlorophyll_Content": 42,
        "Electrochemical_Signal": 1.2
    }

    original_result = predict_with_confidence(sample_input)
    print(original_result)

    print("\n--- WHAT-IF SIMULATION (Improved Conditions) ---")

    what_if_changes = {
        "Soil_Moisture": 55.0,
        "Humidity": 70.0,
        "Ambient_Temperature": 26.0
    }

    simulation_result = what_if_simulation(sample_input, what_if_changes)
    print(simulation_result)
