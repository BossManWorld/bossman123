import pytest
from app import app

@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client

def test_health_check(client):
    res = client.get("/api/health")
    assert res.status_code == 200
    assert res.get_json()["status"] == "ok"

def test_get_all_students(client):
    res = client.get("/api/students")
    assert res.status_code == 200
    assert isinstance(res.get_json(), list)

def test_get_student_found(client):
    res = client.get("/api/students/1")
    assert res.status_code == 200

def test_get_student_not_found(client):
    res = client.get("/api/students/999")
    assert res.status_code == 404

def test_add_student(client):
    res = client.post("/api/students",
        json={"name": "Yahya", "grade": "A"})
    assert res.status_code == 201
    assert res.get_json()["name"] == "Yahya"

def test_add_student_missing_field(client):
    res = client.post("/api/students",
        json={"name": "Yahya"})
    assert res.status_code == 400
