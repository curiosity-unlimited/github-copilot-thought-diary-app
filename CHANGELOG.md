# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.5.1] - 2025-10-02

### Changed
- Modified test database configuration to use a persistent database
- Fixed issue with data loss during test runs by maintaining test data between runs
- Added `clean-test-db` CLI command for optional test database cleanup
- Updated environment variables with `TEST_SQLITE_PATH` for configuring test database location
- Enhanced documentation with test database management instructions
- Improved test user fixture to reuse existing test users instead of recreating them

## [0.5.0] - 2025-10-02

### Added
- Implemented AI-powered sentiment analysis using GitHub Models inference API
- Created services package structure for extensible application services
- Added GitHubModelsService for interacting with GitHub Models API
- Created SentimentAnalyzer facade for easy integration with application components
- Updated environment configuration for GitHub API credentials
- Added sentiment analysis capability to mark positive/negative expressions in thought diaries
- Added comprehensive test suite for sentiment analysis services
- Created documentation for sentiment analysis features in docs/sentiment_analysis.md
- Added environment variable configuration options for GitHub Models inference:
  - `GITHUB_API_KEY` for interacting with GitHub Models API
  - `GITHUB_MODEL` for configuring the inference model
  - `GITHUB_MAX_TOKENS` for setting maximum response token length

## [0.4.2] - 2025-10-01

### Added
- Created comprehensive test suite for models, routes, and application
- Implemented tests for User model (creation, password hashing, validation)
- Implemented tests for ThoughtDiary model (CRUD operations, relationships)
- Updated pytest configuration for consistent test discovery and execution
- Added model-specific test modules in the tests/models directory

## [0.4.1] - 2025-10-01

### Added
- Created system blueprint for system endpoints
- Moved health and version endpoints from app factory to system blueprint
- Added API documentation endpoint at /docs with support for HTML and JSON formats
- Enhanced health endpoint to check database connection status

## [0.4.0] - 2025-10-01

### Added
- Implemented JWT authentication with Flask-JWT-Extended
- Created complete authentication system with register, login, logout, refresh token and profile endpoints
- Added rate limiting for public authentication endpoints
- Implemented token blocklisting for secure logout functionality
- Added environment variables for JWT configuration
- Added Flask-Marshmallow for request validation and serialization
- Created schemas for user authentication data validation and serialization
- Updated authentication endpoints to use marshmallow schemas

## [0.3.0] - 2025-09-29

### Added
- Created ThoughtDiary model with user relationship, content, analyzed_content, and timestamps
- Added bidirectional relationship between User and ThoughtDiary models
- Updated database configuration to register the new ThoughtDiary model
- Updated documentation in /docs to reflect the new ThoughtDiary model
- Updated README.md with ThoughtDiary model information

## [0.2.1] - 2025-09-29

### Fixed
- Fixed database URL selection logic to properly respect the ENV variable
- Added psycopg2-binary dependency for PostgreSQL support
- Updated documentation to reflect the correct database connection logic

## [0.2.0] - 2025-09-29

### Added
- Implemented Flask application factory pattern in app/__init__.py
- Added Flask CLI command for database initialization (init-db)
- Created WSGI entry point for the Flask application
- Updated main.py to provide command-line utilities
- Added application structure documentation

## [0.1.0] - 2025-09-29

### Added
- Created SQLAlchemy User model with email, password_hash, and timestamps
- Added comprehensive password validation and hashing using bcrypt
- Implemented email validation using email-validator
- Added database configuration with SQLite and PostgreSQL support
- Created basic application directory structure
- Updated dependencies in pyproject.toml to include Flask, SQLAlchemy, Flask-SQLAlchemy, Alembic, bcrypt, and email-validator
- Added environment variable configuration with .env.example template
- Created /docs directory with detailed documentation:
  - Added database.md with model specifications and database configuration details
  - Added index.md with project structure and documentation overview