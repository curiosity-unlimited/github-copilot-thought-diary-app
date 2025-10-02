"""
Tests for the ThoughtDiary model's sentiment analysis integration.
"""
import pytest
from unittest.mock import patch, MagicMock
from app.models.thought_diary import ThoughtDiary
from app.models.user import User


class TestThoughtDiaryAnalyzeContent:
    """Tests for ThoughtDiary analyze_content method."""
    
    @patch('app.services.analyzer.SentimentAnalyzer.get_instance')
    def test_analyze_content_success(self, mock_get_instance, db):
        """Test successful sentiment analysis of thought diary content."""
        # Setup mock for sentiment analyzer
        mock_analyzer = MagicMock()
        mock_analyzer.is_available.return_value = True
        mock_analyzer.analyze.return_value = (
            'I felt both <span class="positive">excitement</span> and <span class="negative">anxious</span> after I got elected.',
            None
        )
        mock_get_instance.return_value = mock_analyzer
        
        # Create a user with unique email
        import time
        unique_email = f'analyzer_test_{int(time.time())}@example.com'
        
        # Check if a user with this email already exists
        existing_user = User.query.filter_by(email=unique_email).first()
        if existing_user:
            # Use the existing user
            user = existing_user
        else:
            # Create a new user
            user = User(email=unique_email)
            user.set_password('SecurePass123!')
            db.session.add(user)
            db.session.commit()
        
        diary = ThoughtDiary(
            user_id=user.id,
            content='I felt both excitement and anxious after I got elected.'
        )
        db.session.add(diary)
        db.session.commit()
        
        # Analyze content
        success, error = diary.analyze_content()
        
        # Verify results
        assert success is True
        assert error is None
        assert diary.analyzed_content is not None
        assert '<span class="positive">excitement</span>' in diary.analyzed_content
        assert '<span class="negative">anxious</span>' in diary.analyzed_content
        
        # Verify mock calls
        mock_analyzer.is_available.assert_called_once()
        mock_analyzer.analyze.assert_called_once_with('I felt both excitement and anxious after I got elected.')
    
    @patch('app.services.analyzer.SentimentAnalyzer.get_instance')
    def test_analyze_content_service_unavailable(self, mock_get_instance, db):
        """Test handling of unavailable sentiment analysis service."""
        # Setup mock for sentiment analyzer
        mock_analyzer = MagicMock()
        mock_analyzer.is_available.return_value = False
        mock_get_instance.return_value = mock_analyzer
        
        # Create a user with unique email
        import time
        unique_email = f'unavailable_{int(time.time())}@example.com'
        
        # Check if a user with this email already exists
        existing_user = User.query.filter_by(email=unique_email).first()
        if existing_user:
            # Use the existing user
            user = existing_user
        else:
            # Create a new user
            user = User(email=unique_email)
            user.set_password('SecurePass123!')
            db.session.add(user)
            db.session.commit()
        
        diary = ThoughtDiary(
            user_id=user.id,
            content='Test content'
        )
        db.session.add(diary)
        db.session.commit()
        
        # Analyze content
        success, error = diary.analyze_content()
        
        # Verify results
        assert success is False
        assert error == "Sentiment analysis service is not available"
        assert diary.analyzed_content is None
    
    @patch('app.services.analyzer.SentimentAnalyzer.get_instance')
    def test_analyze_content_analysis_error(self, mock_get_instance, db):
        """Test handling of sentiment analysis errors."""
        # Setup mock for sentiment analyzer
        mock_analyzer = MagicMock()
        mock_analyzer.is_available.return_value = True
        mock_analyzer.analyze.return_value = (None, "API Error")
        mock_get_instance.return_value = mock_analyzer
        
        # Create a user with unique email
        import time
        unique_email = f'analysis_error_{int(time.time())}@example.com'
        
        # Check if a user with this email already exists
        existing_user = User.query.filter_by(email=unique_email).first()
        if existing_user:
            # Use the existing user
            user = existing_user
        else:
            # Create a new user
            user = User(email=unique_email)
            user.set_password('SecurePass123!')
            db.session.add(user)
            db.session.commit()
        
        diary = ThoughtDiary(
            user_id=user.id,
            content='Test content'
        )
        db.session.add(diary)
        db.session.commit()
        
        # Analyze content
        success, error = diary.analyze_content()
        
        # Verify results
        assert success is False
        assert error == "API Error"
        assert diary.analyzed_content is None
    
    @patch('app.services.analyzer.SentimentAnalyzer.get_instance')
    def test_analyze_content_empty_content(self, mock_get_instance, db):
        """Test handling of empty content for sentiment analysis."""
        # Setup mock for sentiment analyzer
        mock_analyzer = MagicMock()
        mock_get_instance.return_value = mock_analyzer
        
        # Create a user with unique email
        import time
        unique_email = f'empty_content_{int(time.time())}@example.com'
        
        # Check if a user with this email already exists
        existing_user = User.query.filter_by(email=unique_email).first()
        if existing_user:
            # Use the existing user
            user = existing_user
        else:
            # Create a new user
            user = User(email=unique_email)
            user.set_password('SecurePass123!')
            db.session.add(user)
            db.session.commit()
        
        diary = ThoughtDiary(
            user_id=user.id,
            content=''
        )
        db.session.add(diary)
        db.session.commit()
        
        # Analyze content
        success, error = diary.analyze_content()
        
        # Verify results
        assert success is False
        assert error == "No content to analyze"
        assert diary.analyzed_content is None
        
        # Verify mock not called
        mock_analyzer.analyze.assert_not_called()