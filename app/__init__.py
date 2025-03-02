from flask import Flask
from celery import Celery
from flask_sqlalchemy import SQLAlchemy
import os

# Initialize Flask extensions
db = SQLAlchemy()

def create_app(config_class=None):
    app = Flask(__name__)
    
    # Load configuration
    if config_class:
        app.config.from_object(config_class)
    
    # Database configuration
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URL", "postgresql://postgres:root@localhost/cv_db")
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  
    
    
    # Initialize extensions with the app
    db.init_app(app)  
    
    with app.app_context():       
        
        # Import and register blueprints - import here to avoid circular imports
        from app.routes.upload import upload_bp
        app.register_blueprint(upload_bp, url_prefix="/api")

        
        ## Initialize rate limiter if needed
        #from app.routes.upload import init_limiter
        #init_limiter(app)
    
    # Ensure the upload directory exists
    os.makedirs(os.path.join(os.getcwd(), "uploads"), exist_ok=True)
    
    return app
