"""
Tests for the ThoughtDiary model.
"""
import pytest
import time
from datetime import datetime, timezone
from app.models.thought_diary import ThoughtDiary
from app.models.user import User


def test_thought_diary_creation(db):
    """Test creating a thought diary entry."""
    # First create a user to associate with the diary entry
    import time
    unique_email = f'diary_user_{int(time.time())}@example.com'
    
    # Check if a user with this email already exists
    existing_user = User.query.filter_by(email=unique_email).first()
    if existing_user:
        # Use the existing user
        user = existing_user
    else:
        # Create a new user
        user = User(email=unique_email)
        user.set_password('SecurePass123!')
        db.session.add(user)
        db.session.commit()
    
    # Create a thought diary entry
    diary = ThoughtDiary(
        user_id=user.id,
        content='Situation: Meeting with colleagues\nThoughts: I might not contribute valuable ideas\nEmotions: Anxious: 7, Nervous: 6\nBehaviors: Spoke very little, avoided eye contact\nAlternative thoughts: My ideas are worth sharing'
    )
    
    db.session.add(diary)
    db.session.commit()
    
    # Retrieve the entry and verify
    retrieved_diary = ThoughtDiary.query.filter_by(user_id=user.id).first()
    assert retrieved_diary is not None
    assert 'Meeting with colleagues' in retrieved_diary.content
    assert 'I might not contribute valuable ideas' in retrieved_diary.content
    assert 'Anxious: 7, Nervous: 6' in retrieved_diary.content
    assert 'Spoke very little, avoided eye contact' in retrieved_diary.content
    assert 'My ideas are worth sharing' in retrieved_diary.content
    assert retrieved_diary.created_at is not None
    assert retrieved_diary.updated_at is not None


def test_thought_diary_find_by_id(db):
    """Test finding a thought diary entry by ID."""
    # Create a user with unique email
    import time
    unique_email = f'find_diary_{int(time.time())}@example.com'
    
    # Check if a user with this email already exists
    existing_user = User.query.filter_by(email=unique_email).first()
    if existing_user:
        # Use the existing user
        user = existing_user
    else:
        # Create a new user
        user = User(email=unique_email)
        user.set_password('SecurePass123!')
        db.session.add(user)
        db.session.commit()
    
    # Create a thought diary entry
    diary = ThoughtDiary(
        user_id=user.id,
        content='Situation: Job interview\nThoughts: They will think I am not qualified\nEmotions: Scared: 8, Doubtful: 7\nBehaviors: Rehearsed answers repeatedly\nAlternative thoughts: I have relevant skills and experience'
    )
    
    db.session.add(diary)
    db.session.commit()
    
    # Find by ID
    found_diary = ThoughtDiary.find_by_id(diary.id)
    assert found_diary is not None
    assert found_diary.id == diary.id
    assert 'Job interview' in found_diary.content
    
    # Test finding a non-existent entry
    not_found = ThoughtDiary.find_by_id(9999)  # Assuming this ID doesn't exist
    assert not_found is None


