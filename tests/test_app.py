import pytest
from fastapi.testclient import TestClient
from src.app import app, activities


@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture(autouse=True)
def reset_activities():
    # Reset activities to original state before each test
    global activities
    activities = {
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
        "Basketball Team": {
            "description": "Competitive basketball training and matches",
            "schedule": "Mondays and Wednesdays, 4:00 PM - 5:30 PM",
            "max_participants": 15,
            "participants": ["alex@mergington.edu"]
        },
        "Soccer Club": {
            "description": "Soccer practice and friendly matches",
            "schedule": "Tuesdays and Thursdays, 4:00 PM - 5:30 PM",
            "max_participants": 18,
            "participants": ["lucas@mergington.edu", "noah@mergington.edu"]
        },
        "Art Studio": {
            "description": "Painting, drawing, and visual arts creation",
            "schedule": "Wednesdays, 3:30 PM - 5:00 PM",
            "max_participants": 16,
            "participants": ["grace@mergington.edu"]
        },
        "Drama Club": {
            "description": "Theater performances and acting workshops",
            "schedule": "Fridays, 4:00 PM - 5:30 PM",
            "max_participants": 20,
            "participants": ["isabella@mergington.edu", "mason@mergington.edu"]
        },
        "Debate Team": {
            "description": "Competitive debating and public speaking",
            "schedule": "Mondays, 3:30 PM - 4:30 PM",
            "max_participants": 10,
            "participants": ["ethan@mergington.edu"]
        },
        "Science Club": {
            "description": "Experiments, research projects, and STEM exploration",
            "schedule": "Thursdays, 3:30 PM - 5:00 PM",
            "max_participants": 25,
            "participants": ["chloe@mergington.edu", "benjamin@mergington.edu"]
        }
    }


def test_root_redirect(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.url.path == "/static/index.html"


def test_get_activities(client):
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data
    assert "Programming Class" in data
    # Check structure of one activity
    chess_club = data["Chess Club"]
    assert "description" in chess_club
    assert "schedule" in chess_club
    assert "max_participants" in chess_club
    assert "participants" in chess_club
    assert isinstance(chess_club["participants"], list)


def test_signup_success(client):
    response = client.post("/activities/Chess Club/signup", params={"email": "newstudent@mergington.edu"})
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "newstudent@mergington.edu" in data["message"]
    assert "Chess Club" in data["message"]
    # Check that student was added
    activities_response = client.get("/activities")
    chess_club = activities_response.json()["Chess Club"]
    assert "newstudent@mergington.edu" in chess_club["participants"]


def test_signup_activity_not_found(client):
    response = client.post("/activities/Nonexistent Activity/signup", params={"email": "student@mergington.edu"})
    assert response.status_code == 404
    data = response.json()
    assert "detail" in data
    assert "Activity not found" in data["detail"]


def test_signup_already_signed_up(client):
    response = client.post("/activities/Chess Club/signup", params={"email": "michael@mergington.edu"})
    assert response.status_code == 400
    data = response.json()
    assert "detail" in data
    assert "Student already signed up for this activity" in data["detail"]


def test_unregister_success(client):
    response = client.delete("/activities/Chess Club/unregister", params={"email": "michael@mergington.edu"})
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "michael@mergington.edu" in data["message"]
    assert "Chess Club" in data["message"]
    # Check that student was removed
    activities_response = client.get("/activities")
    chess_club = activities_response.json()["Chess Club"]
    assert "michael@mergington.edu" not in chess_club["participants"]


def test_unregister_activity_not_found(client):
    response = client.delete("/activities/Nonexistent Activity/unregister", params={"email": "student@mergington.edu"})
    assert response.status_code == 404
    data = response.json()
    assert "detail" in data
    assert "Activity not found" in data["detail"]


def test_unregister_not_registered(client):
    response = client.delete("/activities/Chess Club/unregister", params={"email": "notregistered@mergington.edu"})
    assert response.status_code == 400
    data = response.json()
    assert "detail" in data
    assert "Student not registered for this activity" in data["detail"]