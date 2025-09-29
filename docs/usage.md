# Flask Application Usage Guide

This guide explains how to initialize the database and run the Flask application.

## Prerequisites

Ensure you have set up your environment variables properly. At minimum, your `.env` file should have:

```
SECRET_KEY=your_secret_key_here
ENV=development
SQLITE_PATH=thought_diary.db
```

## Initialize the Database

The application uses a Flask CLI command to initialize the database. Run:

```bash
uv run flask init-db
```

This command will:
1. Create all tables defined in your SQLAlchemy models
2. Set up the database using the configuration from your environment variables
3. Confirm with a success message when complete

## Run the Development Server

To run the Flask development server:

```bash
uv run flask --debug run
```

This starts the development server with:
- Debug mode enabled (auto-reload on code changes)
- Interactive debugger for exceptions
- Default port 5000 (access at http://localhost:5000)

## Available Endpoints

Currently, the application has two basic endpoints:

- `/health` - Health check endpoint that returns a status message
- `/version` - Version information endpoint

## Using the Main CLI

You can also run the main.py script to view application information:

```bash
uv run python main.py
```

This will display information about your environment and available commands.

## Production Deployment

For production deployment, you should:
1. Set ENV=production in your .env file
2. Configure PostgreSQL connection details
3. Use a WSGI server like Gunicorn to run the application

Example with Gunicorn:
```bash
uv add gunicorn
uv run gunicorn wsgi:app
```