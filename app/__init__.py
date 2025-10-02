"""
Thought Diary App main application package.

This module implements the Flask application factory pattern,
which allows for creating multiple instances of the application
with different configurations for various environments.
"""
import os
from datetime import timedelta
from flask import Flask
from flask_jwt_extended import JWTManager
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from app.database.config import init_db, db
from app.schemas import init_ma

# Ensure environment variables are loaded
from dotenv import load_dotenv
load_dotenv()


def create_app(test_config=None):
    """Create and configure the Flask application instance.
    
    Args:
        test_config (dict, optional): Test configuration to override default settings.
            Defaults to None.
    
    Returns:
        Flask: The configured Flask application instance.
    """
    # Create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    
    # Set default configuration
    app.config.from_mapping(
        SECRET_KEY=os.getenv('SECRET_KEY', 'development-key'),
        ENV=os.getenv('ENV', 'development'),
        # JWT Configuration
        JWT_SECRET_KEY=os.getenv('JWT_SECRET_KEY', 'jwt-secret-key-for-development'),
        JWT_ACCESS_TOKEN_EXPIRES_MINUTES=int(os.getenv('JWT_ACCESS_TOKEN_EXPIRES_MINUTES', 15)),
        JWT_REFRESH_TOKEN_EXPIRES_DAYS=int(os.getenv('JWT_REFRESH_TOKEN_EXPIRES_DAYS', 30)),
        JWT_BLOCKLIST_ENABLED=True,
    )
    
    # Override with test config if passed in
    if test_config is not None:
        app.config.update(test_config)
    
    # Ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        # Already exists
        pass
    
    # Initialize database with the app
    init_db(app)
    
    # Initialize Marshmallow
    init_ma(app)
    
    # Initialize JWT manager
    jwt = JWTManager(app)
    
    # Initialize rate limiter
    limiter = Limiter(
        key_func=get_remote_address,
        default_limits=["200 per day", "50 per hour"],
        storage_uri=os.getenv('REDIS_URL') if app.config.get('ENV') == 'production' else "memory://",
    )
    limiter.init_app(app)
    
    # Configure JWT token blocklist
    @jwt.token_in_blocklist_loader
    def check_if_token_is_revoked(jwt_header, jwt_payload):
        from app.auth.utils import is_token_blocklisted
        jti = jwt_payload["jti"]
        return is_token_blocklisted(jti)
    
    # Register CLI commands
    register_cli_commands(app)
    
    # Register blueprints
    from app.auth import bp as auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')
    
    from app.system import bp as system_bp
    app.register_blueprint(system_bp)
    
    return app


def register_cli_commands(app):
    """Register CLI commands with the Flask application.
    
    Args:
        app (Flask): The Flask application instance.
    """
    @app.cli.command('init-db')
    def init_db_command():
        """Initialize the database by creating all tables."""
        with app.app_context():
            db.create_all()
            print('Database tables created successfully!')
            
    @app.cli.command('clean-test-db')
    def clean_test_db_command():
        """Clean the test database by dropping and recreating all tables."""
        if app.config.get('ENV') == 'testing':
            with app.app_context():
                db.drop_all()
                db.create_all()
                print('Test database has been cleaned successfully!')
        else:
            print('This command can only be run in the testing environment.')