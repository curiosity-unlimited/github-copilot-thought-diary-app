"""
Authentication utility functions for the Thought Diary application.

This module provides utility functions for JWT token management,
token blocklisting, and authentication helper functions.
"""
from datetime import datetime, timezone, timedelta
from typing import Dict, Optional, Any, Tuple
from flask import current_app, jsonify
from flask_jwt_extended import get_jwt_identity

from app.models.user import User


def get_token_expiry() -> Tuple[Dict[str, timedelta], Dict[str, timedelta]]:
    """Get token expiration configuration.
    
    Returns:
        Tuple[Dict[str, timedelta], Dict[str, timedelta]]: Access token and refresh token expiry times
    """
    access_expires = timedelta(minutes=current_app.config.get('JWT_ACCESS_TOKEN_EXPIRES_MINUTES', 15))
    refresh_expires = timedelta(days=current_app.config.get('JWT_REFRESH_TOKEN_EXPIRES_DAYS', 30))
    
    return {
        "access_expires": access_expires,
    }, {
        "refresh_expires": refresh_expires
    }


def add_token_to_blocklist(jti: str, token_type: str) -> None:
    """Add a JWT token to the blocklist.
    
    Args:
        jti (str): JWT token identifier
        token_type (str): Token type ('access' or 'refresh')
    """
    # Get redis client from app config if configured for production
    redis_client = current_app.config.get('REDIS_CLIENT')
    
    # Get token expiration time
    access_expires_dict, refresh_expires_dict = get_token_expiry()
    
    # Set the appropriate expiration time based on token type
    if token_type == 'access':
        expires = access_expires_dict['access_expires']
    else:
        expires = refresh_expires_dict['refresh_expires']
    
    # If using Redis for production, store in Redis with expiration
    if redis_client:
        redis_client.set(f"blocklist:{jti}", "", ex=int(expires.total_seconds()))
    else:
        # For development/testing, use in-memory storage
        # This is a simple implementation for development only
        if 'token_blocklist' not in current_app.config:
            current_app.config['token_blocklist'] = {}
            
        # Store token with expiration time
        current_app.config['token_blocklist'][jti] = datetime.now(timezone.utc) + expires


def is_token_blocklisted(jti: str) -> bool:
    """Check if a token is in the blocklist.
    
    Args:
        jti (str): JWT token identifier
        
    Returns:
        bool: True if token is blocklisted, False otherwise
    """
    # Get redis client from app config if configured for production
    redis_client = current_app.config.get('REDIS_CLIENT')
    
    # If using Redis, check if token is in Redis
    if redis_client:
        return redis_client.exists(f"blocklist:{jti}")
    else:
        # For development/testing, check in-memory storage
        blocklist = current_app.config.get('token_blocklist', {})
        
        # Check if token is in blocklist and not expired
        if jti in blocklist:
            expiry = blocklist[jti]
            
            # Clean up expired tokens
            if expiry < datetime.now(timezone.utc):
                del blocklist[jti]
                return False
                
            return True
            
        return False


def get_current_user() -> Optional[User]:
    """Get the current user from JWT identity.
    
    Returns:
        Optional[User]: The current user if authenticated, None otherwise
    """
    user_id = get_jwt_identity()
    if user_id:
        # Convert user_id back to int since it's stored as a string in the JWT
        try:
            user_id_int = int(user_id)
            return User.query.get(user_id_int)
        except (ValueError, TypeError):
            # Handle case where user_id is not a valid integer
            return None
    return None


def error_response(message: str, code: int = 400) -> Tuple[Dict[str, Any], int]:
    """Generate a standard error response.
    
    Args:
        message (str): Error message
        code (int, optional): HTTP status code. Defaults to 400.
        
    Returns:
        Tuple[Dict[str, Any], int]: Error response and status code
    """
    return {"error": message}, code