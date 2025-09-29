"""
Thought Diary App main application package.

This module implements the Flask application factory pattern,
which allows for creating multiple instances of the application
with different configurations for various environments.
"""
import os
from flask import Flask
from app.database.config import init_db, db


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
    
    # Register CLI commands
    register_cli_commands(app)
    
    # Add basic routes
    @app.route('/health')
    def health_check():
        """Health check endpoint."""
        return {'status': 'healthy'}, 200
    
    @app.route('/version')
    def version():
        """Version information endpoint."""
        return {
            'version': '0.1.0',
            'environment': app.config.get('ENV')
        }, 200
    
    # Register blueprints here later
    # from app.auth import bp as auth_bp
    # app.register_blueprint(auth_bp, url_prefix='/auth')
    
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