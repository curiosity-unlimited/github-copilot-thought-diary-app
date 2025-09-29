# Application Structure Documentation

This document describes the application structure and Flask configuration for the Thought Diary application.

## Application Factory Pattern

The Thought Diary application uses the Flask application factory pattern, which allows creating multiple instances of the application with different configurations. This is particularly useful for testing and deploying to different environments.

The application factory is implemented in the [`app/__init__.py`](../app/__init__.py) file.

### Key Components

1. **create_app Function**: The main application factory function that creates and configures a Flask application instance.

   ```python
   def create_app(test_config=None):
       # Create and configure the app
       app = Flask(__name__, instance_relative_config=True)
       
       # Configuration and setup...
       
       return app
   ```

2. **Configuration**: The application loads configuration from environment variables and can be overridden with test-specific configuration.

3. **Database Initialization**: The factory initializes the database connection using the `init_db` function from `app.database.config`.

4. **CLI Commands**: Custom Flask CLI commands are registered, including the `init-db` command for database initialization.

## Running the Application

The application can be run in several ways:

1. **Using Flask's CLI**:
   ```bash
   uv run flask --debug run
   ```

2. **Using the WSGI entry point**:
   ```bash
   uv run python wsgi.py
   ```

## Database Initialization

To initialize the database using the Flask CLI command:

```bash
uv run flask init-db
```

This command will create all tables defined in the SQLAlchemy models.

## Environment-Specific Configuration

The application supports different configurations based on the `ENV` environment variable:

- **development**: Debug mode enabled, SQLite database
- **testing**: For running tests with an isolated database
- **production**: Production settings with PostgreSQL database

Set the `ENV` variable in your `.env` file to switch between environments.