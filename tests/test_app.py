import copy

import pytest
from fastapi.testclient import TestClient

from src.app import app, activities

client = TestClient(app)
original_activities = copy.deepcopy(activities)


@pytest.fixture(autouse=True)
def reset_activities():
    activities.clear()
    activities.update(copy.deepcopy(original_activities))
    yield
    activities.clear()
    activities.update(copy.deepcopy(original_activities))


class TestActivities:
    def test_get_activities_returns_all_activities(self):
        # Arrange
        expected_activity_key = "Chess Club"

        # Act
        response = client.get("/activities")

        # Assert
        assert response.status_code == 200
        data = response.json()
        assert expected_activity_key in data
        assert isinstance(data[expected_activity_key]["participants"], list)

    def test_get_activities_includes_required_fields(self):
        # Arrange / Act
        response = client.get("/activities")
        data = response.json()

        # Assert
        for activity in data.values():
            assert "description" in activity
            assert "schedule" in activity
            assert "max_participants" in activity
            assert "participants" in activity
            assert isinstance(activity["participants"], list)


class TestSignup:
    def test_signup_adds_participant(self):
        # Arrange
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

    def test_signup_duplicate_returns_400(self):
        # Arrange
        activity_name = "Chess Club"
        email = "duplicate@mergington.edu"
        client.post(f"/activities/{activity_name}/signup", params={"email": email})

        # Act
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email},
        )

        # Assert
        assert response.status_code == 400
        assert response.json()["detail"] == "Student already signed up for this activity"

    def test_signup_nonexistent_activity_returns_404(self):
        # Act
        response = client.post(
            "/activities/Nonexistent Activity/signup",
            params={"email": "student@mergington.edu"},
        )

        # Assert
        assert response.status_code == 404
        assert response.json()["detail"] == "Activity not found"


class TestRemoveParticipant:
    def test_remove_participant(self):
        # Arrange
        activity_name = "Basketball Club"
        email = "delete-me@mergington.edu"
        client.post(f"/activities/{activity_name}/signup", params={"email": email})

        # Act
        response = client.delete(f"/activities/{activity_name}/participants/{email}")

        # Assert
        assert response.status_code == 200
        assert response.json() == {"message": f"Removed {email} from {activity_name}"}
        assert email not in activities[activity_name]["participants"]

    def test_remove_nonexistent_participant_returns_404(self):
        # Arrange
        activity_name = "Soccer Team"
        email = "missing@mergington.edu"

        # Act
        response = client.delete(f"/activities/{activity_name}/participants/{email}")

        # Assert
        assert response.status_code == 404
        assert response.json()["detail"] == "Participant not found"

    def test_remove_from_nonexistent_activity_returns_404(self):
        # Act
        response = client.delete(
            "/activities/NotARealActivity/participants/test@mergington.edu"
        )

        # Assert
        assert response.status_code == 404
        assert response.json()["detail"] == "Activity not found"
