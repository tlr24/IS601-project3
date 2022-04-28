from flask import Blueprint, render_template, abort, url_for, current_app
from flask_login import current_user, login_required
from app.songs.forms import csv_upload
from jinja2 import TemplateNotFound

song = Blueprint('songs', __name__, template_folder='templates')

@song.route('/songs/upload', methods=['POST', 'GET'])
@login_required
def song_upload():
    form = csv_upload()
    try:
        return render_template('upload_songs.html', form=form)
    except TemplateNotFound:
        abort(404)
