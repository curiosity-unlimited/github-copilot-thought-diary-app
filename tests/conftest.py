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
    # Create a temporary file to use as a test database
    db_fd, db_path = tempfile.mkstemp()
    
    # Configure the app for testing
    app = create_app({
        'TESTING': True,
        'DEBUG': False,
        'SQLALCHEMY_DATABASE_URI': f'sqlite:///{db_path}',
        'SQLALCHEMY_TRACK_MODIFICATIONS': False,
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
    
    # Cleanup: close and remove the temporary database
    os.close(db_fd)
    os.unlink(db_path)


@pytest.fixture(scope='function')
def db(app):
    """Get a database session for testing.
    
    Args:
        app (Flask): The Flask application fixture.
        
    Returns:
        SQLAlchemy: The database session.
    """
    with app.app_context():
        _db.create_all()
        
    yield _db
    
    # Teardown - clean up after the test
    with app.app_context():
        _db.session.remove()
        _db.drop_all()


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
    """Create a test user in the database.
    
    Args:
        db (SQLAlchemy): The database session fixture.
        
    Returns:
        User: The created test user.
    """
    with db.session.begin():
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