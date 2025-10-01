"""
Authentication blueprint for the Thought Diary application.

This module defines the Flask blueprint for authentication-related routes
and functionality, including user registration, login, and token management.
"""
from flask import Blueprint

# Create blueprint for auth routes
bp = Blueprint('auth', __name__)

# Import routes at the end to avoid circular imports
from app.auth import routes