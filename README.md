# Thought Diary App
- A full-stack web application powered by AI that allows users to write [Thought Diaries](https://positivepsychology.com/thought-diary/), which help identify & challenge negative thinking patterns, promoting healthier mental habits.
- A demo app from the course - GitHub Copilot

## Prerequisites
- [Git](https://git-scm.com/downloads) for version control
- [uv](https://docs.astral.sh/uv/getting-started/installation/) for Python project management
- [Bruno](https://github.com/usebruno/bruno) for API client
- [SQLite](https://sqlite.org/) for development database
- [PostgreSQL](https://www.postgresql.org/) optional, for production database
- [Redis](https://redis.io/) optional, for production rate limiting persistence

## Project Architecture
A modern, comprehensive full-stack travel planning platform with a robust Flask API backend and a modern Vue 3 frontend as well as clear separation between frontend and backend.

### Backend Technologies (`./`)
- **Runtime**: Python 3.11+ with Flask framework
- **Database**: SQLAlchemy ORM with SQLite (development) / PostgreSQL (production)
- **Testing**: Pytest with 80%+ coverage requirement
- **Documentation**: Type hints (PEP 484), comprehensive docstrings

### Frontend Technologies
TODO

## Features

### Authentication
- Users can register, log in, and log out securely.

### Thought Diary Management
- Users can add a thought diary at the top of the page after logging in.
- Thought diaries are added as plain text only.
- All thought diaries are listed in descending date order with pagination.
- Users can edit and delete thought diaries from the list.

### AI-Powered Sentiment Analysis
- The app leverages [model inference from GitHub Models](https://docs.github.com/en/rest/models/inference?apiVersion=2022-11-28) to analyze thought diaries.
- Words and phrases are marked for positive/negative thinking and feelings with green/red background colors.
    - For example, when a user adds or edits a thought diary:
        ```text
        I felt both excitement and anxious after I got elected to join a team for international math competition.
        ```
    - The backend sends the text to GitHub for model inference and receives HTML-labeled text:
        ```html
        I felt both <span class="positive">excitement</span> and <span class="negative">anxious</span> after I got elected to join a team for international math competition.
        ```
    - The backend saves the labeled text in the database.
    - The frontend retrieves and displays the text using CSS:
        ```css
        span.positive {
            background-color: green;
            color: white; /* Optional: Change text color for better contrast */
        }
        span.negative {
            background-color: red;
            color: white; /* Optional: Change text color for better contrast */
        }
        ```

### User Experience
TODO

### Authentication & Security
- **JWT Authentication**: Secure token-based authentication with refresh mechanism
- **Enterprise Security**: Redis rate limiting, HTTPS enforcement, security headers, custom middleware
- **Password Security**: Bcrypt hashing with salt and comprehensive validation
- **Input Validation**: Client and server-side validation with sanitization
- **Protected Routes**: Frontend route guards with backend JWT verification
- **CORS Configuration**: Controlled cross-origin resource sharing for secure API access

### Environment-Specific Deployment

**Development:**
- Backend: Flask development server with debug mode
- Frontend: TODO
- Database: SQLite for simplicity
- Security: Relaxed for development ease

**Production:**
- Backend: Gunicorn with multiple workers, PostgreSQL, Redis
- Frontend: TODO
- Database: PostgreSQL with connection pooling
- Security: Enforce all security features like Redis rate limiting, HTTPS enforcement, security headers, CORS, etc.

### Environment-Specific Settings

- **Development**: Debug enabled, auto-generated keys, CORS relaxed
- **Testing**: Rate limiting disabled, optimized for testing, mock data
- **Production**: HTTPS enforced, security headers, Redis required

### API Endpoints

#### Authentication Endpoints
- `POST /auth/register` - Register new user (rate limited: 3/hour)
- `POST /auth/login` - User login, returns JWT token
- `POST /auth/refresh` - Refresh JWT token
- `POST /auth/logout` - Invalidate current token
- `GET /auth/me` - Get current user profile information

#### Thought Diaries Endpoints
- `GET /diaries` - List all thought diaries with pagination (protected)
- `POST /diaries` - Create a new thought diary (protected)
- `GET /diaries/{id}` - Get a specific thought diary (protected)
- `PUT /diaries/{id}` - Update a specific thought diary (protected)
- `DELETE /diaries/{id}` - Delete a specific thought diary (protected)
- `GET /diaries/stats` - Get statistics about user's thought diaries (protected)

#### System Endpoints
- `GET /health` - Health check endpoint
- `GET /version` - API version information
- `GET /docs` - API documentation

## Setup
1. Fork the repository: 
- Please follow [GitHub Docs](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/working-with-forks/fork-a-repo) to fork the repository to your GitHub account.
- **IMPORTANT: Please uncheck the "Copy the DEFAULT branch only" option when forking in order to copy all branches into the new fork.**
2. Clone the repository from your GitHub account:
- Please replace `<your-github-username>` with your GitHub account username in the command below:
    ```
    git clone https://github.com/<your-github-username>/github-copilot-thought-diary-app.git
    cd github-copilot-thought-diary-app
    ```

3. Fetch all the branches:
    ```
    git fetch --all
    ```

4. List all the branches and make sure `advanced-workflow-start`, `advanced-workflow-end`, `master-workflow-start`, and `master-workflow-end` are in the list:
    ```
    git branch -a
    ```

5. Switch to the `advanced-workflow-start` branch:
    ```
    git checkout advanced-workflow-start
    ```

6. Run the following command in the Copilot Chat window with `agent` mode and an advanced model like `Claude-Sonnet-4` to set up the Python environment:
    ```
    /init-python-project-with-uv
    ```

## License

[MIT](LICENSE)
