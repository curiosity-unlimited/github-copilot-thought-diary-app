"""
Thought Diary routes for the Thought Diary application.

This module defines routes for creating, reading, updating, and deleting
thought diary entries, as well as analyzing sentiment in the entries.
"""
from datetime import datetime, timedelta
from flask import request, jsonify, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
from marshmallow import ValidationError
from sqlalchemy import func
from sqlalchemy.sql import text
from app.database.config import db
from app.models.thought_diary import ThoughtDiary
from app.models.user import User
from app.auth.utils import error_response, get_current_user
from app.schemas.diaries import (
    thought_diary_schema, thought_diaries_schema, 
    thought_diary_create_schema, thought_diary_update_schema,
    thought_diary_pagination_schema, thought_diary_stats_schema
)
from app.diaries import bp


@bp.route('/', methods=['GET'])
@jwt_required()
def get_thought_diaries():
    """Get all thought diaries for the current user with pagination.
    
    Query parameters:
        page (int): Page number, defaults to 1
        per_page (int): Items per page, defaults to 10
        
    Returns:
        200: List of thought diaries with pagination info
        401: Not authenticated
    """
    # Get current user
    current_user = get_current_user()
    if not current_user:
        return error_response("User not found", 404)
        
    # Parse pagination parameters
    try:
        page = int(request.args.get('page', 1))
        per_page = min(int(request.args.get('per_page', 10)), 50)  # Limit to 50 items max
    except ValueError:
        return error_response("Invalid pagination parameters", 400)
        
    # Query with pagination
    diary_query = ThoughtDiary.query.filter_by(user_id=current_user.id).order_by(ThoughtDiary.created_at.desc())
    pagination = diary_query.paginate(page=page, per_page=per_page)
    
    # Prepare response data
    response_data = {
        'items': pagination.items,
        'total': pagination.total,
        'page': pagination.page,
        'per_page': pagination.per_page,
        'total_pages': pagination.pages
    }
    
    return thought_diary_pagination_schema.dump(response_data)


@bp.route('/', methods=['POST'])
@jwt_required()
def create_thought_diary():
    """Create a new thought diary entry.
    
    Request body:
        {
            "content": "My thoughts for today..."
        }
        
    Returns:
        201: Newly created thought diary
        400: Invalid request data
        401: Not authenticated
    """
    try:
        # Get current user
        current_user = get_current_user()
        if not current_user:
            return error_response("User not found", 404)
            
        # Validate input data with schema
        data = thought_diary_create_schema.load(request.get_json() or {})
        
        # Create new thought diary entry
        thought_diary = ThoughtDiary(
            user_id=current_user.id,
            content=data['content']
        )
        
        # Save to database
        db.session.add(thought_diary)
        db.session.commit()
        
        # Analyze content for sentiment
        success, error_message = thought_diary.analyze_content()
        if success:
            db.session.commit()
        
        return thought_diary_schema.dump(thought_diary), 201
        
    except ValidationError as err:
        return error_response(err.messages, 400)


@bp.route('/<int:diary_id>', methods=['GET'])
@jwt_required()
def get_thought_diary(diary_id):
    """Get a specific thought diary entry.
    
    Args:
        diary_id (int): The ID of the thought diary entry
        
    Returns:
        200: The thought diary entry
        401: Not authenticated
        403: Not authorized to access this diary
        404: Diary not found
    """
    # Get current user
    current_user = get_current_user()
    if not current_user:
        return error_response("User not found", 404)
        
    # Find the diary entry
    thought_diary = ThoughtDiary.find_by_id(diary_id)
    if not thought_diary:
        return error_response("Thought diary not found", 404)
        
    # Check if user owns this diary entry
    if thought_diary.user_id != current_user.id:
        return error_response("Not authorized to access this diary", 403)
        
    return thought_diary_schema.dump(thought_diary)


