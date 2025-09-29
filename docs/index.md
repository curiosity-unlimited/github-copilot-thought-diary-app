# Thought Diary App Documentation

Welcome to the Thought Diary App documentation. This documentation provides detailed information about the application's architecture, components, and usage.

## Table of Contents

1. [Database Documentation](database.md)
   - Models
   - Configuration
   - Environment Variables

## Project Structure

```
thought-diary-app/
├── app/                    # Main application package
│   ├── database/           # Database configuration and utilities
│   │   ├── __init__.py
│   │   └── config.py       # Database connection configuration
│   ├── models/             # Database models
│   │   ├── __init__.py
│   │   └── user.py         # User model definition
│   └── __init__.py
├── docs/                   # Documentation files
│   ├── index.md            # This file
│   └── database.md         # Database documentation
├── .env                    # Environment variables (not in version control)
├── .env.example            # Example environment variables
├── main.py                 # Application entry point
├── pyproject.toml          # Project metadata and dependencies
└── README.md               # Project overview and setup instructions
```

## Getting Started

Please refer to the [README.md](../README.md) file in the root directory for setup instructions.

## Environment Variables

The application uses environment variables for configuration. See the [.env.example](../.env.example) file for a list of required and optional environment variables.