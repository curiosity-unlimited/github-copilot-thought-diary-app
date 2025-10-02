"""
Integration tests for the sentiment analysis service.

These tests demonstrate how to test the sentiment analysis service integration
with the Flask application.
"""
import pytest
from unittest.mock import patch, MagicMock
from flask import url_for
from app.services.analyzer import SentimentAnalyzer
from app.models.user import User
from app.models.thought_diary import ThoughtDiary


@pytest.fixture(scope='session')
def sentiment_app():
    """Create a completely fresh Flask app with the example blueprint registered.
    
    By creating a new app instance specifically for these tests, we ensure
    that the blueprint is registered before any requests are handled.
    """
    # Create a test app
    import os
    import tempfile
    from app import create_app
    from app.database.config import db as _db
    
    # Create a temporary file to use as a test database
    db_fd, db_path = tempfile.mkstemp()
    
    # Configure the app for testing
    app = create_app({
        'TESTING': True,
        'DEBUG': False,
        'SQLALCHEMY_DATABASE_URI': f'sqlite:///{db_path}',
        'SQLALCHEMY_TRACK_MODIFICATIONS': False,
        'JWT_SECRET_KEY': 'test-jwt-secret-key',
        'SECRET_KEY': 'test-secret-key',
        'ENV': 'testing',
        'WTF_CSRF_ENABLED': False,
        'SERVER_NAME': 'localhost.localdomain',
    })
    
    # Register the example blueprint
    from app.services.examples import example_bp
    app.register_blueprint(example_bp)
    
    # Create the database and the tables
    with app.app_context():
        _db.create_all()
        
    yield app
    
    # Cleanup: close and remove the temporary database
    os.close(db_fd)
    os.unlink(db_path)


@pytest.fixture
def sentiment_db(sentiment_app):
    """Get a database session for testing with the sentiment app."""
    from app.database.config import db as _db
    
    with sentiment_app.app_context():
        _db.session.begin_nested()
        yield _db
        _db.session.rollback()
        _db.session.remove()


@pytest.fixture
def sentiment_client(sentiment_app):
    """Create a test client for the sentiment app."""
    return sentiment_app.test_client()


@pytest.fixture
def authenticated_client(sentiment_app, sentiment_client, sentiment_db, request):
    """Create an authenticated client for testing.
    
    Uses the test name to create a unique email for each test to avoid unique constraint violations.
    """
    import uuid
    from app.models.user import User
    
    # Create a unique email for this test
    unique_id = str(uuid.uuid4())[:8]
    test_email = f'sentiment_test_{unique_id}@example.com'
    
    # Create a test user
    user = User(email=test_email)
    user.set_password('SecurePass123!')
    sentiment_db.session.add(user)
    sentiment_db.session.commit()
    
    # Login to get an access token
    response = sentiment_client.post('/auth/login', json={
        'email': test_email,
        'password': 'SecurePass123!'
    })
    access_token = response.json['access_token']
    
    # Configure client with the token
    sentiment_client.environ_base['HTTP_AUTHORIZATION'] = f'Bearer {access_token}'
    return sentiment_client
    """Create an authenticated client for testing."""



class TestSentimentAnalysisIntegration:
    """Integration tests for sentiment analysis service."""
    
    @patch('app.services.analyzer.SentimentAnalyzer.get_instance')
    def test_analyze_sentiment_endpoint(self, mock_get_instance, authenticated_client):
        """Test the sentiment analysis example endpoint."""
        # Setup mock analyzer
        mock_analyzer = MagicMock()
        mock_analyzer.is_available.return_value = True
        
        # Setup mock for sentiment analyzer analyze method
        mock_analyzer.analyze.return_value = (
            'I felt both <span class="positive">excitement</span> and <span class="negative">anxious</span> after I got elected.',
            None
        )
        mock_get_instance.return_value = mock_analyzer
        
        # Make the API call
        response = authenticated_client.post('/examples/analyze-sentiment', json={
            'content': 'I felt both excitement and anxious after I got elected.'
        })
        
        # Check response
        assert response.status_code == 200
        data = response.json
        assert 'message' in data
        assert 'diary' in data
        assert data['diary']['content'] == 'I felt both excitement and anxious after I got elected.'
        assert '<span class="positive">excitement</span>' in data['diary']['analyzed_content']
        assert '<span class="negative">anxious</span>' in data['diary']['analyzed_content']
        
    @patch('app.services.analyzer.SentimentAnalyzer.get_instance')
    def test_analyze_sentiment_service_unavailable(self, mock_get_instance, authenticated_client):
        """Test handling of unavailable sentiment analysis service."""
        # Setup mock analyzer
        mock_analyzer = MagicMock()
        mock_analyzer.is_available.return_value = False
        mock_get_instance.return_value = mock_analyzer
        
        # Make the API call
        response = authenticated_client.post('/examples/analyze-sentiment', json={
            'content': 'Test content'
        })
        
        # Check response
        assert response.status_code == 200
        data = response.json
        assert 'warning' in data
        assert 'Sentiment analysis is not available' in data['warning']