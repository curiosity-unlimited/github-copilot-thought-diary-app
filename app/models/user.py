"""
User model definition for the Thought Diary application.
"""
from datetime import datetime
from typing import Optional
import bcrypt
import re
from sqlalchemy import String, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column
from email_validator import validate_email, EmailNotValidError

from app.database.config import db


class User(db.Model):
    """User model for authentication and authorization.
    
    Attributes:
        id (int): Unique identifier for the user
        email (str): User's email address, used for login
        password_hash (str): Bcrypt hashed password
        created_at (datetime): Timestamp when user was created
        updated_at (datetime): Timestamp when user was last updated
    """
    __tablename__ = 'users'
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False, index=True)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False
    )
    
    def __repr__(self) -> str:
        """Provide a string representation of the User model.
        
        Returns:
            str: String representation of the User model
        """
        return f"<User id={self.id} email={self.email}>"
    
    @staticmethod
    def is_valid_email(email: str) -> bool:
        """Check if the email is valid.
        
        Args:
            email (str): The email to validate
            
        Returns:
            bool: True if the email is valid, False otherwise
        """
        try:
            validate_email(email)
            return True
        except EmailNotValidError:
            return False
    
    @staticmethod
    def is_valid_password(password: str) -> bool:
        """Check if the password meets the requirements.
        
        Password requirements:
        - At least 8 characters long
        - Contains at least one uppercase letter
        - Contains at least one lowercase letter
        - Contains at least one number
        - Contains at least one special character
        
        Args:
            password (str): The password to validate
            
        Returns:
            bool: True if the password meets the requirements, False otherwise
        """
        if len(password) < 8:
            return False
            
        patterns = [
            r'[A-Z]',  # At least one uppercase letter
            r'[a-z]',  # At least one lowercase letter
            r'\d',     # At least one number
            r'[^A-Za-z0-9]'  # At least one special character
        ]
        
        return all(bool(re.search(pattern, password)) for pattern in patterns)
    
    def set_password(self, password: str) -> None:
        """Hash and set the user password.
        
        Args:
            password (str): The password to hash and set
        """
        password_bytes = password.encode('utf-8')
        salt = bcrypt.gensalt()
        self.password_hash = bcrypt.hashpw(password_bytes, salt).decode('utf-8')
    
    def check_password(self, password: str) -> bool:
        """Verify if the provided password matches the stored hash.
        
        Args:
            password (str): The password to check
            
        Returns:
            bool: True if the password matches, False otherwise
        """
        password_bytes = password.encode('utf-8')
        hash_bytes = self.password_hash.encode('utf-8')
        return bcrypt.checkpw(password_bytes, hash_bytes)
    
    @classmethod
    def find_by_email(cls, email: str) -> Optional['User']:
        """Find a user by email.
        
        Args:
            email (str): The email to search for
            
        Returns:
            Optional[User]: The user if found, None otherwise
        """
        return cls.query.filter_by(email=email).first()