def test_thought_diary_find_all_by_user_id(db):
    """Test finding all thought diary entries for a user."""
    # Create a user with unique email
    import time
    unique_email = f'multiple_{int(time.time())}@example.com'
    
    # Check if a user with this email already exists
    existing_user = User.query.filter_by(email=unique_email).first()
    if existing_user:
        # Use the existing user
        user = existing_user
    else:
        # Create a new user
        user = User(email=unique_email)
        user.set_password('SecurePass123!')
        db.session.add(user)
        db.session.commit()
    
    # Create multiple thought diary entries
    diary1 = ThoughtDiary(
        user_id=user.id,
        content='Situation: Presentation\nThoughts: I will forget what to say\nEmotions: Anxious: 8\nBehaviors: Over-prepared and memorized script\nAlternative thoughts: I am well-prepared and knowledgeable'
    )
    
    diary2 = ThoughtDiary(
        user_id=user.id,
        content='Situation: Social gathering\nThoughts: People will find me boring\nEmotions: Nervous: 6, Sad: 4\nBehaviors: Stayed quiet and left early\nAlternative thoughts: I can engage in meaningful conversations'
    )
    
    db.session.add_all([diary1, diary2])
    db.session.commit()
    
    # Find all entries for the user
    entries = ThoughtDiary.find_by_user_id(user.id)
    assert len(entries) == 2
    assert any('Presentation' in entry.content for entry in entries)
    assert any('Social gathering' in entry.content for entry in entries)
    
    # Test user with no entries
    unique_email = f'noentries_{int(time.time())}@example.com'
    existing_user = User.query.filter_by(email=unique_email).first()
    
    if existing_user:
        other_user = existing_user
    else:
        other_user = User(email=unique_email)
        other_user.set_password('SecurePass123!')
        db.session.add(other_user)
        db.session.commit()
    
    no_entries = ThoughtDiary.find_by_user_id(other_user.id)
    assert len(no_entries) == 0


def test_thought_diary_representation():
    """Test the string representation of a ThoughtDiary."""
    user_id = 1
    diary = ThoughtDiary(
        id=1,
        user_id=user_id,
        content='Situation: Test situation'
    )
    
    # This test might need to be adjusted based on your actual __repr__ method
    assert 'ThoughtDiary' in repr(diary)
    assert str(user_id) in repr(diary)
    assert 'ThoughtDiary' in repr(diary)


def test_thought_diary_timestamps(db):
    """Test that timestamps are set correctly."""
    import time
    unique_email = f'timestamps_{int(time.time())}@example.com'
    
    # Check if a user with this email already exists
    existing_user = User.query.filter_by(email=unique_email).first()
    if existing_user:
        # Use the existing user
        user = existing_user
    else:
        # Create a new user
        user = User(email=unique_email)
        user.set_password('SecurePass123!')
        db.session.add(user)
        db.session.commit()
    
    diary = ThoughtDiary(
        user_id=user.id,
        content='Situation: Testing timestamps\nThoughts: Thinking about time\nEmotions: Curious: 5\nBehaviors: Taking notes\nAlternative thoughts: Time is relative'
    )
    
    db.session.add(diary)
    db.session.commit()
    
    # Check that timestamps are created
    assert diary.created_at is not None
    assert diary.updated_at is not None
    
    # updated_at should match created_at initially
    assert diary.updated_at == diary.created_at


def test_thought_diary_update(db):
    """Test updating a thought diary entry."""
    import time
    unique_email = f'update_{int(time.time())}@example.com'
    
    # Check if a user with this email already exists
    existing_user = User.query.filter_by(email=unique_email).first()
    if existing_user:
        # Use the existing user
        user = existing_user
    else:
        # Create a new user
        user = User(email=unique_email)
        user.set_password('SecurePass123!')
        db.session.add(user)
        db.session.commit()
    
    diary = ThoughtDiary(
        user_id=user.id,
        content='Situation: Initial situation\nThoughts: Initial thoughts\nEmotions: Initial emotions\nBehaviors: Initial behaviors\nAlternative thoughts: Initial alternatives'
    )
    
    db.session.add(diary)
    db.session.commit()
    
    # Save the creation timestamp
    created_at = diary.created_at
    
    # Wait a moment to ensure timestamps would be different
    time.sleep(1)
    
    # Update the entry
    diary.content = 'Situation: Updated situation\nThoughts: Updated thoughts\nEmotions: Initial emotions\nBehaviors: Initial behaviors\nAlternative thoughts: Initial alternatives'
    db.session.commit()
    
    # Retrieve the updated entry
    updated_diary = ThoughtDiary.find_by_id(diary.id)
    assert 'Updated situation' in updated_diary.content
    assert 'Updated thoughts' in updated_diary.content
    
    # created_at should remain unchanged
    assert updated_diary.created_at == created_at
    
    # updated_at should be greater than created_at
    assert updated_diary.updated_at > updated_diary.created_at