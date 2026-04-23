"""
Integration tests for FastAPI endpoints using the Arrange-Act-Assert pattern.

Each test follows the AAA pattern:
- Arrange: Set up test data and parameters
- Act: Make the HTTP request to the endpoint
- Assert: Verify the response status code and content
"""

import pytest


class TestRootEndpoint:
    """Tests for the GET / root endpoint."""
    
    def test_get_root_redirects_to_static_index(self, test_client):
        """
        Test that GET / redirects to /static/index.html.
        
        Arrange: Prepare test client
        Act: Make GET request to root endpoint with follow_redirects=False
        Assert: Verify status code is 307 (temporary redirect) and location header points to /static/index.html
        """
        # ARRANGE
        expected_redirect_url = "/static/index.html"
        
        # ACT
        response = test_client.get("/", follow_redirects=False)
        
        # ASSERT
        assert response.status_code == 307
        assert response.headers["location"] == expected_redirect_url


class TestGetActivitiesEndpoint:
    """Tests for the GET /activities endpoint."""
    
    def test_get_all_activities_returns_complete_list(self, test_client):
        """
        Test that GET /activities returns all activities with complete data.
        
        Arrange: Prepare test client and expected activity count
        Act: Make GET request to /activities endpoint
        Assert: Verify response contains all 9 activities with correct structure
        """
        # ARRANGE
        expected_activity_count = 9
        expected_activities = [
            "Chess Club", "Programming Class", "Gym Class", 
            "Soccer Team", "Swimming Club", "Art Studio", 
            "Drama Club", "Robotics Club", "Debate Team"
        ]
        
        # ACT
        response = test_client.get("/activities")
        activities = response.json()
        
        # ASSERT
        assert response.status_code == 200
        assert len(activities) == expected_activity_count
        for activity_name in expected_activities:
            assert activity_name in activities
    
    def test_get_activities_returns_activity_structure(self, test_client):
        """
        Test that each activity has the required fields.
        
        Arrange: Prepare expected field names
        Act: Make GET request to /activities and retrieve first activity
        Assert: Verify activity contains all required fields
        """
        # ARRANGE
        required_fields = {"description", "schedule", "max_participants", "participants"}
        
        # ACT
        response = test_client.get("/activities")
        activities = response.json()
        chess_club = activities["Chess Club"]
        
        # ASSERT
        assert response.status_code == 200
        assert all(field in chess_club for field in required_fields)
        assert isinstance(chess_club["participants"], list)
        assert isinstance(chess_club["max_participants"], int)
    
    def test_get_activities_includes_existing_participants(self, test_client):
        """
        Test that activities include their existing participants.
        
        Arrange: Prepare expected initial participants for Chess Club
        Act: Make GET request to /activities
        Assert: Verify Chess Club includes expected initial participants
        """
        # ARRANGE
        expected_participants = ["michael@mergington.edu", "daniel@mergington.edu"]
        
        # ACT
        response = test_client.get("/activities")
        activities = response.json()
        chess_club_participants = activities["Chess Club"]["participants"]
        
        # ASSERT
        assert response.status_code == 200
        assert chess_club_participants == expected_participants


class TestSignupEndpoint:
    """Tests for the POST /activities/{activity_name}/signup endpoint."""
    
    def test_signup_successful_adds_participant(self, test_client):
        """
        Test that a student can successfully sign up for an activity.
        
        Arrange: Prepare email of student not yet signed up
        Act: Make POST request to signup endpoint
        Assert: Verify response is 200 and success message returned
        """
        # ARRANGE
        activity_name = "Chess Club"
        email = "netstudent@example.com"
        
        # ACT
        response = test_client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )
        
        # ASSERT
        assert response.status_code == 200
        assert "Signed up" in response.json()["message"]
        assert email in response.json()["message"]
    
    def test_signup_invalid_activity_returns_404(self, test_client):
        """
        Test that signup to a non-existent activity returns 404.
        
        Arrange: Prepare signup request with invalid activity name
        Act: Make POST request to signup endpoint with invalid activity
        Assert: Verify response is 404 with appropriate error message
        """
        # ARRANGE
        invalid_activity = "Nonexistent Club"
        email = "student@example.com"
        
        # ACT
        response = test_client.post(
            f"/activities/{invalid_activity}/signup",
            params={"email": email}
        )
        
        # ASSERT
        assert response.status_code == 404
        assert "Activity not found" in response.json()["detail"]
    
    def test_signup_duplicate_participant_returns_400(self, test_client):
        """
        Test that a student already signed up cannot sign up again.
        
        Arrange: Prepare signup request with email already registered
        Act: Make POST request to signup endpoint with existing participant
        Assert: Verify response is 400 with duplicate signup error message
        """
        # ARRANGE
        activity_name = "Chess Club"
        existing_email = "michael@mergington.edu"  # Already in Chess Club
        
        # ACT
        response = test_client.post(
            f"/activities/{activity_name}/signup",
            params={"email": existing_email}
        )
        
        # ASSERT
        assert response.status_code == 400
        assert "already signed up" in response.json()["detail"]
    
    def test_signup_missing_email_parameter_returns_400(self, test_client):
        """
        Test that signup without email parameter returns 400.
        
        Arrange: Prepare signup request without email parameter
        Act: Make POST request to signup endpoint without email
        Assert: Verify response is 422 (validation error for missing required param)
        """
        # ARRANGE
        activity_name = "Chess Club"
        
        # ACT
        response = test_client.post(f"/activities/{activity_name}/signup")
        
        # ASSERT
        assert response.status_code == 422  # FastAPI returns 422 for missing required parameters


