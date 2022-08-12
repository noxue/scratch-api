from fastapi.testclient import TestClient

from app import app
from log import log

client = TestClient(app)


token = None


# def test_login():
#     response = client.post(
#         "/api/users/login", json={"username": "admin", "password": "admin"})

#     assert response.status_code == 200
#     assert response.json()["status"] == "ok"
#     assert response.json()["message"] == "登录成功"
#     assert response.json()["data"]['token'] is not None
#     global token
#     token = response.json()["data"]['token']
#     log.debug(token)


def test_create():
    response = client.post('/api/scratch/projects/', data="xxxxxxxxxxx", params={
                           "title": "xxxxxttttitle"},  headers={"Authorization": f"Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoxMSwidXNlcm5hbWUiOiJhZG1pbiIsImV4cCI6MTY2MjkzMTE1M30.ExiJs1uS7257vrb7lQfKp9uwQ5iQQcLxmkfAj-0Q5eI"})
    assert response.status_code == 200
    assert response.json()["status"] == "ok"
    log.debug(response.json())
    

