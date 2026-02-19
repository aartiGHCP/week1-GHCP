from fastapi.testclient import TestClient
from src.app import app, activities


client = TestClient(app)


def test_get_activities():
    resp = client.get("/activities")
    assert resp.status_code == 200
    data = resp.json()
    # Should return a dict of activities
    assert isinstance(data, dict)
    assert "Basketball" in data


def test_signup_and_unregister_flow():
    activity = "Basketball"
    email = "test_student@example.com"

    # Ensure email not already present
    if email in activities[activity]["participants"]:
        activities[activity]["participants"].remove(email)

    # Sign up
    signup = client.post(f"/activities/{activity}/signup", params={"email": email})
    assert signup.status_code == 200
    assert "Signed up" in signup.json().get("message", "")

    # Confirm participant is in list
    resp = client.get("/activities")
    assert resp.status_code == 200
    assert email in resp.json()[activity]["participants"]

    # Unregister
    unreg = client.post(f"/activities/{activity}/unregister", params={"email": email})
    assert unreg.status_code == 200
    assert "Unregistered" in unreg.json().get("message", "")

    # Confirm removal
    resp2 = client.get("/activities")
    assert email not in resp2.json()[activity]["participants"]
