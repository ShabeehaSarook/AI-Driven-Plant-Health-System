import joblib
import numpy as np

# Explainable AI
from utils.explain_prediction import generate_explanation
from utils.plant_communication import generate_plant_message

# ================================
# LOAD TRAINED MODEL
# ================================
model = joblib.load("models/plant_model.pkl")

# ================================
# FEATURE ORDER (MUST MATCH TRAINING)
# ================================
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

# ================================
# CORE PREDICTION FUNCTION
# ================================
def predict_with_confidence(input_data: dict):
    """
    Returns:
    - prediction
    - confidence
    - explanation
    - plant_message
    """

    # Convert input dict to numpy array
    values = [input_data[feature] for feature in FEATURES]
    X = np.array(values).reshape(1, -1)

    # Prediction
    prediction = model.predict(X)[0]

    # Confidence
    probabilities = model.predict_proba(X)[0]
    confidence = round(max(probabilities) * 100, 2)

    # Explainable AI
    explanation = generate_explanation(model, FEATURES, X)

    # Plant communication
    plant_message = generate_plant_message(prediction, explanation)

    return {
        "prediction": prediction,
        "confidence": f"{confidence}%",
        "explanation": explanation,
        "plant_message": plant_message
    }

# ================================
# STEP 9 — WHAT-IF SIMULATION
# ================================
def what_if_simulation(base_input: dict, changes: dict):
    """
    Simulates changes in environment and re-predicts plant health
    """

    simulated_input = base_input.copy()

    for key, value in changes.items():
        if key in simulated_input:
            simulated_input[key] = value

    return predict_with_confidence(simulated_input)

# ================================
# LOCAL TESTING
# ================================
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
