"""This tests login, registration, logout"""
from flask import session
from app.db.models import User

def test_request_main_menu_links(client):
    """This makes the index page"""
    response = client.get("/")
    assert response.status_code == 200
    assert b'href="/login"' in response.data
    assert b'href="/register"' in response.data

def test_auth_pages(client):
    """This makes the index page"""
    response = client.get("/dashboard")
    assert response.status_code == 302
    response = client.get("/register")
    assert response.status_code == 200
    response = client.get("/login")
    assert response.status_code == 200

def test_successful_register(client):
    """Tests successful registration"""
    assert client.get("register").status_code == 200
    response = client.post("register", data={"email": "a@a.com", "password": "12345678", "confirm": "12345678"})
    assert "/login" == response.headers["Location"]

    # test that the user was inserted into the database
    with client.application.app_context():
        assert User.query.filter_by(email="a@a.com").first() is not None