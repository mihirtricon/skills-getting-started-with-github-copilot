"""
Pytest configuration and shared fixtures for the test suite.
"""

import pytest
from fastapi.testclient import TestClient
from src.app import app, activities


@pytest.fixture
def test_client():
    """
    Provide a TestClient instance for making HTTP requests to the FastAPI application.
    
    This fixture allows tests to make HTTP calls to endpoints without needing
    a running server.
    """
    return TestClient(app)


@pytest.fixture(autouse=True)
def reset_activities():
    """
    Reset activities to initial state before each test.
    
    This fixture automatically runs before every test to ensure a clean state.
    Tests can modify the activities data without affecting other tests.
    """
    # Store the original initial state
    original_activities = {
        "Chess Club": {
            "description": "Learn strategies and compete in chess tournaments",
            "schedule": "Fridays, 3:30 PM - 5:00 PM",
            "max_participants": 12,
            "participants": ["michael@mergington.edu", "daniel@mergington.edu"]
        },
        "Programming Class": {
            "description": "Learn programming fundamentals and build software projects",
            "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
            "max_participants": 20,
            "participants": ["emma@mergington.edu", "sophia@mergington.edu"]
        },
        "Gym Class": {
            "description": "Physical education and sports activities",
            "schedule": "Mondays, Wednesdays, Fridays, 2:00 PM - 3:00 PM",
            "max_participants": 30,
            "participants": ["john@mergington.edu", "olivia@mergington.edu"]
        },
        "Soccer Team": {
            "description": "Practice team play and compete in soccer matches",
            "schedule": "Tuesdays and Thursdays, 4:00 PM - 5:30 PM",
            "max_participants": 22,
            "participants": ["alex@mergington.edu", "nina@mergington.edu"]
        },
        "Swimming Club": {
            "description": "Develop swimming techniques and participate in swim meets",
            "schedule": "Wednesdays and Fridays, 4:00 PM - 5:00 PM",
            "max_participants": 18,
            "participants": ["liam@mergington.edu", "maya@mergington.edu"]
        },
        "Art Studio": {
            "description": "Explore painting, drawing, and mixed media art projects",
            "schedule": "Mondays and Wednesdays, 3:30 PM - 5:00 PM",
            "max_participants": 16,
            "participants": ["ava@mergington.edu", "lucas@mergington.edu"]
        },
        "Drama Club": {
            "description": "Rehearse scenes, perform plays, and build stage confidence",
            "schedule": "Tuesdays and Thursdays, 4:00 PM - 5:30 PM",
            "max_participants": 20,
            "participants": ["mia@mergington.edu", "ethan@mergington.edu"]
        },
        "Robotics Club": {
            "description": "Design and build robots for competitions and challenges",
            "schedule": "Mondays and Thursdays, 4:00 PM - 6:00 PM",
            "max_participants": 14,
            "participants": ["oliver@mergington.edu", "hannah@mergington.edu"]
        },
        "Debate Team": {
            "description": "Develop argumentative skills and compete in debate tournaments",
            "schedule": "Wednesdays, 4:00 PM - 5:30 PM",
            "max_participants": 15,
            "participants": ["sophia@mergington.edu", "david@mergington.edu"]
        }
    }
    
    # Clear and repopulate the activities dict to reset state
    activities.clear()
    activities.update(original_activities)
    yield
    # Cleanup after test (optional but good practice)
    activities.clear()
    activities.update(original_activities)
