"""
Schema initialization for the Thought Diary application.

This module initializes the Marshmallow instance and provides
a base schema for other schemas to inherit from.
"""
from flask_marshmallow import Marshmallow

# Initialize Marshmallow
ma = Marshmallow()

def init_ma(app):
    """Initialize Marshmallow with the Flask application.
    
    Args:
        app (Flask): The Flask application instance.
    """
    ma.init_app(app)