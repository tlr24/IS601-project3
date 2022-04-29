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

def test_successful_login(client, add_user):
    """Tests successful login"""
    # test that viewing the page renders without template errors
    assert client.get("/login").status_code == 200

    # test that successful login redirects to the index page
    response = client.post("/login", data={"email": "a@a.com", "password": "12345678"})
    assert response.headers["Location"] == "/dashboard"

    with client.application.app_context():
        user_id = User.query.filter_by(email="a@a.com").first().get_id()

    # check that the login request set the user_id in the session
    with client:
        client.get("/")
        assert session["_user_id"] == user_id
