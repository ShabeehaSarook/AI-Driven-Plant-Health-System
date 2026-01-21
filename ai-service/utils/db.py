from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, PyMongoError
from datetime import datetime
from bson import ObjectId
import os

MONGO_URI = os.environ.get("MONGODB_URI", "mongodb://localhost:27017/")
DB_NAME = os.environ.get("DB_NAME", "plant_health_db")

try:
    client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
    client.admin.command('ping')
    db = client[DB_NAME]
    predictions_col = db["predictions"]
    users_col = db["users"]
except:
    client = None
    db = None
    predictions_col = None
    users_col = None


def to_object_id(value):
    try:
        return ObjectId(str(value))
    except Exception:
        return None


def save_prediction(data: dict):
    if predictions_col is None:
        raise Exception("Database not available")
    
    try:
        record = {
            "user_id": str(data.get("user_id")) if data.get("user_id") else None,
            "input": data.get("input"),
            "prediction": data.get("prediction"),
            "confidence": data.get("confidence"),
            "explanation": data.get("explanation"),
            "plant_message": data.get("plant_message"),
            "report": data.get("report"),
            "timestamp": datetime.now()
        }
        result = predictions_col.insert_one(record)
        return result.inserted_id
    except PyMongoError as e:
        raise Exception(f"Failed to save prediction: {str(e)}")


def get_predictions(user_id=None, limit=50):
    if predictions_col is None:
        raise Exception("Database not available")
    
    try:
        query = {}
        if user_id:
            query["user_id"] = str(user_id)

        data = list(
            predictions_col.find(query)
            .sort("timestamp", -1)
            .limit(limit)
        )

        for d in data:
            d["_id"] = str(d["_id"])
            if "timestamp" in d and isinstance(d["timestamp"], datetime):
                d["timestamp"] = d["timestamp"].isoformat()

        return data
    except PyMongoError as e:
        raise Exception(f"Failed to retrieve predictions: {str(e)}")


def create_user(email: str, password_hash: bytes):
    if users_col is None:
        raise Exception("Database not available")
    
    try:
        user = {
            "email": email,
            "password_hash": password_hash,
            "created_at": datetime.now()
        }
        result = users_col.insert_one(user)
        return str(result.inserted_id)
    except PyMongoError as e:
        raise Exception(f"Failed to create user: {str(e)}")


def find_user_by_email(email: str):
    if users_col is None:
        raise Exception("Database not available")
    
    try:
        return users_col.find_one({"email": email})
    except PyMongoError as e:
        raise Exception(f"Failed to query user: {str(e)}")


def find_user_by_id(user_id: str):
    if users_col is None:
        raise Exception("Database not available")
    
    try:
        oid = to_object_id(user_id)
        if not oid:
            return None
        return users_col.find_one({"_id": oid})
    except PyMongoError as e:
        raise Exception(f"Failed to query user: {str(e)}")
