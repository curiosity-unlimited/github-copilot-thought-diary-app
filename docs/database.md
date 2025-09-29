# Database Documentation

This document describes the database models and structure used in the Thought Diary application.

## Overview

The application uses SQLAlchemy as an ORM (Object-Relational Mapper) to interact with the database. The database configuration supports both SQLite (for development) and PostgreSQL (for production) environments.

## Models

### User

The `User` model is responsible for user authentication and account management.

#### Fields

| Field Name     | Type         | Description                                   | Constraints          |
|----------------|--------------|-----------------------------------------------|----------------------|
| id             | Integer      | Primary key for user                         | Primary key, auto-increment |
| email          | String(255)  | User's email address                        | Unique, not null, indexed |
| password_hash  | String(255)  | Bcrypt hashed password                       | Not null             |
| created_at     | DateTime     | Timestamp when user was created              | Not null, default now |
| updated_at     | DateTime     | Timestamp when user was last updated         | Not null, default now, auto-update |

#### Methods

| Method Name      | Parameters           | Return Type | Description                                     |
|------------------|----------------------|-------------|-------------------------------------------------|
| set_password     | password (str)       | None        | Hashes and sets the user password               |
| check_password   | password (str)       | bool        | Verifies if password matches stored hash        |
| find_by_email    | email (str)          | User/None   | Class method to find a user by email            |
| is_valid_email   | email (str)          | bool        | Static method to validate email format          |
| is_valid_password| password (str)       | bool        | Static method to validate password strength     |

#### Password Requirements

Passwords must meet the following requirements:
- Minimum 8 characters
- At least one uppercase letter
- At least one lowercase letter
- At least one number
- At least one special character

## Database Configuration

The database configuration is handled in `app/database/config.py` and uses environment variables to determine which database to connect to.

### Environment Variables

| Variable    | Description                        | Example Value          |
|-------------|------------------------------------|------------------------|
| DB_USER     | PostgreSQL database user           | postgres               |
| DB_PASSWORD | PostgreSQL database password       | your_db_password_here  |
| DB_HOST     | PostgreSQL database host           | localhost              |
| DB_PORT     | PostgreSQL database port           | 5432                   |
| DB_NAME     | PostgreSQL database name           | thought_diary          |
| SQLITE_PATH | SQLite database file path          | thought_diary.db       |

### Connection Logic

The application uses the following logic to determine which database to connect to:
1. If all PostgreSQL environment variables are set (`DB_USER`, `DB_PASSWORD`, `DB_HOST`, `DB_PORT`, `DB_NAME`), it uses PostgreSQL.
2. Otherwise, it falls back to SQLite using the path specified in `SQLITE_PATH` (defaults to `thought_diary.db` if not set).