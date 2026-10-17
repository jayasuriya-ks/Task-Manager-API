from app import app

def test_home():
    app.config["TESTING"] = True
    client = app.test_client()

    response = client.get("/")

    assert response.status_code == 200
    assert response.get_json() == {
        "message": "Task Manager API is running!"
    }

def test_create_task_without_title():
    app.config["TESTING"] = True
    client = app.test_client()

    response = client.post(
        "/tasks",
        json = {"description": "Task wihout title"}
    )

    assert response.status_code == 400
    assert response.get_json() == {
        "error": "Title is required"
    }

def test_create_task_with_title():

    client = app.test_client()

    response = client.post(
        "/tasks",
        json={"title": ""}
    )

    assert response.status_code == 400
    assert response.get_json()["error"] == "Title is required"

def test_create_task_with_whitespace_title():

    client = app.test_client()

    response = client.post(
        "/tasks",
        json={"title": " "}
    )

    assert response.status_code == 400
    assert response.get_json()["error"] == "Title is required"

def test_create_task_with_long_title():

    client = app.test_client()

    response = client.post(
        "/tasks",
        json={"title": "A" * 151}
    )

    assert response.status_code == 400
    assert response.get_json()["error"] == ("Title must be 150 characters or fewer")