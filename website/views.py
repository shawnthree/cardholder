from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from sqlalchemy import null
from .models import Note
from . import db
import json

views = Blueprint('views', __name__)


@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST':
        note = request.form.get('note')

        try:
            if len(note) < 20:
                flash('Card info is too short!', category='error')
            elif len(note) > 20:
                flash('Card info is too short!', category='error')
            elif int(note[:16])==null:
                flash('CardNumber should be all numbers', category='error')
            elif int(note[17:])==null:
                flash('Security code should be all numbers', category='error')
            else:
                new_note = Note(data=note, user_id=current_user.id)
                db.session.add(new_note)
                db.session.commit()
                flash('Card added!', category='success')
        except:
            flash('Card Number and Security Code should not contain any invalid digits',category='error')

    return render_template("home.html", user=current_user)


@views.route('/delete-note', methods=['POST'])
def delete_note():
    note = json.loads(request.data)
    noteId = note['noteId']
    note = Note.query.get(noteId)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()

    return jsonify({})