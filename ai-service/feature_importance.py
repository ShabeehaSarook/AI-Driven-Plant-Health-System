import joblib
import pandas as pd
import matplotlib.pyplot as plt

# Load trained model
model = joblib.load("models/plant_model.pkl")

# Feature names (MUST match training)
features = [
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

# Get importance values
importances = model.feature_importances_

# Create DataFrame
fi_df = pd.DataFrame({
    "Feature": features,
    "Importance": importances
}).sort_values(by="Importance", ascending=False)

print("\nFeature Importance Ranking:\n")
print(fi_df)

# Plot
plt.figure(figsize=(10, 6))
plt.barh(fi_df["Feature"], fi_df["Importance"])
plt.gca().invert_yaxis()
plt.title("Feature Importance - Plant Health Prediction")
plt.xlabel("Importance Score")
plt.tight_layout()
plt.show()
