FEATURE_EXPLANATIONS = {
    "Soil_Moisture": "Soil moisture level is affecting water availability",
    "Ambient_Temperature": "High ambient temperature is increasing plant stress",
    "Soil_Temperature": "Soil temperature is impacting root activity",
    "Humidity": "Humidity level is influencing transpiration",
    "Light_Intensity": "Light intensity is affecting photosynthesis",
    "Soil_pH": "Soil pH is impacting nutrient absorption",
    "Nitrogen_Level": "Nitrogen deficiency affects plant growth",
    "Phosphorus_Level": "Phosphorus impacts root and flower development",
    "Potassium_Level": "Potassium supports overall plant immunity",
    "Chlorophyll_Content": "Low chlorophyll indicates reduced photosynthesis",
    "Electrochemical_Signal": "Electrochemical signals indicate plant stress"
}

def generate_explanation(model, feature_names, input_values):
    importances = model.feature_importances_

    feature_contributions = list(zip(feature_names, importances))
    feature_contributions.sort(key=lambda x: x[1], reverse=True)

    top_features = feature_contributions[:3]

    explanation = []
    for feature, _ in top_features:
        if feature in FEATURE_EXPLANATIONS:
            explanation.append(FEATURE_EXPLANATIONS[feature])

    return explanation
