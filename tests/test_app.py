"""
Tests for the Flask application factory and basic configuration.
"""
import pytest
from flask import Flask
from app import create_app


def test_create_app():
    """Test that the application factory creates a valid Flask application."""
    app = create_app()
    assert isinstance(app, Flask)
    # In our test environment, ENV might be 'testing' due to our fixture setup
    assert app.config['ENV'] in ['development', 'testing']
    

def test_create_app_test_config():
    """Test that the application factory accepts custom test configurations."""
    test_config = {'TESTING': True, 'SECRET_KEY': 'test-key'}
    app = create_app(test_config)
    assert app.config['TESTING']
    assert app.config['SECRET_KEY'] == 'test-key'


def test_app_context_exists(app):
    """Test that the application context exists."""
    assert app.config['TESTING']
    with app.app_context():
        assert True


def test_db_exists(app, db):
    """Test that the database is initialized in the app."""
    with app.app_context():
        from app.database.config import db as app_db
        from sqlalchemy import text
        assert app_db is not None
        # Test that we can execute a simple query
        assert db.session.execute(text('SELECT 1')).scalar() == 1


def test_jwt_manager_initialized(app):
    """Test that JWT manager is initialized in the app."""
    with app.app_context():
        assert app.config['JWT_SECRET_KEY'] is not None
        assert app.config['JWT_BLOCKLIST_ENABLED']