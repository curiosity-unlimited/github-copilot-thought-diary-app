"""
Tests for the User model.
"""
import pytest
from datetime import datetime
from app.models.user import User
from email_validator import EmailNotValidError


def test_user_creation(db):
    """Test creating a user instance."""
    user = User(email='user@example.com')
    user.set_password('SecurePass123!')
    
    db.session.add(user)
    db.session.commit()
    
    retrieved_user = User.query.filter_by(email='user@example.com').first()
    assert retrieved_user is not None
    assert retrieved_user.email == 'user@example.com'
    assert retrieved_user.password_hash is not None
    assert retrieved_user.created_at is not None
    assert retrieved_user.updated_at is not None


def test_password_hashing(db):
    """Test password hashing and verification."""
    user = User(email='password@example.com')
    user.set_password('SecurePass123!')
    
    # Test that passwords are hashed and not stored in plain text
    assert user.password_hash != 'SecurePass123!'
    
    # Test password verification
    assert user.check_password('SecurePass123!')
    assert not user.check_password('WrongPassword!')


def test_email_validation(monkeypatch):
    """Test email validation method."""
    # Mock the validate_email function to simulate success for valid emails and throw exception for invalid emails
    def mock_validate_email(email):
        valid_emails = ['user@example.com', 'user.name@example.co.uk', 'user+tag@example.org']
        if email in valid_emails:
            return {'email': email}
        else:
            raise EmailNotValidError("Invalid email")
    
    # Import the module to patch
    import app.models.user
    
    # Apply the monkeypatch
    monkeypatch.setattr(app.models.user, 'validate_email', mock_validate_email)
    
    # Now test with our mocked function
    assert User.is_valid_email('user@example.com')
    assert User.is_valid_email('user.name@example.co.uk')
    assert User.is_valid_email('user+tag@example.org')
    
    # Invalid emails
    assert not User.is_valid_email('user@')
    assert not User.is_valid_email('@example.com')
    assert not User.is_valid_email('user@example')
    assert not User.is_valid_email('user.example.com')


def test_password_validation():
    """Test password validation method."""
    # Valid passwords - must contain uppercase, lowercase, number, special char, and be 8+ chars
    assert User.is_valid_password('SecurePass123!')
    assert User.is_valid_password('Abcd1234#')
    assert User.is_valid_password('P@ssw0rd')
    
    # Invalid passwords
    assert not User.is_valid_password('short1')  # Too short
    assert not User.is_valid_password('lowercase123!')  # No uppercase
    assert not User.is_valid_password('UPPERCASE123!')  # No lowercase
    assert not User.is_valid_password('SecurePassword')  # No number
    assert not User.is_valid_password('SecurePass123')  # No special char


def test_find_by_email(db):
    """Test finding a user by email."""
    user = User(email='find@example.com')
    user.set_password('SecurePass123!')
    
    db.session.add(user)
    db.session.commit()
    
    # Test finding an existing user
    found_user = User.find_by_email('find@example.com')
    assert found_user is not None
    assert found_user.email == 'find@example.com'
    
    # Test finding a non-existent user
    not_found = User.find_by_email('nonexistent@example.com')
    assert not_found is None


def test_user_representation():
    """Test the string representation of a User."""
    user = User(id=1, email='repr@example.com')
    
    # This test might need to be adjusted based on your actual __repr__ method
    assert 'User' in repr(user)
    assert 'repr@example.com' in repr(user)


def test_user_created_at_defaults_to_current_time(db):
    """Test that created_at defaults to the current time."""
    user = User(email='timestamp@example.com')
    user.set_password('SecurePass123!')
    
    db.session.add(user)
    db.session.commit()
    
    # Check that timestamps exist
    assert user.created_at is not None
    assert user.updated_at is not None
    
    # updated_at should match created_at initially
    assert user.updated_at == user.created_at