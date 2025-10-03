"""
Tests for Thought Diary API endpoints.
"""
import json
import pytest
from unittest.mock import patch
from app.models.thought_diary import ThoughtDiary
from app.database.config import db


def test_get_thought_diaries(app, client, test_user, auth_headers):
    """Test retrieving all thought diaries for a user."""
    # Create some test diary entries
    with app.app_context():
        # Check if test diaries already exist and delete them if they do
        existing_diaries = ThoughtDiary.query.filter_by(user_id=test_user.id).all()
        for diary in existing_diaries:
            db.session.delete(diary)
        
        # Create new test diaries
        diaries = [
            ThoughtDiary(
                user_id=test_user.id,
                content=f"Test diary {i}",
                analyzed_content=f"Test <span class=\"positive\">diary</span> {i}"
            )
            for i in range(3)
        ]
        db.session.add_all(diaries)
        db.session.commit()
    
    # Test API endpoint
    response = client.get('/diaries/', headers=auth_headers)
    
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'items' in data
    assert len(data['items']) == 3
    assert data['total'] == 3
    assert data['page'] == 1


def test_get_thought_diaries_pagination(app, client, test_user, auth_headers):
    """Test pagination of thought diaries."""
    # Create more test diary entries for pagination
    with app.app_context():
        # Check if test diaries already exist and delete them if they do
        existing_diaries = ThoughtDiary.query.filter_by(user_id=test_user.id).all()
        for diary in existing_diaries:
            db.session.delete(diary)
        
        # Create new test diaries
        diaries = [
            ThoughtDiary(
                user_id=test_user.id,
                content=f"Test diary {i}",
                analyzed_content=f"Test <span class=\"positive\">diary</span> {i}"
            )
            for i in range(15)  # Create 15 diaries for pagination testing
        ]
        db.session.add_all(diaries)
        db.session.commit()
    
    # Test first page with 5 items
    response = client.get('/diaries/?page=1&per_page=5', headers=auth_headers)
    
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'items' in data
    assert len(data['items']) == 5
    assert data['total'] == 15
    assert data['page'] == 1
    assert data['per_page'] == 5
    assert data['total_pages'] == 3
    
    # Test second page
    response = client.get('/diaries/?page=2&per_page=5', headers=auth_headers)
    
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'items' in data
    assert len(data['items']) == 5
    assert data['page'] == 2


def test_create_thought_diary(app, client, test_user, auth_headers):
    """Test creating a new thought diary."""
    # Test data
    diary_content = "I felt both excitement and anxious after I got elected."
    
    # Mock the sentiment analysis service
    with patch('app.services.analyzer.SentimentAnalyzer.analyze') as mock_analyze:
        mock_analyze.return_value = (
            "I felt both <span class=\"positive\">excitement</span> and <span class=\"negative\">anxious</span> after I got elected.",
            None
        )
        
        # Create a new diary
        response = client.post(
            '/diaries/',
            headers=auth_headers,
            json={'content': diary_content}
        )
    
    # Verify response
    assert response.status_code == 201
    data = json.loads(response.data)
    assert data['content'] == diary_content
    assert "<span class=\"positive\">excitement</span>" in data['analyzed_content']
    assert "<span class=\"negative\">anxious</span>" in data['analyzed_content']
    
    # Verify it was saved to the database
    with app.app_context():
        diary = ThoughtDiary.find_by_id(data['id'])
        assert diary is not None
        assert diary.content == diary_content


def test_create_thought_diary_invalid_data(client, auth_headers):
    """Test creating a diary with invalid data."""
    # Test with empty content
    response = client.post(
        '/diaries/',
        headers=auth_headers,
        json={'content': ''}
    )
    
    assert response.status_code == 400
    
    # Test with missing content field
    response = client.post(
        '/diaries/',
        headers=auth_headers,
        json={}
    )
    
    assert response.status_code == 400


