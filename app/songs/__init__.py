import csv
import logging
import os
from flask import Blueprint, render_template, abort, url_for, current_app
from flask_login import current_user, login_required
from app.db import db
from app.db.models import Song
from app.songs.forms import csv_upload
from jinja2 import TemplateNotFound
from werkzeug.utils import secure_filename, redirect

song = Blueprint('songs', __name__, template_folder='templates')


@song.route('/songs/upload', methods=['POST', 'GET'])
@login_required
def song_upload():
    form = csv_upload()
    if form.validate_on_submit():
        log = logging.getLogger("csv")
        filename = secure_filename(form.file.data.filename)
        filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
        form.file.data.save(filepath)
        log.info("User " + str(current_user.get_id()) + " uploaded file: " + filename)
        # user = current_user
        list_of_songs = []
        with open(filepath) as file:
            csv_file = csv.DictReader(file)
            for row in csv_file:
                song = Song.query.filter_by(title=row['Name']).first()
                if song is None:
                    current_user.songs.append(Song(row['Name'], row['Artist'], row['Year'], row['Genre']))
                    db.session.commit()
                else:
                    current_user.songs.append(song)
                    db.session.commit()

        return redirect(url_for('songs.songs_browse'), 302)
    try:
        return render_template('upload_songs.html', form=form)
    except TemplateNotFound:
        abort(404)

@song.route('/songs', methods=['GET'], defaults={"page": 1})
@song.route('/songs/<int:page>', methods=['GET'])
@login_required
def songs_browse(page):
    page = page
    per_page = 1000
    pagination = Song.query.paginate(page, per_page, error_out=False)
    data = pagination.items
    try:
        return render_template('browse_songs.html',data=data,pagination=pagination)
    except TemplateNotFound:
        abort(404)