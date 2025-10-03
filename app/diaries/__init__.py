"""
Thought Diary blueprint initialization module.

This module initializes the Flask Blueprint for Thought Diary functionality.
"""
from flask import Blueprint

# Create blueprint
bp = Blueprint('diaries', __name__)

# Import routes to register them with the blueprint
from app.diaries import routes