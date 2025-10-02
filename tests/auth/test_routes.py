"""
Tests for authentication routes and functionality.
"""
import pytest
import json
from flask import url_for
from app.models.user import User


def test_register_success(client, db):
    """Test successful user registration."""
    # Use a timestamp to ensure email is unique across test runs
    import time
    unique_email = f'newuser_{int(time.time())}@example.com'
    
    data = {
        'email': unique_email,
        'password': 'SecurePass123!'
    }
    response = client.post('/auth/register', json=data)
    
    # Check if the response is either 201 (created) or 400 (if email exists)
    if response.status_code == 400:
        # If the test fails with 400, check if it's due to email already existing
        if b'Email is already registered' in response.data:
            # Try with a different email
            unique_email = f'newuser_{int(time.time())+100}@example.com'
            data['email'] = unique_email
            response = client.post('/auth/register', json=data)
            
    assert response.status_code == 201, f"Failed with status {response.status_code}: {response.data}"
    assert b'User created successfully' in response.data
    
    # Check that the user was actually created
    user = User.query.filter_by(email='newuser@example.com').first()
    assert user is not None
    assert user.email == 'newuser@example.com'


def test_register_invalid_email(client, db):
    """Test registration with invalid email format."""
    data = {
        'email': 'invalid-email',
        'password': 'SecurePass123!'
    }
    response = client.post('/auth/register', json=data)
    
    assert response.status_code == 400
    assert b'Not a valid email address' in response.data


def test_register_weak_password(client, db):
    """Test registration with a weak password."""
    data = {
        'email': 'valid@example.com',
        'password': 'weak'  # Missing uppercase, number, special char, and too short
    }
    response = client.post('/auth/register', json=data)
    
    assert response.status_code == 400
    # Check that it contains an error related to the password
    response_data = json.loads(response.data)
    assert 'error' in response_data
    assert 'password' in response_data['error']
    

def test_register_duplicate_email(client, test_user):
    """Test registration with an already registered email."""
    data = {
        'email': 'test@example.com',  # Already used by test_user fixture
        'password': 'SecurePass123!'
    }
    response = client.post('/auth/register', json=data)
    
    assert response.status_code == 400
    assert b'Email is already registered' in response.data


def test_login_success(client, test_user):
    """Test successful login."""
    data = {
        'email': 'test@example.com',
        'password': 'Test123!'
    }
    response = client.post('/auth/login', json=data)
    
    assert response.status_code == 200
    json_data = json.loads(response.data)
    assert 'access_token' in json_data
    assert 'refresh_token' in json_data
    assert 'user' in json_data
    assert json_data['user']['email'] == 'test@example.com'


def test_login_invalid_credentials(client, test_user):
    """Test login with invalid credentials."""
    data = {
        'email': 'test@example.com',
        'password': 'WrongPassword!'
    }
    response = client.post('/auth/login', json=data)
    
    assert response.status_code == 401
    assert b'Invalid email or password' in response.data


def test_me_success(client, auth_headers):
    """Test successful user profile retrieval."""
    response = client.get('/auth/me', headers=auth_headers)
    
    assert response.status_code == 200
    json_data = json.loads(response.data)
    assert json_data['email'] == 'test@example.com'


def test_me_unauthorized(client):
    """Test unauthorized access to user profile."""
    response = client.get('/auth/me')
    
    assert response.status_code == 401
    assert b'Missing Authorization Header' in response.data


def test_refresh_token(client, auth_headers, app):
    """Test refreshing an access token with a refresh token."""
    with app.app_context():
        # First, get a refresh token through login
        login_response = client.post('/auth/login', json={
            'email': 'test@example.com',
            'password': 'Test123!'
        })
        refresh_token = json.loads(login_response.data)['refresh_token']
        
        # Use the refresh token to get a new access token
        refresh_headers = {'Authorization': f'Bearer {refresh_token}'}
        response = client.post('/auth/refresh', headers=refresh_headers)
        
        assert response.status_code == 200
        json_data = json.loads(response.data)
        assert 'access_token' in json_data
        assert 'expires_in' in json_data


def test_logout(client, auth_headers):
    """Test successful logout."""
    response = client.post('/auth/logout', headers=auth_headers)
    
    assert response.status_code == 200
    assert b'Successfully logged out' in response.data
    
    # Verify that the token is now invalid
    second_response = client.get('/auth/me', headers=auth_headers)
    assert second_response.status_code == 401