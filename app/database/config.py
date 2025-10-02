"""
Database configuration and setup for the Thought Diary application.
"""
import os
from typing import Optional
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    """Base class for all models."""
    pass


db = SQLAlchemy(model_class=Base)


def init_db(app) -> None:
    """Initialize the database with the Flask application.
    
    Args:
        app: The Flask application
    """
    # Configure SQLAlchemy
    database_url = get_database_url()
    app.config["SQLALCHEMY_DATABASE_URI"] = database_url
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    
    # Initialize the database with the app
    db.init_app(app)
    
    # Import models to ensure they are registered with SQLAlchemy
    from app.models.user import User  # noqa
    from app.models.thought_diary import ThoughtDiary  # noqa


def get_database_url() -> str:
    """Get database URL from environment or use default SQLite URL.
    
    Returns:
        The database URL string
    """
    # Check environment setting first
    env = os.getenv("ENV", "development").lower()
    
    # Use SQLite for development environments
    if env == "development":
        db_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 
                              "instance", os.getenv("SQLITE_PATH", "thought_diary.db"))
        return f"sqlite:///{db_path}"
    
    # For testing environment, use a separate database to not interfere with production data
    if env == "testing":
        test_db_path = os.getenv("TEST_SQLITE_PATH")
        if test_db_path:
            return f"sqlite:///{test_db_path}"
        else:
            # Use memory database for testing if no test DB path is provided
            return "sqlite:///instance/testing.db"
    
    # For production, use PostgreSQL if configured
    db_user: Optional[str] = os.getenv("DB_USER")
    db_password: Optional[str] = os.getenv("DB_PASSWORD")
    db_host: Optional[str] = os.getenv("DB_HOST")
    db_port: Optional[str] = os.getenv("DB_PORT")
    db_name: Optional[str] = os.getenv("DB_NAME", "thought_diary")
    
    # If PostgreSQL environment variables are set, use PostgreSQL
    if all([db_user, db_password, db_host, db_port, db_name]):
        return f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
    
    # Fall back to SQLite if PostgreSQL is not configured
    db_path = os.getenv("SQLITE_PATH", "thought_diary.db")
    return f"sqlite:///{db_path}"