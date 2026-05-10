"""
Backend tests for the FastAPI application.
Uses pytest and the AAA pattern for clear Arrange-Act-Assert structure.
"""

import copy

from fastapi.testclient import TestClient

from src.app import app, activities

client = TestClient(app)
initial_activities = copy.deepcopy(activities)


def restore_activities():
    activities.clear()
    activities.update(copy.deepcopy(initial_activities))


def test_get_activities_returns_all_activities():
    # Arrange
    restore_activities()

    # Act
    response = client.get("/activities")

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data
    assert "Programming Class" in data
    assert isinstance(data["Chess Club"]["participants"], list)


def test_get_activities_includes_expected_fields():
    # Arrange
    restore_activities()

    # Act
    response = client.get("/activities")

    # Assert
    data = response.json()
    for activity_info in data.values():
        assert "description" in activity_info
        assert "schedule" in activity_info
        assert "max_participants" in activity_info
        assert "participants" in activity_info


def test_signup_for_activity_adds_participant():
    # Arrange
    restore_activities()
    activity_name = "Chess Club"
    email = "newstudent@mergington.edu"

    # Act
    response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": email},
    )

    # Assert
    assert response.status_code == 200
    assert response.json() == {"message": f"Signed up {email} for {activity_name}"}
    assert email in activities[activity_name]["participants"]


def test_signup_for_missing_activity_returns_404():
    # Arrange
    restore_activities()

    # Act
    response = client.post(
        "/activities/Nonexistent Activity/signup",
        params={"email": "student@mergington.edu"},
    )

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_signup_for_existing_participant_returns_400():
    # Arrange
    restore_activities()
    existing_email = initial_activities["Chess Club"]["participants"][0]

    # Act
    response = client.post(
        "/activities/Chess Club/signup",
        params={"email": existing_email},
    )

    # Assert
    assert response.status_code == 400
    assert response.json()["detail"] == "Student already signed up for this activity"