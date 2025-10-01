"""
System blueprint for the Thought Diary application.

This module defines the Flask blueprint for system-related routes
and functionality, including health checks, version information,
and API documentation.
"""
from flask import Blueprint

# Create blueprint for system routes
bp = Blueprint('system', __name__)

# Import routes at the end to avoid circular imports
from app.system import routes