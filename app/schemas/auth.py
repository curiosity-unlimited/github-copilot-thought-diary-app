"""
Authentication schemas for the Thought Diary application.

This module defines schemas for validating and serializing
authentication-related data.
"""
from marshmallow import fields, validate, validates, ValidationError
from app.models.user import User
from app.schemas import ma


class UserSchema(ma.SQLAlchemySchema):
    """Schema for User model serialization."""
    
    class Meta:
        model = User
        # Only serialize these fields
        fields = ('id', 'email', 'created_at')
        
    id = ma.auto_field()
    email = ma.auto_field()
    created_at = ma.auto_field(dump_only=True)


class RegisterSchema(ma.Schema):
    """Schema for user registration validation."""
    
    email = fields.Email(required=True, validate=validate.Length(max=255))
    password = fields.Str(
        required=True, 
        validate=validate.Length(min=8, max=100),
        load_only=True  # password should never be sent back in responses
    )
    
    @validates('email')
    def validate_email(self, value, **kwargs):
        """Validate that the email is not already taken.
        
        Args:
            value (str): The email to validate
            **kwargs: Additional arguments passed by marshmallow
            
        Raises:
            ValidationError: If the email is already in use
        """
        user = User.find_by_email(value)
        if user:
            raise ValidationError('Email is already registered')
    
    @validates('password')
    def validate_password(self, value, **kwargs):
        """Validate password complexity requirements.
        
        Args:
            value (str): The password to validate
            **kwargs: Additional arguments passed by marshmallow
            
        Raises:
            ValidationError: If the password doesn't meet requirements
        """
        if not User.is_valid_password(value):
            raise ValidationError(
                'Password must contain at least one uppercase letter, '
                'one lowercase letter, one number, and one special character'
            )


class LoginSchema(ma.Schema):
    """Schema for login validation."""
    
    email = fields.Email(required=True)
    password = fields.Str(required=True, load_only=True)


class TokenResponseSchema(ma.Schema):
    """Schema for token response serialization."""
    
    access_token = fields.Str(dump_only=True)
    refresh_token = fields.Str(dump_only=True)
    expires_in = fields.Int(dump_only=True)
    user = fields.Nested(UserSchema, dump_only=True)


# Create schema instances for validation and serialization
user_schema = UserSchema()
users_schema = UserSchema(many=True)

register_schema = RegisterSchema()
login_schema = LoginSchema()
token_schema = TokenResponseSchema()