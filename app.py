from flask import Flask, jsonify
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from app import db, create_app  # Import db and create_app from __init__.py
import logging
import os

# Configure Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create an application instance
app = create_app()

# Initialize rate limiter for all APIs
limiter = Limiter(get_remote_address, app=app, storage_uri="memory://")

# Global Error Handling
@app.errorhandler(429)  # Rate limit exceeded
def ratelimit_error(e):
    return jsonify({"error": "Rate limit exceeded. Try again later."}), 429

@app.errorhandler(400)
def bad_request_error(e):
    return jsonify({"error": "Bad request. Check your input."}), 400

@app.errorhandler(500)
def internal_server_error(e):
    return jsonify({"error": "Internal server error. Try again later."}), 500

if __name__ == "__main__":
    with app.app_context():
        # Create all database tables if they don't exist
        db.create_all()
    app.run(debug=True)
