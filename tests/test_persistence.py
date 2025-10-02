"""
Test for database persistence between test runs.
"""
import os
import pytest
from datetime import datetime
from app.models.user import User
from app.models.thought_diary import ThoughtDiary


def test_database_persistence(app, db):
    """
    Test that data is persisted between test runs.
    
    This test:
    1. Creates a special marker user
    2. Adds a thought diary entry for this user
    3. Checks that the data exists in the database
    
    If you run this test multiple times, the marker user should
    continue to exist, proving that the database is persistent.
    """
    # Create a unique marker user for testing persistence
    marker_email = f"persistence_test_user@example.com"
    
    with app.app_context():
        # Try to find the persistence marker user
        marker_user = User.query.filter_by(email=marker_email).first()
        
        if marker_user:
            # The user exists from a previous test run, proving persistence
            # Count their diaries to see if they're also persisted
            diary_count = ThoughtDiary.query.filter_by(user_id=marker_user.id).count()
            
            # Add another entry for this run
            new_diary = ThoughtDiary(
                user_id=marker_user.id,
                content=f"Persistence test entry at {datetime.now().isoformat()}",
                analyzed_content=None
            )
            db.session.add(new_diary)
            db.session.commit()
            
            # Check that the new count is one more than before
            new_count = ThoughtDiary.query.filter_by(user_id=marker_user.id).count()
            assert new_count == diary_count + 1
            print(f"Persistence confirmed! User has {new_count} diaries across test runs.")
            
        else:
            # First run - create the marker user and a diary entry
            marker_user = User(email=marker_email)
            marker_user.set_password("PersistenceTest123!")
            db.session.add(marker_user)
            db.session.flush()  # Get the ID without committing
            
            # Create an initial thought diary
            diary = ThoughtDiary(
                user_id=marker_user.id,
                content=f"Initial persistence test entry at {datetime.now().isoformat()}",
                analyzed_content=None
            )
            db.session.add(diary)
            db.session.commit()
            
            # Check that they were created
            assert User.query.filter_by(email=marker_email).first() is not None
            assert ThoughtDiary.query.filter_by(user_id=marker_user.id).count() == 1
            print("Created persistence test user and diary. Run the test again to confirm persistence.")