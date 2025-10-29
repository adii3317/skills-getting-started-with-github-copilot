import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)


def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert "Chess Club" in data
    assert "Programming Class" in data


def test_signup_for_activity():
    email = "newstudent@mergington.edu"
    activity = "Chess Club"
    response = client.post(f"/activities/{activity}/signup", params={"email": email})
    assert response.status_code == 200
    assert response.json()["message"] == f"Signed up {email} for {activity}"
    # Try signing up again (should fail)
    response = client.post(f"/activities/{activity}/signup", params={"email": email})
    assert response.status_code == 400


def test_unregister_from_activity():
    email = "emma@mergington.edu"
    activity = "Programming Class"
    response = client.post(f"/activities/{activity}/unregister", params={"email": email})
    assert response.status_code == 200
    assert response.json()["message"] == f"Unregistered {email} from {activity}"
    # Try unregistering again (should fail)
    response = client.post(f"/activities/{activity}/unregister", params={"email": email})
    assert response.status_code == 404


def test_signup_invalid_activity():
    response = client.post("/activities/Nonexistent/signup", params={"email": "test@mergington.edu"})
    assert response.status_code == 404


def test_unregister_invalid_activity():
    response = client.post("/activities/Nonexistent/unregister", params={"email": "test@mergington.edu"})
    assert response.status_code == 404


def test_unregister_missing_email():
    activity = "Chess Club"
    response = client.post(f"/activities/{activity}/unregister")
    assert response.status_code == 400
