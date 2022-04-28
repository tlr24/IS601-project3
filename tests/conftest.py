"""This makes the test configuration setup"""
# pylint: disable=redefined-outer-name
import os

import pytest
from app import create_app, User
from app.db import db


@pytest.fixture()
def application():
    """This makes the app"""
    # you need this one if you want to see what's in the database
    # os.environ['FLASK_ENV'] = 'development'
    # you need to run it in testing to pass on GitHub
    os.environ['FLASK_ENV'] = 'testing'

    application = create_app()
    application.config.update({
        "WTF_CSRF_METHODS": [],
        "WTF_CSRF_ENABLED": False
    })

    with application.app_context():
        db.create_all()
        yield application
        db.session.remove()
        # drops the database tables after the test runs
        db.drop_all()


@pytest.fixture()
def add_user(application):
    """Adds a user when running the test"""
    with application.app_context():
        user = User('t@gmail.com', '12345678')
        db.session.add(user)
        db.session.commit()


@pytest.fixture()
def client(application):
    """This makes the http client"""
    return application.test_client()


@pytest.fixture()
def runner(application):
    """This makes the task runner"""
    return application.test_cli_runner()
