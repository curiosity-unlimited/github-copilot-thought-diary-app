"""
Sentiment Analysis Integration Module

This module provides a simple interface for integrating sentiment analysis
capabilities into the application, abstracting the underlying service implementation.
"""
import logging
from typing import Optional, Tuple
from app.services.sentiment_analysis import GitHubModelsService

# Configure logger
logger = logging.getLogger(__name__)

class SentimentAnalyzer:
    """Sentiment analysis integration for the application.
    
    This class serves as a facade for sentiment analysis services,
    providing a simple interface for the rest of the application.
    """
    
    # Singleton instance
    _instance = None
    
    @classmethod
    def get_instance(cls) -> 'SentimentAnalyzer':
        """Get or create the singleton instance of SentimentAnalyzer.
        
        Returns:
            SentimentAnalyzer: The singleton instance
        """
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance
    
    def __init__(self):
        """Initialize the sentiment analyzer with the GitHub Models service."""
        self.service = GitHubModelsService()
        
    def analyze(self, text: str) -> Tuple[Optional[str], Optional[str]]:
        """Analyze the sentiment in the provided text.
        
        This method sends the text for sentiment analysis and returns
        the analyzed text with sentiment highlighting.
        
        Args:
            text (str): The text to analyze
            
        Returns:
            Tuple[Optional[str], Optional[str]]: A tuple containing:
                - The analyzed text with sentiment highlights (or None if failed)
                - Error message if any (or None if successful)
        """
        return self.service.analyze_sentiment(text)
    
    def is_available(self) -> bool:
        """Check if sentiment analysis service is available and configured.
        
        Returns:
            bool: True if the service is configured and available, False otherwise
        """
        return self.service.is_configured()