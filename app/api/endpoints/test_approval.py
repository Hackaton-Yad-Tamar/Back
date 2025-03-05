import pytest
from fastapi.testclient import TestClient
from app.api.endpoints.admin.approval_api import approve_users
from app.core.admin_approval import UserResponse

client = TestClient(approve_users)

def test_get_unapproved_users():
    response = client.get("/users/unapproved")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_approve_user_success(mocker):
    mocker.patch("app.core.admin_approval.do_approve_user", return_value=UserResponse(id=1, name="Test User"))
    response = client.post("/users/1/approve")
    assert response.status_code == 200
    assert response.json()["name"] == "Test User"

def test_approve_user_not_found(mocker):
    mocker.patch("app.core.admin_approval.do_approve_user", return_value=None)
    response = client.post("/users/1/approve")
    assert response.status_code == 404
    assert response.json()["detail"] == "User not found"

def test_reject_user_success(mocker):
    mocker.patch("app.core.admin_approval.do_reject_user", return_value=UserResponse(id=1, name="Test User"))
    response = client.post("/users/1/reject")
    assert response.status_code == 200
    assert response.json()["name"] == "Test User"

def test_reject_user_not_found(mocker):
    mocker.patch("app.core.admin_approval.do_reject_user", return_value=None)
    response = client.post("/users/1/reject")
    assert response.status_code == 404
    assert response.json()["detail"] == "User not found"