# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

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