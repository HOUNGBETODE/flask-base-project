import os
from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from commons.config.config.config import Config
from controllers.swagger.swagger import setup_swagger
from core.scheduler.scheduler_init import initialize_scheduler
from commons.config.errors.errors import register_error_handlers
from core.blueprint.blueprint import initialize_blueprint_route


def create_app():
    """
    Create and configure the Flask application.

    This function initializes the Flask app, loads the configuration,
    sets up extensions like CORS, JWTManager, and Swagger, and registers
    error handlers and blueprints.
    
    Returns:
        Flask: The configured Flask application instance.
    """

    instance_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../../instance'))
    app = Flask(__name__, template_folder='../../templates', static_folder='../../static', instance_path=instance_path)

    # Log application startup for debugging purposes
    app.logger.info("Flask application started successfully.")
    
    # Load configuration from the Config object
    app.config.from_object(Config)
    
    # Ensure the upload folder exists
    os.makedirs(Config.UPLOAD_FOLDER, exist_ok=True)
    os.makedirs(Config.UPLOAD_USER_AVATAR, exist_ok=True)
    os.makedirs(Config.UPLOAD_ATTACHMENT, exist_ok=True)
    os.makedirs(Config.DELETED_ATTACHMENTS, exist_ok=True)

    # Initialize extensions and middleware
    
    # Configure Swagger documentation
    setup_swagger(app)

    # Configure Cross-Origin Resource Sharing (CORS) policy
    CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True, allow_headers=["Authorization", "Content-Type"])
    
    # Register custom error handlers
    register_error_handlers(app)
    
    # Initialize and register application blueprints
    initialize_blueprint_route(app)
    # initialize_scheduler(app)

    # Configure JWT (JSON Web Token) Manager
    jwt = JWTManager(app)

    return app