@bp.route('/<int:diary_id>', methods=['PUT'])
@jwt_required()
def update_thought_diary(diary_id):
    """Update a specific thought diary entry.
    
    Args:
        diary_id (int): The ID of the thought diary entry
        
    Request body:
        {
            "content": "Updated thoughts for today..."
        }
        
    Returns:
        200: The updated thought diary entry
        400: Invalid request data
        401: Not authenticated
        403: Not authorized to access this diary
        404: Diary not found
    """
    try:
        # Get current user
        current_user = get_current_user()
        if not current_user:
            return error_response("User not found", 404)
            
        # Validate input data with schema
        data = thought_diary_update_schema.load(request.get_json() or {})
        
        # Find the diary entry
        thought_diary = ThoughtDiary.find_by_id(diary_id)
        if not thought_diary:
            return error_response("Thought diary not found", 404)
            
        # Check if user owns this diary entry
        if thought_diary.user_id != current_user.id:
            return error_response("Not authorized to update this diary", 403)
            
        # Update content
        thought_diary.content = data['content']
        
        # Re-analyze content for sentiment
        success, error_message = thought_diary.analyze_content()
        
        # Save to database
        db.session.commit()
        
        return thought_diary_schema.dump(thought_diary)
        
    except ValidationError as err:
        return error_response(err.messages, 400)


@bp.route('/<int:diary_id>', methods=['DELETE'])
@jwt_required()
def delete_thought_diary(diary_id):
    """Delete a specific thought diary entry.
    
    Args:
        diary_id (int): The ID of the thought diary entry
        
    Returns:
        200: Success message
        401: Not authenticated
        403: Not authorized to access this diary
        404: Diary not found
    """
    # Get current user
    current_user = get_current_user()
    if not current_user:
        return error_response("User not found", 404)
        
    # Find the diary entry
    thought_diary = ThoughtDiary.find_by_id(diary_id)
    if not thought_diary:
        return error_response("Thought diary not found", 404)
        
    # Check if user owns this diary entry
    if thought_diary.user_id != current_user.id:
        return error_response("Not authorized to delete this diary", 403)
        
    # Delete the entry
    db.session.delete(thought_diary)
    db.session.commit()
    
    return jsonify({'message': 'Thought diary deleted successfully'})


@bp.route('/stats', methods=['GET'])
@jwt_required()
def get_diary_stats():
    """Get statistics about the current user's thought diaries.
    
    Returns:
        200: Diary statistics
        401: Not authenticated
    """
    # Get current user
    current_user = get_current_user()
    if not current_user:
        return error_response("User not found", 404)
    
    # Calculate total entries
    total_entries = ThoughtDiary.query.filter_by(user_id=current_user.id).count()
    
    # Calculate entries this week
    one_week_ago = datetime.now() - timedelta(days=7)
    entries_this_week = ThoughtDiary.query.filter(
        ThoughtDiary.user_id == current_user.id,
        ThoughtDiary.created_at >= one_week_ago
    ).count()
    
    # Calculate entries this month
    one_month_ago = datetime.now() - timedelta(days=30)
    entries_this_month = ThoughtDiary.query.filter(
        ThoughtDiary.user_id == current_user.id,
        ThoughtDiary.created_at >= one_month_ago
    ).count()
    
    # Calculate average content length
    avg_query = db.session.query(func.avg(func.length(ThoughtDiary.content))).filter(
        ThoughtDiary.user_id == current_user.id
    ).scalar()
    average_length = int(avg_query) if avg_query else 0
    
    # Get the last entry date
    last_entry = ThoughtDiary.query.filter_by(user_id=current_user.id).order_by(ThoughtDiary.created_at.desc()).first()
    last_entry_date = last_entry.created_at if last_entry else None
    
    # Count positive and negative sentiments (simple heuristic based on HTML spans)
    sentiment_counts = {
        "positive": 0,
        "negative": 0,
        "neutral": 0
    }
    
    all_diaries = ThoughtDiary.query.filter_by(user_id=current_user.id).all()
    for diary in all_diaries:
        if diary.analyzed_content:
            positive_count = diary.analyzed_content.count('<span class="positive">')
            negative_count = diary.analyzed_content.count('<span class="negative">')
            
            if positive_count > negative_count:
                sentiment_counts["positive"] += 1
            elif negative_count > positive_count:
                sentiment_counts["negative"] += 1
            else:
                sentiment_counts["neutral"] += 1
        else:
            sentiment_counts["neutral"] += 1
    
    # Prepare stats response
    stats = {
        'total_entries': total_entries,
        'entries_this_week': entries_this_week,
        'entries_this_month': entries_this_month,
        'average_length': average_length,
        'sentiment_counts': sentiment_counts,
        'last_entry_date': last_entry_date
    }
    
    return thought_diary_stats_schema.dump(stats)