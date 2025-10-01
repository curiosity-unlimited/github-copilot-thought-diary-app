"""
System routes for the Thought Diary application.

This module defines routes for system functionality, including
health checks, version information, and API documentation.
"""
from flask import jsonify, current_app, render_template, Response, url_for, request
import os
import json
from pathlib import Path
from app.system import bp


@bp.route('/health')
def health_check():
    """Health check endpoint.
    
    Returns:
        dict: Status information indicating system health
        int: HTTP status code 200
    """
    # Check database connection
    db_status = "connected"
    try:
        from app.database.config import db
        with current_app.app_context():
            # Execute a simple query to check connection
            db.session.execute('SELECT 1').scalar()
    except Exception as e:
        db_status = f"disconnected ({str(e)})"
    
    return jsonify({
        'status': 'healthy',
        'database': db_status,
        'environment': current_app.config.get('ENV')
    }), 200


@bp.route('/version')
def version():
    """Version information endpoint.
    
    Returns:
        dict: Version information including application version and environment
        int: HTTP status code 200
    """
    # Get application version from pyproject.toml if available
    app_version = '0.1.0'  # Default fallback version
    
    try:
        # Try to read version from pyproject.toml
        import tomli
        pyproject_path = Path(current_app.root_path).parent / 'pyproject.toml'
        if pyproject_path.exists():
            with open(pyproject_path, 'rb') as f:
                pyproject_data = tomli.load(f)
                app_version = pyproject_data.get('project', {}).get('version', app_version)
    except (ImportError, Exception):
        # Fallback to default version if any issues occur
        pass
    
    return jsonify({
        'version': app_version,
        'environment': current_app.config.get('ENV')
    }), 200


@bp.route('/docs')
def api_documentation():
    """API documentation endpoint.
    
    Returns:
        Response: HTML or JSON documentation of the API
        int: HTTP status code 200
    """
    # Generate list of all API endpoints
    endpoints = []
    
    # Add system endpoints
    endpoints.append({
        'group': 'System',
        'endpoints': [
            {
                'path': '/health',
                'method': 'GET',
                'description': 'Health check endpoint',
                'auth_required': False
            },
            {
                'path': '/version',
                'method': 'GET',
                'description': 'API version information',
                'auth_required': False
            },
            {
                'path': '/docs',
                'method': 'GET',
                'description': 'API documentation',
                'auth_required': False
            }
        ]
    })
    
    # Add auth endpoints
    endpoints.append({
        'group': 'Authentication',
        'endpoints': [
            {
                'path': '/auth/register',
                'method': 'POST',
                'description': 'Register new user',
                'auth_required': False,
                'rate_limit': '3 per hour'
            },
            {
                'path': '/auth/login',
                'method': 'POST',
                'description': 'User login, returns JWT token',
                'auth_required': False,
                'rate_limit': '5 per 15 minute'
            },
            {
                'path': '/auth/refresh',
                'method': 'POST',
                'description': 'Refresh JWT token',
                'auth_required': True,
                'note': 'Requires refresh token'
            },
            {
                'path': '/auth/logout',
                'method': 'POST',
                'description': 'Invalidate current token',
                'auth_required': True
            },
            {
                'path': '/auth/me',
                'method': 'GET',
                'description': 'Get current user profile information',
                'auth_required': True
            }
        ]
    })
    
    # Add thought diaries endpoints (placeholder for future implementation)
    endpoints.append({
        'group': 'Thought Diaries',
        'endpoints': [
            {
                'path': '/diaries',
                'method': 'GET',
                'description': 'List all thought diaries with pagination',
                'auth_required': True
            },
            {
                'path': '/diaries',
                'method': 'POST',
                'description': 'Create a new thought diary',
                'auth_required': True
            },
            {
                'path': '/diaries/{id}',
                'method': 'GET',
                'description': 'Get a specific thought diary',
                'auth_required': True
            },
            {
                'path': '/diaries/{id}',
                'method': 'PUT',
                'description': 'Update a specific thought diary',
                'auth_required': True
            },
            {
                'path': '/diaries/{id}',
                'method': 'DELETE',
                'description': 'Delete a specific thought diary',
                'auth_required': True
            },
            {
                'path': '/diaries/stats',
                'method': 'GET',
                'description': 'Get statistics about user\'s thought diaries',
                'auth_required': True
            }
        ]
    })
    
    # Check Accept header to determine response format
    if 'text/html' in request.headers.get('Accept', ''):
        # Return HTML documentation (simplified for now)
        html_doc = """
        <!DOCTYPE html>
        <html>
        <head>
            <title>Thought Diary API Documentation</title>
            <style>
                body { font-family: sans-serif; line-height: 1.6; max-width: 1200px; margin: 0 auto; padding: 20px; }
                h1, h2, h3 { margin-top: 20px; }
                .endpoint { margin-bottom: 10px; padding: 10px; border: 1px solid #ddd; border-radius: 4px; }
                .method { display: inline-block; padding: 3px 8px; border-radius: 3px; color: white; font-weight: bold; margin-right: 10px; }
                .get { background-color: #61affe; }
                .post { background-color: #49cc90; }
                .put { background-color: #fca130; }
                .delete { background-color: #f93e3e; }
                .auth { background-color: #7D3C98; color: white; padding: 2px 5px; border-radius: 3px; font-size: 12px; margin-left: 10px; }
                .rate { background-color: #F39C12; color: white; padding: 2px 5px; border-radius: 3px; font-size: 12px; margin-left: 10px; }
            </style>
        </head>
        <body>
            <h1>Thought Diary API Documentation</h1>
        """
        
        # Add endpoints by group
        for group in endpoints:
            html_doc += f"<h2>{group['group']}</h2>"
            
            for endpoint in group['endpoints']:
                method_class = endpoint['method'].lower()
                auth_badge = '<span class="auth">🔒 Auth Required</span>' if endpoint.get('auth_required') else ''
                rate_limit = f'<span class="rate">⏱ {endpoint["rate_limit"]}</span>' if 'rate_limit' in endpoint else ''
                
                html_doc += f"""
                <div class="endpoint">
                    <span class="method {method_class}">{endpoint['method']}</span>
                    <strong>{endpoint['path']}</strong>
                    {auth_badge} {rate_limit}
                    <p>{endpoint['description']}</p>
                </div>
                """
                
        html_doc += """
        </body>
        </html>
        """
        
        return Response(html_doc, mimetype='text/html')
    else:
        # Return JSON documentation by default
        return jsonify({
            'api_name': 'Thought Diary API',
            'version': current_app.config.get('VERSION', '0.1.0'),
            'endpoints': endpoints
        })