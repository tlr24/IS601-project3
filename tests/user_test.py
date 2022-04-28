import logging

from app import db
from app.db.models import User, Song

def test_adding_user(application):
    log = logging.getLogger("myApp")
    with application.app_context():
        assert db.session.query(User).count() == 0
        assert db.session.query(Song).count() == 0
        #showing how to add a record
        #create a record
        user = User('tttt@gmail.com', '12345678')
        #add it to get ready to be committed
        db.session.add(user)
        #call the commit
        db.session.commit()
        #assert that we now have a new user
        assert db.session.query(User).count() == 1
        #finding one user record by email
        user = User.query.filter_by(email='tttt@gmail.com').first()
        log.info(user)
        #asserting that the user retrieved is correct
        assert user.email == 'tttt@gmail.com'
