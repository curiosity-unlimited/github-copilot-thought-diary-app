"""
Command-line interface for the Thought Diary application.

This module serves as a command-line entry point for various utility functions.
For running the Flask application, use the wsgi.py script or Flask CLI commands.
"""
import os
import sys
from dotenv import load_dotenv
from flask import Flask
from app import create_app

def main():
    """Main entry point for command-line utilities."""
    # Load environment variables from .env file
    load_dotenv()
    
    # Print application information
    print("Thought Diary Application CLI")
    print("-----------------------------")
    print(f"Environment: {os.getenv('ENV', 'development')}")
    
    # Example of creating an app instance
    app = create_app()
    print(f"Application created with Flask version: {Flask.__version__}")
    print("Use 'uv run flask --help' for available commands")
    print("To initialize the database: uv run flask init-db")
    print("To run the development server: uv run flask --debug run")


if __name__ == "__main__":
    main()
