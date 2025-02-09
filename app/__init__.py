# app/__init__.py

import logging
from flask import Flask
from config import Config

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    logging.info("Config loaded. DB_FILE: %s", app.config.get("DB_FILE"))
    
    from app import routes
    app.register_blueprint(routes.bp)
    
    logging.info("Blueprints registered. Application is ready.")
    return app