def test_get_thought_diary_by_id(app, client, test_user, auth_headers):
    """Test retrieving a specific thought diary."""
    # Create a test diary
    with app.app_context():
        diary = ThoughtDiary(
            user_id=test_user.id,
            content="Test specific diary",
            analyzed_content="Test <span class=\"positive\">specific</span> diary"
        )
        db.session.add(diary)
        db.session.commit()
        diary_id = diary.id
    
    # Test API endpoint
    response = client.get(f'/diaries/{diary_id}', headers=auth_headers)
    
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['id'] == diary_id
    assert data['content'] == "Test specific diary"
    assert "<span class=\"positive\">specific</span>" in data['analyzed_content']


def test_get_nonexistent_diary(client, auth_headers):
    """Test retrieving a nonexistent diary."""
    response = client.get('/diaries/99999', headers=auth_headers)
    
    assert response.status_code == 404


def test_update_thought_diary(app, client, test_user, auth_headers):
    """Test updating a thought diary."""
    # Create a test diary
    with app.app_context():
        diary = ThoughtDiary(
            user_id=test_user.id,
            content="Original content",
            analyzed_content="Original <span class=\"positive\">content</span>"
        )
        db.session.add(diary)
        db.session.commit()
        diary_id = diary.id
    
    # Updated content
    updated_content = "Updated content with more positive thoughts"
    
    # Mock the sentiment analysis service
    with patch('app.services.analyzer.SentimentAnalyzer.analyze') as mock_analyze:
        mock_analyze.return_value = (
            "Updated content with more <span class=\"positive\">positive</span> thoughts",
            None
        )
        
        # Update the diary
        response = client.put(
            f'/diaries/{diary_id}',
            headers=auth_headers,
            json={'content': updated_content}
        )
    
    # Verify response
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['content'] == updated_content
    assert "<span class=\"positive\">positive</span>" in data['analyzed_content']
    
    # Verify it was updated in the database
    with app.app_context():
        updated_diary = ThoughtDiary.find_by_id(diary_id)
        assert updated_diary.content == updated_content


def test_delete_thought_diary(app, client, test_user, auth_headers):
    """Test deleting a thought diary."""
    # Create a test diary
    with app.app_context():
        diary = ThoughtDiary(
            user_id=test_user.id,
            content="Diary to delete",
            analyzed_content="Diary to <span class=\"negative\">delete</span>"
        )
        db.session.add(diary)
        db.session.commit()
        diary_id = diary.id
    
    # Delete the diary
    response = client.delete(f'/diaries/{diary_id}', headers=auth_headers)
    
    # Verify response
    assert response.status_code == 200
    
    # Verify it was deleted from the database
    with app.app_context():
        deleted_diary = ThoughtDiary.find_by_id(diary_id)
        assert deleted_diary is None


def test_get_diary_stats(app, client, test_user, auth_headers):
    """Test getting diary statistics."""
    # Create some test diaries
    with app.app_context():
        # Check if test diaries already exist and delete them if they do
        existing_diaries = ThoughtDiary.query.filter_by(user_id=test_user.id).all()
        for diary in existing_diaries:
            db.session.delete(diary)
        
        # Create diaries with different sentiment patterns
        diaries = [
            # Positive sentiment
            ThoughtDiary(
                user_id=test_user.id,
                content="Positive diary",
                analyzed_content="<span class=\"positive\">Positive</span> diary with <span class=\"positive\">good</span> content"
            ),
            # Negative sentiment
            ThoughtDiary(
                user_id=test_user.id,
                content="Negative diary",
                analyzed_content="<span class=\"negative\">Negative</span> diary with <span class=\"negative\">bad</span> content"
            ),
            # Neutral sentiment (equal positive and negative)
            ThoughtDiary(
                user_id=test_user.id,
                content="Mixed diary",
                analyzed_content="<span class=\"positive\">Good</span> and <span class=\"negative\">bad</span> content"
            )
        ]
        db.session.add_all(diaries)
        db.session.commit()
    
    # Test API endpoint
    response = client.get('/diaries/stats', headers=auth_headers)
    
    # Verify response
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'total_entries' in data
    assert data['total_entries'] == 3
    assert 'sentiment_counts' in data
    assert data['sentiment_counts']['positive'] == 1
    assert data['sentiment_counts']['negative'] == 1
    assert data['sentiment_counts']['neutral'] == 1