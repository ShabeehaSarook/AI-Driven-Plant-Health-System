def generate_plant_message(prediction, explanation):
    if prediction == "Healthy":
        return {
            "plant_message": (
                "Plant is healthy. All conditions are optimal. "
                "Continue with current care routine."
            ),
            "plant_mood": "Healthy"
        }

    elif prediction == "Moderate Stress":
        return {
            "plant_message": (
                "Plant is experiencing moderate stress. "
                + " ".join(explanation)
                + ". Please take corrective action soon."
            ),
            "plant_mood": "Stressed"
        }

    elif prediction == "High Stress":
        return {
            "plant_message": (
                "Plant is under serious stress. "
                + " ".join(explanation)
                + ". Immediate attention is required."
            ),
            "plant_mood": "Critical"
        }

    else:
        return {
            "plant_message": (
                "Plant is experiencing unusual conditions. "
                "Please check the environment."
            ),
            "plant_mood": "Unknown"
        }
