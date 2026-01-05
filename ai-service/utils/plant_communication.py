def generate_plant_message(prediction, explanation):
    """
    Converts prediction + explanation into natural language plant communication
    """

    if prediction == "Healthy":
        return {
            "plant_message": (
                "I'm feeling great 🌿! All conditions are optimal. "
                "Thank you for taking good care of me."
            ),
            "plant_mood": "😊 Happy"
        }

    elif prediction == "Moderate Stress":
        return {
            "plant_message": (
                "I'm feeling a bit stressed 😟. "
                + " ".join(explanation)
                + ". Please take corrective action soon."
            ),
            "plant_mood": "😐 Stressed"
        }

    elif prediction == "High Stress":
        return {
            "plant_message": (
                "I'm under serious stress 🚨. "
                + " ".join(explanation)
                + ". Immediate attention is required to save me."
            ),
            "plant_mood": "😞 Critical"
        }

    else:
        return {
            "plant_message": (
                "I'm experiencing unusual conditions. "
                "Please check my environment."
            ),
            "plant_mood": "⚠️ Unknown"
        }
