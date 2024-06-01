import os
import sys

# Add the parent directory of 'app' to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from fastapi import status
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_get_all_blogs():
    response = client.get("/blog/all")
    assert response.status_code == 200


# test authentification endpoints
def test_auth_error():
    response = client.post("/token", data={"username": "test", "password": "test"})
    access_token = response.json().get("access_token")
    assert access_token is None
    message = response.json().get("detail")
    assert message == "Invalid credentials"


def test_auth_success():
    response = client.post("/token", data={"username": "string", "password": "string"})
    access_token = response.json().get("access_token")
    assert access_token is not None


# test post article endpoint
def test_post_article():
    response = client.post("/token", data={"username": "string", "password": "string"})
    access_token = response.json().get("access_token")

    assert access_token

    response = client.post(
        "/article",
        json={
            "title": "Test article",
            "content": "Test content",
            "published": True,
            "creator_id": 1,
        },
        headers={"Authorization": f"Bearer {access_token}"},
    )

    assert response.status_code == status.HTTP_200_OK

    article = response.json()
    assert article["title"] == "Test article"
    assert article["content"] == "Test content"
    assert article["published"] == True
    assert article["user"]["username"] == "string"
