import os
from pathlib import Path

# Base directory
BASE_DIR = Path(__file__).resolve().parent.parent


class Config:
    """Base configuration class."""
    
    # Security
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret-key-change-in-production")
    JWT_EXPIRES_HOURS = int(os.environ.get("JWT_EXPIRES_HOURS", "24"))
    
    # Environment
    ENV = os.environ.get("FLASK_ENV", os.environ.get("ENV", "production"))
    DEBUG = os.environ.get("FLASK_DEBUG", "0") == "1"
    
    # Server
    HOST = os.environ.get("HOST", "127.0.0.1")
    PORT = int(os.environ.get("PORT", "5000"))
    
    # Database
    MONGODB_URI = os.environ.get("MONGODB_URI", "mongodb://localhost:27017/plant_health")
    MONGODB_DB_NAME = os.environ.get("MONGODB_DB_NAME", "plant_health")
    
    # Rate Limiting
    RATELIMIT_STORAGE_URI = os.environ.get("RATE_LIMIT_STORAGE_URI", "memory://")
    
    # CORS
    CORS_ORIGINS = os.environ.get("CORS_ORIGINS", "*")
    
    # Reports
    REPORTS_DIR = os.path.join(BASE_DIR, "reports")
    REPORT_RETENTION_DAYS = int(os.environ.get("REPORT_RETENTION_DAYS", "30"))
    
    # ML Models
    ML_MODELS_DIR = os.path.join(BASE_DIR, "ml_models")
    MODEL_PATH = os.path.join(ML_MODELS_DIR, "plant_model.pkl")
    MODEL_META_PATH = os.path.join(ML_MODELS_DIR, "plant_model.meta.json")
    
    # Data
    DATA_DIR = os.path.join(BASE_DIR, "data")
    TRAINING_DATA_PATH = os.path.join(DATA_DIR, "plant_health_data.csv")


class DevelopmentConfig(Config):
    """Development configuration."""
    DEBUG = True
    ENV = "development"


class ProductionConfig(Config):
    """Production configuration."""
    DEBUG = False
    ENV = "production"


class TestingConfig(Config):
    """Testing configuration."""
    TESTING = True
    ENV = "testing"
    MONGODB_DB_NAME = "plant_health_test"


# Configuration dictionary
config = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
    "testing": TestingConfig,
    "default": ProductionConfig
}
