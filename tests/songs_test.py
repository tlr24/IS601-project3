"""Tests the songs functionality"""
import logging
import csv
import os
import pytest
from app.db.models import db, Song, User


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

def test_adding_songs(application):
    """Test adding songs"""
    with application.app_context():
        user = User('tttt@gmail.com', '12345678')
        db.session.add(user)
        db.session.commit()
        # prepare songs to insert
        user.songs = [Song("title1", "artist1", "2020", "Rap"), Song("title2", "artist2", "2022", "Pop")]
        db.session.commit()
        assert db.session.query(Song).count() == 2
        song1 = Song.query.filter_by(title='title1').first()
        assert song1.title == "title1"
        # changing the title of the song
        song1.title = "New Song"
        db.session.commit()
        song2 = Song.query.filter_by(title='New Song').first()
        assert song2.title == "New Song"
        # checking cascade delete
        db.session.delete(user)
        assert db.session.query(User).count() == 0
        assert db.session.query(Song).count() == 0
