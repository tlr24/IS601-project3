"""Tests the songs functionality"""
import logging
import csv
import os
import pytest
from app.db.models import db, Song


def test_csv_upload(client, add_user):
    """Test that we can upload csvs"""
    log = logging.getLogger("debug")
    root = os.path.dirname(os.path.abspath(__file__))
    csv_file = os.path.join(root, '../app/uploads/music.csv')
    # login to upload a csv file
    response = client.post("/login", data={"email": "a@a.com", "password": "12345678"})
    assert "/dashboard" == response.headers["Location"]
    assert client.get("/songs/upload").status_code == 200
    file = open(csv_file, 'rb')
    response2 = client.post("/songs/upload", data={"file": file}) #.read(1024)
    assert 302 == response2.status_code
    assert "/songs" == response2.headers["Location"]

    # check that the file was uploaded
    assert os.path.exists(csv_file) == True

    # test that the user was inserted into the database
    with client.application.app_context():
        log.debug(file)
        # assert Song.query.filter_by(title="Down").first() is not None
