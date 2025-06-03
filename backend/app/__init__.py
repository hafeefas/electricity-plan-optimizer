from flask import Flask
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def create_app():
    app = Flask(__name__)
    
    # Register blueprints
    from .api.routes import main_bp
    from .api.xml_routes import xml_bp
    
    app.register_blueprint(main_bp)
    app.register_blueprint(xml_bp)
    
    # Log registered routes
    logger.info("\nRegistered routes:")
    for rule in app.url_map.iter_rules():
        logger.info(f"{rule.endpoint}: {rule.rule}")
    
    return app 