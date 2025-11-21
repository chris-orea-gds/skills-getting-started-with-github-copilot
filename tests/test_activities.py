from fastapi.testclient import TestClient
from src.app import app, activities

client = TestClient(app)

TEST_ACTIVITY = "Chess Club"
TEST_EMAIL = "tester@example.com"


def setup_function():
    # Ensure test email not present before each test
    if TEST_EMAIL in activities[TEST_ACTIVITY]["participants"]:
        activities[TEST_ACTIVITY]["participants"].remove(TEST_EMAIL)


def teardown_function():
    # Clean up after test
    if TEST_EMAIL in activities[TEST_ACTIVITY]["participants"]:
        activities[TEST_ACTIVITY]["participants"].remove(TEST_EMAIL)


def test_get_activities():
    resp = client.get("/activities")
    assert resp.status_code == 200
    data = resp.json()
    assert TEST_ACTIVITY in data


def test_signup_and_remove_participant():
    # Signup
    resp = client.post(f"/activities/{TEST_ACTIVITY}/signup?email={TEST_EMAIL}")
    assert resp.status_code == 200
    assert TEST_EMAIL in activities[TEST_ACTIVITY]["participants"]

    # Remove
    resp = client.delete(f"/activities/{TEST_ACTIVITY}/remove?email={TEST_EMAIL}")
    assert resp.status_code == 200
    assert TEST_EMAIL not in activities[TEST_ACTIVITY]["participants"]
