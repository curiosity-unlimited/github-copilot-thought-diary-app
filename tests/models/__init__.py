"""
Tests for the User model.
"""
import pytest
from app.models.user import User


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


def test_email_validation():
    """Test email validation method."""
    # Valid emails
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
    
    assert str(user) == '<User id=1 email=repr@example.com>'
    assert repr(user) == '<User id=1 email=repr@example.com>'