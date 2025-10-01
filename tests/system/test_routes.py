"""
Tests for system endpoints including health, version, and documentation.
"""
import json
import pytest


def test_health_endpoint(client):
    """Test the health check endpoint."""
    response = client.get('/health')
    
    assert response.status_code == 200
    json_data = json.loads(response.data)
    assert json_data['status'] == 'healthy'
    assert 'database' in json_data
    assert 'environment' in json_data


def test_version_endpoint(client):
    """Test the version information endpoint."""
    response = client.get('/version')
    
    assert response.status_code == 200
    json_data = json.loads(response.data)
    assert 'version' in json_data
    assert 'environment' in json_data
    assert json_data['environment'] == 'testing'


def test_docs_endpoint_json(client):
    """Test the API documentation endpoint returning JSON."""
    # Default request without Accept header should return JSON
    response = client.get('/docs')
    
    assert response.status_code == 200
    json_data = json.loads(response.data)
    assert 'api_name' in json_data
    assert 'version' in json_data
    assert 'endpoints' in json_data
    
    # Check that all endpoint groups are included
    endpoint_groups = [group['group'] for group in json_data['endpoints']]
    assert 'System' in endpoint_groups
    assert 'Authentication' in endpoint_groups
    assert 'Thought Diaries' in endpoint_groups


def test_docs_endpoint_html(client):
    """Test the API documentation endpoint returning HTML."""
    response = client.get(
        '/docs', 
        headers={'Accept': 'text/html'}
    )
    
    assert response.status_code == 200
    assert response.content_type == 'text/html; charset=utf-8'
    assert b'<!DOCTYPE html>' in response.data
    assert b'Thought Diary API Documentation' in response.data