from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)


def test_get_activities():
    """Test retrieving all activities"""
    # Arrange - TestClient is already set up

    # Act
    response = client.get("/activities")

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert len(data) == 9  # We have 9 activities
    assert "Chess Club" in data
    assert "participants" in data["Chess Club"]
    assert "max_participants" in data["Chess Club"]


def test_signup_for_activity():
    """Test signing up for an activity"""
    # Arrange
    email = "newstudent@mergington.edu"
    activity = "Programming Class"

    # Act
    response = client.post(f"/activities/{activity}/signup?email={email}")

    # Assert
    assert response.status_code == 200
    result = response.json()
    assert "Signed up" in result["message"]
    assert email in result["message"]

    # Verify the participant was added
    response2 = client.get("/activities")
    data = response2.json()
    assert email in data[activity]["participants"]


def test_signup_duplicate():
    """Test signing up for an activity when already signed up"""
    # Arrange
    email = "emma@mergington.edu"  # Already in Programming Class
    activity = "Programming Class"

    # Act
    response = client.post(f"/activities/{activity}/signup?email={email}")

    # Assert
    assert response.status_code == 400
    result = response.json()
    assert "already signed up" in result["detail"]


def test_signup_activity_not_found():
    """Test signing up for a non-existent activity"""
    # Arrange
    email = "test@mergington.edu"
    activity = "Nonexistent Activity"

    # Act
    response = client.post(f"/activities/{activity}/signup?email={email}")

    # Assert
    assert response.status_code == 404
    result = response.json()
    assert "Activity not found" in result["detail"]


def test_unregister_from_activity():
    """Test unregistering from an activity"""
    # Arrange
    email = "sophia@mergington.edu"  # Already in Programming Class
    activity = "Programming Class"

    # Act
    response = client.delete(f"/activities/{activity}/signup?email={email}")

    # Assert
    assert response.status_code == 200
    result = response.json()
    assert "Unregistered" in result["message"]
    assert email in result["message"]

    # Verify the participant was removed
    response2 = client.get("/activities")
    data = response2.json()
    assert email not in data[activity]["participants"]


def test_unregister_participant_not_found():
    """Test unregistering a participant who is not signed up"""
    # Arrange
    email = "nonexistent@mergington.edu"
    activity = "Chess Club"

    # Act
    response = client.delete(f"/activities/{activity}/signup?email={email}")

    # Assert
    assert response.status_code == 404
    result = response.json()
    assert "Participant not found" in result["detail"]


def test_unregister_activity_not_found():
    """Test unregistering from a non-existent activity"""
    # Arrange
    email = "test@mergington.edu"
    activity = "Nonexistent Activity"

    # Act
    response = client.delete(f"/activities/{activity}/signup?email={email}")

    # Assert
    assert response.status_code == 404
    result = response.json()
    assert "Activity not found" in result["detail"]