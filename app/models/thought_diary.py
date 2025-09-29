"""
ThoughtDiary model definition for the Thought Diary application.
"""
from datetime import datetime
from typing import Optional
from sqlalchemy import String, Text, DateTime, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.config import db
from app.models.user import User


class ThoughtDiary(db.Model):
    """ThoughtDiary model for storing user thoughts and their analysis.
    
    Attributes:
        id (int): Unique identifier for the thought diary entry
        user_id (int): Foreign key to the User who created this entry
        content (str): The original content of the thought diary entry
        analyzed_content (str): The analyzed/processed content (sentiment analysis, etc.)
        created_at (datetime): Timestamp when the entry was created
        updated_at (datetime): Timestamp when the entry was last updated
    """
    __tablename__ = 'thought_diaries'
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False, index=True)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    analyzed_content: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
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
    
    # Define relationship with User model
    user = relationship("User", back_populates="thought_diaries")
    
    def __repr__(self) -> str:
        """Provide a string representation of the ThoughtDiary model.
        
        Returns:
            str: String representation of the ThoughtDiary model
        """
        return f"<ThoughtDiary id={self.id} user_id={self.user_id}>"
    
    @classmethod
    def find_by_user_id(cls, user_id: int, limit: int = 10, offset: int = 0) -> list["ThoughtDiary"]:
        """Find thought diary entries by user_id with pagination.
        
        Args:
            user_id (int): The user ID to search for
            limit (int): Maximum number of entries to return
            offset (int): Number of entries to skip
            
        Returns:
            list[ThoughtDiary]: List of thought diary entries
        """
        return cls.query.filter_by(user_id=user_id).order_by(cls.created_at.desc()).limit(limit).offset(offset).all()
    
    @classmethod
    def find_by_id(cls, id: int) -> Optional["ThoughtDiary"]:
        """Find a thought diary entry by ID.
        
        Args:
            id (int): The entry ID to search for
            
        Returns:
            Optional[ThoughtDiary]: The entry if found, None otherwise
        """
        return cls.query.get(id)