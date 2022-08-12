from fastapi.testclient import TestClient

from app import app
from utils import generate_jwt_token, decode_jwt_token
from log import log

client = TestClient(app)

token = None


def test_token():
    token = generate_jwt_token(1, "admin")
    data = decode_jwt_token(token)
    assert data['user_id'] == 1
    assert data['username'] == 'admin'

def test_login():
    response = client.post(
        "/api/users/login", json={"username": "admin", "password": "admin"})
    
    assert response.status_code == 200
    assert response.json()["status"] == "ok"
    assert response.json()["message"] == "登录成功"
    assert response.json()["data"]['token'] is not None
    global token
    token = response.json()["data"]['token']


def test_get_me():
    global token
    response = client.get(
        "/api/users/me", headers={"Authorization": f"Bearer {token}"})
    log.debug(response.json())
    assert response.status_code == 200
    assert response.json()["status"] == "ok"
    assert response.json()["message"] == "获取成功"
    assert response.json()["data"]['username'] == "admin"