class TestRemoveParticipantEndpoint:
    """Tests for the DELETE /activities/{activity_name}/participants endpoint."""
    
    def test_remove_participant_successful(self, test_client):
        """
        Test that a participant can be removed from an activity.
        
        Arrange: Prepare participant email to remove
        Act: Make DELETE request to remove endpoint with existing participant
        Assert: Verify response is 200 with success message
        """
        # ARRANGE
        activity_name = "Chess Club"
        email = "michael@mergington.edu"  # Initial participant
        
        # ACT
        response = test_client.delete(
            f"/activities/{activity_name}/participants",
            params={"email": email}
        )
        
        # ASSERT
        assert response.status_code == 200
        assert "Removed" in response.json()["message"]
        assert email in response.json()["message"]
    
    def test_remove_participant_invalid_activity_returns_404(self, test_client):
        """
        Test that removing from a non-existent activity returns 404.
        
        Arrange: Prepare removal request with invalid activity name
        Act: Make DELETE request with invalid activity
        Assert: Verify response is 404 with appropriate error message
        """
        # ARRANGE
        invalid_activity = "Nonexistent Club"
        email = "student@example.com"
        
        # ACT
        response = test_client.delete(
            f"/activities/{invalid_activity}/participants",
            params={"email": email}
        )
        
        # ASSERT
        assert response.status_code == 404
        assert "Activity not found" in response.json()["detail"]
    
    def test_remove_nonexistent_participant_returns_404(self, test_client):
        """
        Test that removing a participant not in the activity returns 404.
        
        Arrange: Prepare removal request with email not in activity
        Act: Make DELETE request with email not in participants list
        Assert: Verify response is 404 with participant not found error
        """
        # ARRANGE
        activity_name = "Chess Club"
        email = "notinlist@example.com"  # Not in Chess Club participants
        
        # ACT
        response = test_client.delete(
            f"/activities/{activity_name}/participants",
            params={"email": email}
        )
        
        # ASSERT
        assert response.status_code == 404
        assert "Participant not found" in response.json()["detail"]
    
    def test_remove_participant_missing_email_parameter_returns_422(self, test_client):
        """
        Test that removal without email parameter returns 422.
        
        Arrange: Prepare removal request without email parameter
        Act: Make DELETE request without email query parameter
        Assert: Verify response is 422 (validation error for missing required param)
        """
        # ARRANGE
        activity_name = "Chess Club"
        
        # ACT
        response = test_client.delete(f"/activities/{activity_name}/participants")
        
        # ASSERT
        assert response.status_code == 422


class TestEndToEndWorkflow:
    """Integration tests for complete workflows combining multiple operations."""
    
    def test_signup_then_remove_workflow(self, test_client):
        """
        Test complete workflow: signup a student, verify they're added, then remove them.
        
        Arrange: Prepare student email
        Act: Sign up student, retrieve activities, remove student
        Assert: Verify student is added after signup and removed after deletion
        """
        # ARRANGE
        activity_name = "Art Studio"
        email = "workflow@example.com"
        
        # ACT - Signup
        signup_response = test_client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )
        
        # ASSERT - Signup successful
        assert signup_response.status_code == 200
        
        # ACT - Get activities to verify participant added
        get_response = test_client.get("/activities")
        participants = get_response.json()[activity_name]["participants"]
        
        # ASSERT - Participant in list
        assert email in participants
        
        # ACT - Remove participant
        remove_response = test_client.delete(
            f"/activities/{activity_name}/participants",
            params={"email": email}
        )
        
        # ASSERT - Removal successful
        assert remove_response.status_code == 200
        
        # ACT - Get activities again to verify participant removed
        final_response = test_client.get("/activities")
        final_participants = final_response.json()[activity_name]["participants"]
        
        # ASSERT - Participant no longer in list
        assert email not in final_participants
