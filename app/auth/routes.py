"""
Authentication routes for the Thought Diary application.

This module defines routes for user registration, login, logout,
token refresh, and user profile retrieval.
"""
from flask import request, jsonify, current_app
from flask_jwt_extended import (
    create_access_token, create_refresh_token, 
    jwt_required, get_jwt_identity, get_jwt
)
from marshmallow import ValidationError
from app.database.config import db
from app.models.user import User
from app.auth import bp
from app.auth.utils import add_token_to_blocklist, error_response, get_token_expiry, get_current_user
from app.schemas.auth import register_schema, login_schema, user_schema, token_schema
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

# Get the limiter instance
limiter = Limiter(
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"],
)

@bp.route('/register', methods=['POST'])
@limiter.limit("3 per hour")
def register():
    """Register a new user.
    
    Request body:
        {
            "email": "user@example.com",
            "password": "SecurePassword123!"
        }
        
    Returns:
        201: User created successfully
        400: Invalid request data
        409: User already exists
    """
    try:
        # Validate input data with schema
        data = register_schema.load(request.get_json() or {})
        
        # Create new user
        user = User(email=data['email'])
        user.set_password(data['password'])
        
        # Save to database
        db.session.add(user)
        db.session.commit()
        
        return jsonify({
            'message': 'User created successfully',
            'user': user_schema.dump(user)
        }), 201
        
    except ValidationError as err:
        return error_response(err.messages, 400)


@bp.route('/login', methods=['POST'])
@limiter.limit("5 per 15 minute")
def login():
    """Authenticate user and issue JWT tokens.
    
    Request body:
        {
            "email": "user@example.com",
            "password": "SecurePassword123!"
        }
        
    Returns:
        200: Authentication successful
        400: Invalid request data
        401: Authentication failed
    """
    try:
        # Validate input data with schema
        data = login_schema.load(request.get_json() or {})
        
        # Find user by email
        user = User.find_by_email(data['email'])
        
        # Check if user exists and password is correct
        if not user or not user.check_password(data['password']):
            return error_response("Invalid email or password", 401)
        
        # Get token expiration configuration
        access_expires_dict, refresh_expires_dict = get_token_expiry()
        
        # Generate tokens - convert ID to string to avoid "Subject must be a string" error
        access_token = create_access_token(identity=str(user.id))
        refresh_token = create_refresh_token(identity=str(user.id))
        
        # Prepare response
        response_data = {
            'access_token': access_token,
            'refresh_token': refresh_token,
            'user': user,
            'expires_in': int(access_expires_dict['access_expires'].total_seconds())
        }
        
        return token_schema.dump(response_data)
        
    except ValidationError as err:
        return error_response(err.messages, 400)


@bp.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
    """Refresh access token using a valid refresh token.
    
    Returns:
        200: New access token
        401: Invalid or expired refresh token
    """
    # Get user identity from refresh token
    current_user_id = get_jwt_identity()
    
    # Generate new access token - identity is already a string from login
    access_token = create_access_token(identity=current_user_id)
    access_expires_dict, _ = get_token_expiry()
    
    return jsonify({
        'access_token': access_token,
        'expires_in': int(access_expires_dict['access_expires'].total_seconds())
    })


@bp.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    """Invalidate the current JWT token.
    
    Returns:
        200: Logout successful
        401: Invalid or expired token
    """
    # Get JWT token details
    token = get_jwt()
    jti = token['jti']
    ttype = token['type']
    
    # Add token to blocklist
    add_token_to_blocklist(jti, ttype)
    
    return jsonify({'message': 'Successfully logged out'})


@bp.route('/me', methods=['GET'])
@jwt_required()
def get_user_profile():
    """Get the current user's profile information.
    
    Returns:
        200: User profile
        401: Not authenticated
        404: User not found
    """
    # Get current user from JWT identity
    user = get_current_user()
    
    if not user:
        return error_response("User not found", 404)
    
    return user_schema.dump(user)