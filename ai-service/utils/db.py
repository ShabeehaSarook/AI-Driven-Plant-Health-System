from pymongo import MongoClient
from datetime import datetime


# Local MongoDB connection
client = MongoClient("mongodb://localhost:27017/")

# Database & collection
db = client["plant_health_db"]
collection = db["predictions"]

def save_prediction(data):
    record = {
        "input": data["input"],
        "prediction": data["prediction"],
        "confidence": data["confidence"],
        "explanation": data["explanation"],
        "plant_message": data.get("plant_message"),
        "timestamp": datetime.now()
    }

    collection.insert_one(record)
