"""
Unit tests for data models and utility functions using the Arrange-Act-Assert pattern.

These tests validate data structure, types, and helper logic at a unit level,
separate from endpoint integration testing.
"""

import pytest
from src.app import activities


class TestActivityDataStructure:
    """Unit tests for validating activity data structure and fields."""
    
    def test_activity_has_required_fields(self):
        """
        Test that each activity contains all required fields.
        
        Arrange: Define required field names
        Act: Iterate through all activities
        Assert: Verify each activity has all required fields
        """
        # ARRANGE
        required_fields = {"description", "schedule", "max_participants", "participants"}
        
        # ACT & ASSERT
        for activity_name, activity_data in activities.items():
            # Each activity must have all required fields
            assert all(field in activity_data for field in required_fields), \
                f"Activity '{activity_name}' missing required fields"
            # Each field must have the correct type
            assert isinstance(activity_data["description"], str)
            assert isinstance(activity_data["schedule"], str)
            assert isinstance(activity_data["max_participants"], int)
            assert isinstance(activity_data["participants"], list)
    
    def test_activity_description_not_empty(self):
        """
        Test that all activities have non-empty descriptions.
        
        Arrange: Get all activities
        Act: Check description field for each
        Assert: Verify all descriptions are non-empty strings
        """
        # ARRANGE & ACT
        for activity_name, activity_data in activities.items():
            # ASSERT
            assert activity_data["description"], \
                f"Activity '{activity_name}' has empty description"
            assert len(activity_data["description"]) > 0
            assert isinstance(activity_data["description"], str)
    
    def test_activity_schedule_not_empty(self):
        """
        Test that all activities have non-empty schedules.
        
        Arrange: Get all activities
        Act: Check schedule field for each
        Assert: Verify all schedules are non-empty strings
        """
        # ARRANGE & ACT
        for activity_name, activity_data in activities.items():
            # ASSERT
            assert activity_data["schedule"], \
                f"Activity '{activity_name}' has empty schedule"
            assert len(activity_data["schedule"]) > 0
            assert isinstance(activity_data["schedule"], str)
    
    def test_activity_max_participants_positive(self):
        """
        Test that all activities have positive max_participants values.
        
        Arrange: Get all activities
        Act: Check max_participants field for each
        Assert: Verify all max_participants are positive integers
        """
        # ARRANGE & ACT
        for activity_name, activity_data in activities.items():
            # ASSERT
            assert activity_data["max_participants"] > 0, \
                f"Activity '{activity_name}' has non-positive max_participants"
            assert isinstance(activity_data["max_participants"], int)


class TestParticipantListValidation:
    """Unit tests for validating participant list data and format."""
    
    def test_participants_is_list(self):
        """
        Test that participants field is always a list.
        
        Arrange: Get all activities
        Act: Check participants field type
        Assert: Verify participants is a list for all activities
        """
        # ARRANGE & ACT
        for activity_name, activity_data in activities.items():
            # ASSERT
            assert isinstance(activity_data["participants"], list), \
                f"Activity '{activity_name}' participants is not a list"
    
    def test_participants_are_email_strings(self):
        """
        Test that all participants are valid email-like strings.
        
        Arrange: Define email validation pattern
        Act: Iterate through all participants in all activities
        Assert: Verify each participant contains '@' as basic email validation
        """
        # ARRANGE
        activities_data = activities
        
        # ACT & ASSERT
        for activity_name, activity_data in activities_data.items():
            for participant in activity_data["participants"]:
                # Basic email validation: must be a string with @ symbol
                assert isinstance(participant, str), \
                    f"Participant in {activity_name} is not a string: {participant}"
                assert "@" in participant, \
                    f"Participant '{participant}' in {activity_name} missing '@' symbol"
                assert len(participant) > 0
    
    def test_no_duplicate_participants_in_activity(self):
        """
        Test that no activity has duplicate participants.
        
        Arrange: Store activity participants
        Act: Convert list to set and compare lengths
        Assert: Verify list length equals set length (no duplicates)
        """
        # ARRANGE & ACT
        for activity_name, activity_data in activities.items():
            participants = activity_data["participants"]
            unique_participants = set(participants)
            
            # ASSERT
            assert len(participants) == len(unique_participants), \
                f"Activity '{activity_name}' has duplicate participants"
    
    def test_participants_count_within_limits(self):
        """
        Test that participant count doesn't exceed max_participants.
        
        Arrange: Store participant count and max capacity
        Act: Compare counts
        Assert: Verify current participants don't exceed max allowed
        """
        # ARRANGE & ACT
        for activity_name, activity_data in activities.items():
            current_count = len(activity_data["participants"])
            max_allowed = activity_data["max_participants"]
            
            # ASSERT
            assert current_count <= max_allowed, \
                f"Activity '{activity_name}' has {current_count} participants " \
                f"but max is {max_allowed}"


class TestActivityDataConsistency:
    """Unit tests for overall data consistency across activities."""
    
    def test_all_activities_exist_and_not_none(self):
        """
        Test that activities dictionary is populated and not empty.
        
        Arrange: Get activities dictionary
        Act: Check if activities exist
        Assert: Verify activities is a non-empty dictionary
        """
        # ARRANGE & ACT
        total_activities = len(activities)
        
        # ASSERT
        assert total_activities > 0, "No activities found in database"
        assert activities is not None
    
    def test_activity_names_are_valid_strings(self):
        """
        Test that all activity names are valid non-empty strings.
        
        Arrange: Get all activity names
        Act: Validate each name
        Assert: Verify all names are non-empty strings with word characters
        """
        # ARRANGE & ACT
        for activity_name in activities.keys():
            # ASSERT
            assert isinstance(activity_name, str), \
                f"Activity name is not a string: {activity_name}"
            assert len(activity_name) > 0, "Activity name is empty"
            assert activity_name[0].isupper(), \
                f"Activity name '{activity_name}' should start with capital letter"
