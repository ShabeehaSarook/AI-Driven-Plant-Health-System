from flask import Flask
from flask_cors import CORS
from app.extensions import limiter
import os
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def create_app():
    """Application factory pattern for Flask app."""
    app = Flask(__name__)

    # Load configuration
    from config.settings import Config
    app.config.from_object(Config)

    # Initialize CORS
    cors_origins_raw = os.environ.get("CORS_ORIGINS")
    if cors_origins_raw:
        cors_origins = [o.strip() for o in cors_origins_raw.split(",") if o.strip()]
    else:
        cors_origins = "*"
    
    CORS(app, resources={r"/*": {"origins": cors_origins}})

    # Initialize rate limiter
    limiter.init_app(app)

    # Register blueprints
    from app.routes.auth_routes import auth_bp
    from app.routes.admin_routes import admin_bp
    from app.routes.prediction_routes import prediction_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(prediction_bp)

    # Ensure MongoDB indexes
    try:
        from app.utils.indexes import ensure_indexes
        ensure_indexes()
    except Exception as e:
        logger.warning(f"Index initialization failed: {e}")

    # Error handlers
    from app.utils.api_errors import ApiError, error_response

    @app.errorhandler(ApiError)
    def handle_api_error(err):
        payload, status = error_response(err.message, status_code=err.status_code, code=err.code, details=err.details)
        from flask import jsonify
        return jsonify(payload), status

    @app.errorhandler(404)
    def not_found(_):
        payload, status = error_response("Not found", status_code=404, code="not_found")
        from flask import jsonify
        return jsonify(payload), status

    @app.errorhandler(405)
    def method_not_allowed(_):
        payload, status = error_response("Method not allowed", status_code=405, code="method_not_allowed")
        from flask import jsonify
        return jsonify(payload), status

    @app.errorhandler(429)
    def too_many_requests(_):
        payload, status = error_response("Too many requests", status_code=429, code="rate_limited")
        from flask import jsonify
        return jsonify(payload), status

    @app.errorhandler(500)
    def internal_error(_):
        payload, status = error_response("An internal error occurred", status_code=500, code="internal_error")
        from flask import jsonify
        return jsonify(payload), status

    @app.route("/", methods=["GET"])
    def home():
        from flask import jsonify
        return jsonify({
            "message": "Smart Plant Health Monitoring API",
            "status": "running",
            "version": "1.0.0"
        }), 200

    return app
