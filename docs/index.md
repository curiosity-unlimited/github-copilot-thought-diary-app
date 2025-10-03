# Thought Diary App Documentation

Welcome to the Thought Diary App documentation. This documentation provides detailed information about the application's architecture, components, and usage.

## Table of Contents

1. [Application Structure](application.md)
   - Application Factory Pattern
   - Running the Application
   - Environment-Specific Configuration

2. [Database Documentation](database.md)
   - Models
   - Configuration
   - Environment Variables

3. [Authentication](authentication.md)
   - JWT Authentication
   - User Registration
   - Login and Token Management
   
4. [Thought Diary API](diaries.md)
   - Endpoints
   - Request/Response Formats
   - Authentication Requirements
   
5. [Sentiment Analysis](sentiment_analysis.md)
   - GitHub Models API Integration
   - Content Analysis
   - Displaying Analyzed Content
   
6. [Usage Guide](usage.md)
   - Initializing the Database
   - Running the Development Server
   - Production Deployment

## Project Structure

```
thought-diary-app/
├── app/                    # Main application package
│   ├── database/           # Database configuration and utilities
│   │   ├── __init__.py
│   │   └── config.py       # Database connection configuration
│   ├── models/             # Database models
│   │   ├── __init__.py
│   │   ├── user.py         # User model definition
│   │   └── thought_diary.py # ThoughtDiary model definition
│   └── __init__.py         # Application factory pattern implementation
├── docs/                   # Documentation files
│   ├── index.md            # This file
│   └── database.md         # Database documentation
├── .env                    # Environment variables (not in version control)
├── .env.example            # Example environment variables
├── main.py                 # CLI utility entry point
├── wsgi.py                 # WSGI entry point for Flask application
├── pyproject.toml          # Project metadata and dependencies
└── README.md               # Project overview and setup instructions
```

## Getting Started

Please refer to the [README.md](../README.md) file in the root directory for setup instructions.

## Environment Variables

The application uses environment variables for configuration. See the [.env.example](../.env.example) file for a list of required and optional environment variables.