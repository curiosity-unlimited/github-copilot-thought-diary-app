"""
Example usage of the sentiment analysis service.

This module provides a simple example of how to use the sentiment analysis service
in a route handler. This is for demonstration purposes only and should be adapted
to fit into the actual API endpoints for thought diaries.
"""
from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models.thought_diary import ThoughtDiary
from app.models.user import User
from app.services.analyzer import SentimentAnalyzer
from app.database.config import db

# Example blueprint (not to be used directly in the application)
example_bp = Blueprint('examples', __name__, url_prefix='/examples')


@example_bp.route('/analyze-sentiment', methods=['POST'])
@jwt_required()
def analyze_sentiment_example():
    """Example route that demonstrates sentiment analysis.
    
    This is a demonstration endpoint showing how to use the sentiment analyzer
    with a thought diary entry.
    
    Request Body:
        {
            "content": "Text content to analyze"
        }
    
    Returns:
        JSON response with original and analyzed content
    """
    data = request.get_json()
    
    # Input validation
    if not data or 'content' not in data:
        return jsonify({"error": "Content is required"}), 400
    
    content = data['content']
    if not content or not content.strip():
        return jsonify({"error": "Content cannot be empty"}), 400
    
    # Get current user
    current_user_id = get_jwt_identity()
    user = db.session.get(User, current_user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404
    
    # Create a new thought diary entry
    diary = ThoughtDiary(
        user_id=current_user_id,
        content=content
    )
    
    # Analyze content
    analyzer_available = SentimentAnalyzer.get_instance().is_available()
    if not analyzer_available:
        return jsonify({
            "warning": "Sentiment analysis is not available",
            "diary": {
                "content": content,
                "analyzed_content": None
            }
        }), 200
    
    # Perform analysis
    success, error = diary.analyze_content()
    if not success:
        return jsonify({
            "warning": f"Sentiment analysis failed: {error}",
            "diary": {
                "content": content,
                "analyzed_content": None
            }
        }), 200
    
    # Save to database (in a real implementation)
    # db.session.add(diary)
    # db.session.commit()
    
    # Return the analyzed content
    return jsonify({
        "message": "Sentiment analysis completed successfully",
        "diary": {
            "content": diary.content,
            "analyzed_content": diary.analyzed_content
        }
    }), 200


# Note: This is just an example and should not be registered with the app
# def register_example_blueprint(app):
#     app.register_blueprint(example_bp)