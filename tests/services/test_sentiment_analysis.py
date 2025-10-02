"""
Tests for the sentiment analysis service.
"""
import pytest
from unittest.mock import patch, MagicMock
from app.services.sentiment_analysis import GitHubModelsService
from app.services.analyzer import SentimentAnalyzer


class TestGitHubModelsService:
    """Tests for the GitHubModelsService class."""
    
    def test_init_with_api_key(self):
        """Test initialization with API key."""
        service = GitHubModelsService(api_key="test_api_key")
        assert service.api_key == "test_api_key"
    
    @patch('os.getenv')
    def test_init_with_env_variable(self, mock_getenv):
        """Test initialization with environment variable."""
        def mock_getenv_side_effect(key, default=None):
            if key == "GITHUB_API_KEY":
                return "env_api_key"
            return default
        
        mock_getenv.side_effect = mock_getenv_side_effect
        service = GitHubModelsService()
        assert service.api_key == "env_api_key"
        mock_getenv.assert_any_call("GITHUB_API_KEY")
    
    def test_init_with_custom_model(self):
        """Test initialization with custom model."""
        service = GitHubModelsService(api_key="test_api_key", model="custom/model")
        assert service.model == "custom/model"
    
    @patch('os.getenv')
    def test_init_with_model_env_variable(self, mock_getenv):
        """Test initialization with model from environment variable."""
        def mock_getenv_side_effect(key, default=None):
            if key == "GITHUB_MODEL":
                return "env/model"
            return default
        
        mock_getenv.side_effect = mock_getenv_side_effect
        service = GitHubModelsService()
        assert service.model == "env/model"
    
    def test_init_with_custom_max_tokens(self):
        """Test initialization with custom max_tokens."""
        service = GitHubModelsService(api_key="test_api_key", max_tokens=500)
        assert service.max_tokens == 500
    
    @patch('os.getenv')
    def test_init_with_max_tokens_env_variable(self, mock_getenv):
        """Test initialization with max_tokens from environment variable."""
        def mock_getenv_side_effect(key, default=None):
            if key == "GITHUB_MAX_TOKENS":
                return "750"
            return default
        
        mock_getenv.side_effect = mock_getenv_side_effect
        service = GitHubModelsService()
        assert service.max_tokens == 750
    
    @patch('os.getenv')
    def test_init_with_invalid_max_tokens_env_variable(self, mock_getenv):
        """Test initialization with invalid max_tokens from environment variable."""
        def mock_getenv_side_effect(key, default=None):
            if key == "GITHUB_MAX_TOKENS":
                return "not-a-number"
            return default
        
        mock_getenv.side_effect = mock_getenv_side_effect
        service = GitHubModelsService()
        assert service.max_tokens == GitHubModelsService.DEFAULT_MAX_TOKENS
    
    def test_is_configured_with_key(self):
        """Test is_configured returns True when API key is set."""
        service = GitHubModelsService(api_key="test_api_key")
        assert service.is_configured() is True
    
    def test_is_configured_without_key(self):
        """Test is_configured returns False when API key is not set."""
        with patch('os.getenv', return_value=None):
            service = GitHubModelsService()
            assert service.is_configured() is False
    
    @patch('requests.post')
    def test_analyze_sentiment_success(self, mock_post):
        """Test successful sentiment analysis."""
        # Setup mock response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "choices": [
                {
                    "message": {
                        "content": "I felt both <span class=\"positive\">excitement</span> and <span class=\"negative\">anxious</span> after I got elected.",
                        "role": "assistant"
                    }
                }
            ]
        }
        mock_post.return_value = mock_response
        
        # Test the service with custom model and max_tokens
        service = GitHubModelsService(
            api_key="test_api_key",
            model="test/model-123",
            max_tokens=456
        )
        result, error = service.analyze_sentiment("I felt both excitement and anxious after I got elected.")
        
        # Verify results
        assert error is None
        assert "<span class=\"positive\">excitement</span>" in result
        assert "<span class=\"negative\">anxious</span>" in result
        
        # Verify API call
        mock_post.assert_called_once()
        args, kwargs = mock_post.call_args
        assert args[0] == GitHubModelsService.BASE_URL
        assert "Authorization" in kwargs["headers"]
        assert kwargs["headers"]["Authorization"] == "Bearer test_api_key"
        
        # Verify payload contains custom model and max_tokens
        payload = kwargs["json"]
        assert payload["model"] == "test/model-123"
        assert payload["max_tokens"] == 456
        assert payload["temperature"] == 0.3  # Should still use the fixed temperature
    
    @patch('requests.post')
    def test_analyze_sentiment_api_error(self, mock_post):
        """Test API error handling."""
        # Setup mock response
        mock_response = MagicMock()
        mock_response.status_code = 400
        mock_response.text = "Bad Request"
        mock_post.return_value = mock_response
        
        # Test the service
        service = GitHubModelsService(api_key="test_api_key")
        result, error = service.analyze_sentiment("Test text")
        
        # Verify results
        assert result is None
        assert error is not None
        assert "failed with status 400" in error
    
    @patch('os.getenv', return_value=None)  # Mock os.getenv to return None for all env vars
    def test_analyze_sentiment_no_api_key(self, mock_getenv):
        """Test sentiment analysis fails when no API key is provided."""
        # Create service with explicitly None API key and mock env vars
        service = GitHubModelsService(api_key=None)
        
        # Verify the API key is actually None
        assert service.api_key is None
        
        # Call the method
        result, error = service.analyze_sentiment("Test text")
        
        # Verify results
        assert result is None
        assert error == "GitHub API key is not configured"


class TestSentimentAnalyzer:
    """Tests for the SentimentAnalyzer class."""
    
    def test_singleton_pattern(self):
        """Test the singleton pattern of SentimentAnalyzer."""
        analyzer1 = SentimentAnalyzer.get_instance()
        analyzer2 = SentimentAnalyzer.get_instance()
        assert analyzer1 is analyzer2
    
    @patch('app.services.sentiment_analysis.GitHubModelsService.analyze_sentiment')
    def test_analyze_delegates_to_service(self, mock_analyze_sentiment):
        """Test that analyze method delegates to the service."""
        # Setup mock
        mock_analyze_sentiment.return_value = ("analyzed text", None)
        
        # Test analyzer
        analyzer = SentimentAnalyzer.get_instance()
        result, error = analyzer.analyze("Test text")
        
        # Verify results
        assert result == "analyzed text"
        assert error is None
        mock_analyze_sentiment.assert_called_once_with("Test text")
    
    @patch('app.services.sentiment_analysis.GitHubModelsService.is_configured')
    def test_is_available_delegates_to_service(self, mock_is_configured):
        """Test that is_available method delegates to the service."""
        # Setup mock
        mock_is_configured.return_value = True
        
        # Test analyzer
        analyzer = SentimentAnalyzer.get_instance()
        result = analyzer.is_available()
        
        # Verify results
        assert result is True
        mock_is_configured.assert_called_once()