"""
GitHub Models Sentiment Analysis Service

This module provides functionality to analyze sentiment in text using
GitHub Models inference API. It wraps the GitHub Models API to provide
sentiment analysis capabilities for the application.
"""
import os
import json
import logging
import requests
from typing import Optional, Dict, Any, Tuple

# Configure logger
logger = logging.getLogger(__name__)

class GitHubModelsService:
    """Service for interacting with GitHub Models API for sentiment analysis.
    
    This service handles communication with the GitHub Models inference API
    to analyze sentiment in text content from thought diaries.
    """
    # Base URL for GitHub Models API
    BASE_URL = "https://models.github.ai/inference/chat/completions"
    
    # Default model and parameters
    DEFAULT_MODEL = "openai/gpt-4o"
    DEFAULT_MAX_TOKENS = 1000
    
    def __init__(self, api_key: Optional[str] = None, model: Optional[str] = None, max_tokens: Optional[int] = None):
        """Initialize the GitHub Models service.
        
        Args:
            api_key (Optional[str]): GitHub API key with 'models: read' permission.
                If not provided, will attempt to read from environment variable.
            model (Optional[str]): The model ID to use for inference.
                If not provided, will attempt to read from environment variable or use default.
            max_tokens (Optional[int]): Maximum number of tokens for the response.
                If not provided, will attempt to read from environment variable or use default.
        """
        # Load API key from parameter or environment variable
        self.api_key = api_key or os.getenv("GITHUB_API_KEY")
        if not self.api_key:
            logger.warning(
                "GitHub API key not provided. Set GITHUB_API_KEY environment variable "
                "or pass api_key to GitHubModelsService constructor."
            )
        
        # Load model from parameter or environment variable or use default
        self.model = model or os.getenv("GITHUB_MODEL", self.DEFAULT_MODEL)
        
        # Load max_tokens from parameter or environment variable or use default
        max_tokens_env = os.getenv("GITHUB_MAX_TOKENS")
        if max_tokens is not None:
            self.max_tokens = max_tokens
        elif max_tokens_env is not None:
            try:
                self.max_tokens = int(max_tokens_env)
            except (ValueError, TypeError):
                logger.warning(f"Invalid max_tokens value in environment: {max_tokens_env}. Using default.")
                self.max_tokens = self.DEFAULT_MAX_TOKENS
        else:
            self.max_tokens = self.DEFAULT_MAX_TOKENS
        
        logger.info(f"GitHub Models Service initialized with model={self.model}, max_tokens={self.max_tokens}")
    
    def analyze_sentiment(self, text: str) -> Tuple[Optional[str], Optional[str]]:
        """Analyze sentiment in the provided text using GitHub Models.
        
        The function sends the text to GitHub Models inference API and processes
        the response to identify positive and negative sentiments, returning
        HTML-formatted text with sentiment highlighting.
        
        Args:
            text (str): The text content to analyze for sentiment.
            
        Returns:
            Tuple[Optional[str], Optional[str]]: A tuple containing:
                - HTML-formatted text with sentiment highlighting (or None if failed)
                - Error message if any (or None if successful)
        """
        # Check if API key is configured
        if not self.api_key or not self.api_key.strip():
            return None, "GitHub API key is not configured"
        
        # Check if text is provided
        if not text or not text.strip():
            return None, "Empty text provided for sentiment analysis"
        
        try:
            # Prepare headers for the GitHub Models API request
            headers = {
                "Accept": "application/vnd.github+json",
                "Authorization": f"Bearer {self.api_key}",
                "X-GitHub-Api-Version": "2022-11-28",
                "Content-Type": "application/json"
            }
            
            # Prepare the message for sentiment analysis
            # Using system message to instruct the model on the task
            messages = [
                {
                    "role": "system",
                    "content": (
                        "You are a sentiment analysis assistant. Analyze the user's text and "
                        "identify positive and negative emotions, thoughts, and feelings. "
                        "Wrap positive words/phrases with <span class=\"positive\">positive text</span> "
                        "and negative words/phrases with <span class=\"negative\">negative text</span>. "
                        "Only wrap the specific words/phrases, not entire sentences. "
                        "Return ONLY the wrapped text without any additional comments or analysis."
                    )
                },
                {
                    "role": "user",
                    "content": text
                }
            ]
            
            # Create the request payload using configured values
            payload = {
                "model": self.model,
                "messages": messages,
                "temperature": 0.3,  # Lower temperature for more predictable results
                "max_tokens": self.max_tokens,
            }
            
            # Make the request to GitHub Models API
            response = requests.post(
                self.BASE_URL,
                headers=headers,
                json=payload,
                timeout=10  # Timeout after 10 seconds
            )
            
            # Check for successful response
            if response.status_code == 200:
                # Extract the analyzed content from the response
                result = response.json()
                if "choices" in result and result["choices"] and "message" in result["choices"][0]:
                    analyzed_text = result["choices"][0]["message"]["content"]
                    return analyzed_text, None
                else:
                    logger.error(f"Unexpected response format: {result}")
                    return None, "Unexpected API response format"
            else:
                error_message = f"GitHub Models API request failed with status {response.status_code}: {response.text}"
                logger.error(error_message)
                return None, error_message
                
        except Exception as e:
            error_message = f"Error analyzing sentiment: {str(e)}"
            logger.exception(error_message)
            return None, error_message
    
    def is_configured(self) -> bool:
        """Check if the GitHub Models service is properly configured.
        
        Returns:
            bool: True if the API key is available, False otherwise.
        """
        return self.api_key is not None and len(self.api_key) > 0