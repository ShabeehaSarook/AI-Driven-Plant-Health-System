#!/usr/bin/env python3
"""
Main entry point for the Plant Health Monitoring API.
"""
import os
import logging
from app import create_app
from config.settings import Config

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

app = create_app()

if __name__ == "__main__":
    host = Config.HOST
    port = Config.PORT
    debug = Config.DEBUG
    
    logger.info(f"Starting Plant Health Monitoring API on {host}:{port}")
    logger.info(f"Environment: {Config.ENV}")
    logger.info(f"Debug mode: {debug}")
    
    # Create necessary directories
    os.makedirs(Config.REPORTS_DIR, exist_ok=True)
    os.makedirs(Config.ML_MODELS_DIR, exist_ok=True)
    
    app.run(host=host, port=port, debug=debug)
