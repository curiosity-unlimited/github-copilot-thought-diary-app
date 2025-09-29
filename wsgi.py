"""
Main entry point for the Thought Diary Flask application.

This script serves as the entry point for running the Flask application.
It imports the application factory and creates an instance of the application.

Example usage:
    # Run in development mode with debug
    $ uv run flask --debug run
    
    # Initialize database
    $ uv run flask init-db
"""
import os
from app import create_app

app = create_app()

if __name__ == '__main__':
    # Only used for running the app directly, not for production
    app.run(debug=True)