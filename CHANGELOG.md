# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

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