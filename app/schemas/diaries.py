"""
Thought Diary schemas for the Thought Diary application.

This module defines schemas for validating and serializing
Thought Diary-related data.
"""
from marshmallow import fields, validate, validates, ValidationError
from app.models.thought_diary import ThoughtDiary
from app.schemas import ma


class ThoughtDiarySchema(ma.SQLAlchemySchema):
    """Schema for ThoughtDiary model serialization."""
    
    class Meta:
        model = ThoughtDiary
        # Fields to serialize
        fields = ('id', 'user_id', 'content', 'analyzed_content', 'created_at', 'updated_at')
        
    id = ma.auto_field(dump_only=True)
    user_id = ma.auto_field(dump_only=True)
    content = ma.auto_field()
    analyzed_content = ma.auto_field(dump_only=True)
    created_at = ma.auto_field(dump_only=True)
    updated_at = ma.auto_field(dump_only=True)


class ThoughtDiaryCreateSchema(ma.Schema):
    """Schema for thought diary creation validation."""
    
    content = fields.Str(required=True, validate=validate.Length(min=1, max=10000))
    
    @validates('content')
    def validate_content(self, value, **kwargs):
        """Validate that the content is not empty.
        
        Args:
            value (str): The content to validate
            **kwargs: Additional arguments passed by marshmallow
            
        Raises:
            ValidationError: If the content is empty
        """
        if not value.strip():
            raise ValidationError('Content cannot be empty')


class ThoughtDiaryUpdateSchema(ThoughtDiaryCreateSchema):
    """Schema for thought diary update validation."""
    pass


class ThoughtDiaryPaginationSchema(ma.Schema):
    """Schema for paginated thought diary responses."""
    
    items = fields.Nested(ThoughtDiarySchema, many=True)
    total = fields.Int(dump_only=True)
    page = fields.Int(dump_only=True)
    per_page = fields.Int(dump_only=True)
    total_pages = fields.Int(dump_only=True)


class ThoughtDiaryStatsSchema(ma.Schema):
    """Schema for thought diary statistics."""
    
    total_entries = fields.Int(dump_only=True)
    entries_this_week = fields.Int(dump_only=True)
    entries_this_month = fields.Int(dump_only=True)
    average_length = fields.Int(dump_only=True)
    sentiment_counts = fields.Dict(keys=fields.Str(), values=fields.Int(), dump_only=True)
    last_entry_date = fields.DateTime(dump_only=True)


# Create schema instances for validation and serialization
thought_diary_schema = ThoughtDiarySchema()
thought_diaries_schema = ThoughtDiarySchema(many=True)
thought_diary_create_schema = ThoughtDiaryCreateSchema()
thought_diary_update_schema = ThoughtDiaryUpdateSchema()
thought_diary_pagination_schema = ThoughtDiaryPaginationSchema()
thought_diary_stats_schema = ThoughtDiaryStatsSchema()