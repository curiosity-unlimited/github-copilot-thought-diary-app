"""
Pytest configuration and fixtures for the Thought Diary application tests.
"""
import os
import tempfile
import pytest
from flask import Flask
from flask.testing import FlaskClient
from app import create_app
from app.database.config import db as _db
from app.models.user import User


@pytest.fixture(scope='session')
def app():
    """Create a Flask app configured for testing.
    
    Returns:
        Flask: The configured Flask application instance.
    """
    # Use a persistent test database path
    test_db_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 
                               "instance", "test_database.db")
    
    # Set the environment variable for test DB
    os.environ["TEST_SQLITE_PATH"] = test_db_path
    os.environ["ENV"] = "testing"
    
    # Configure the app for testing
    app = create_app({
        'TESTING': True,
        'DEBUG': False,
        'JWT_SECRET_KEY': 'test-jwt-secret-key',
        'SECRET_KEY': 'test-secret-key',
        'ENV': 'testing',
        'WTF_CSRF_ENABLED': False,
        'SERVER_NAME': 'localhost.localdomain',
    })
    
    # Create the database and the tables
    with app.app_context():
        _db.create_all()
        
    yield app
    
    # Don't delete the test database to preserve data between test runs


@pytest.fixture(scope='function')
def db(app):
    """Get a database session for testing.
    
    Args:
        app (Flask): The Flask application fixture.
        
    Returns:
        SQLAlchemy: The database session.
    """
    with app.app_context():
        # Make sure all tables exist but don't drop them
        _db.create_all()
        
    yield _db
    
    # Just clean the session, but don't drop tables to preserve data
    with app.app_context():
        _db.session.remove()
        # Rolling back any uncommitted changes to keep the database clean
        _db.session.rollback()


@pytest.fixture(scope='function')
def client(app):
    """Get a test client for the Flask application.
    
    Args:
        app (Flask): The Flask application fixture.
        
    Returns:
        FlaskClient: The test client for making requests.
    """
    return app.test_client()


@pytest.fixture(scope='function')
def test_user(db):
    """Create a test user in the database or use existing one.
    
    Args:
        db (SQLAlchemy): The database session fixture.
        
    Returns:
        User: The created or existing test user.
    """
    # Check if the test user already exists
    from app.models.user import User
    
    with db.session.begin():
        user = User.query.filter_by(email='test@example.com').first()
        
        # Create the user only if they don't exist
        if user is None:
            user = User(email='test@example.com')
            user.set_password('Test123!')
            db.session.add(user)
    
    return user


@pytest.fixture(scope='function')
def auth_headers(app, client, test_user):
    """Get authentication headers with a valid token.
    
    Args:
        app (Flask): The Flask application fixture.
        client (FlaskClient): The test client fixture.
        test_user (User): The test user fixture.
        
    Returns:
        dict: Headers dictionary with Authorization header.
    """
    response = client.post('/auth/login', json={
        'email': 'test@example.com',
        'password': 'Test123!'
    })
    
    access_token = response.json.get('access_token')
    
    return {'Authorization': f'Bearer {access_token}'}