from flask import Blueprint, render_template, redirect, url_for, flash, request, current_app, send_from_directory, jsonify
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
import os
from app import db
from app.models import Note, User
from app.blueprints.core.forms import NoteForm, UploadForm, SearchForm
from app.utils.security import allowed_file, secure_filename_custom, sanitize_input, log_security_event

core = Blueprint("core", __name__)


@core.route("/")
@core.route("/home")
@login_required
def home():
    notes = Note.query.filter_by(user_id=current_user.id).order_by(Note.created_at.desc()).limit(5).all()
    return render_template('core/home.html', title='Home', notes=notes)


@core.route("/notes", methods=["GET", "POST"])
@login_required
def notes():
    form = NoteForm()
    search_form = SearchForm()

    query = request.args.get('q', '')
    if query:
        notes = Note.query.filter(
            Note.user_id == current_user.id,
            (Note.title.contains(query) | Note.content.contains(query))
        ).order_by(Note.created_at.desc()).all()
    else:
        notes = Note.query.filter_by(user_id=current_user.id).order_by(Note.created_at.desc()).all()

    if form.validate_on_submit():
        note = Note(
            title=sanitize_input(form.title.data),
            content=sanitize_input(form.content.data),
            user_id=current_user.id,
            is_completed=form.is_completed.data
        )
        db.session.add(note)
        db.session.commit()
        log_security_event("note_created", f"Note '{note.title}' created")
        flash("Note created successfully!", "success")
        return redirect(url_for('core.notes'))

    return render_template('core/notes.html', title='My Notes',
                         form=form, notes=notes, search_form=search_form, query=query)


@core.route("/notes/<int:note_id>/edit", methods=["GET", "POST"])
@login_required
def edit_note(note_id):
    note = Note.query.filter_by(id=note_id, user_id=current_user.id).first_or_404()
    form = NoteForm(obj=note)

    if form.validate_on_submit():
        note.title = sanitize_input(form.title.data)
        note.content = sanitize_input(form.content.data)
        note.is_completed = form.is_completed.data
        db.session.commit()
        log_security_event("note_updated", f"Note '{note.title}' updated")
        flash("Note updated successfully!", "success")
        return redirect(url_for('core.notes'))

    return render_template('core/notes.html', title='Edit Note', form=form, edit_note=note)


@core.route("/notes/<int:note_id>/delete", methods=["POST"])
@login_required
def delete_note(note_id):
    note = Note.query.filter_by(id=note_id, user_id=current_user.id).first_or_404()
    db.session.delete(note)
    db.session.commit()
    log_security_event("note_deleted", f"Note '{note.title}' deleted")
    flash("Note deleted successfully!", "success")
    return redirect(url_for('core.notes'))


@core.route("/upload", methods=["GET", "POST"])
@login_required
def upload():
    form = UploadForm()
    if form.validate_on_submit():
        file = form.file.data
        if file and allowed_file(file.filename):
            filename = secure_filename_custom(file.filename)
            file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            log_security_event("file_uploaded", f"File '{filename}' uploaded")
            flash(f"File {filename} uploaded successfully!", "success")
            return redirect(url_for('core.upload'))
        else:
            flash("Invalid file type!", "danger")

    # List uploaded files
    upload_dir = current_app.config['UPLOAD_FOLDER']
    files = []
    if os.path.exists(upload_dir):
        files = [f for f in os.listdir(upload_dir) if os.path.isfile(os.path.join(upload_dir, f))]

    return render_template('core/upload.html', title='File Upload', form=form, files=files)


@core.route("/uploads/<filename>")
@login_required
def uploaded_file(filename):
    return send_from_directory(current_app.config['UPLOAD_FOLDER'], filename)


@core.route("/search", methods=["GET", "POST"])
@login_required
def search():
    form = SearchForm()
    results = []

    if form.validate_on_submit() or request.args.get('q'):
        query = form.query.data or request.args.get('q')
        if query:
            results = Note.query.filter(
                Note.user_id == current_user.id,
                (Note.title.contains(query) | Note.content.contains(query))
            ).order_by(Note.created_at.desc()).all()
            log_security_event("search_performed", f"Search query: '{query}'")

    return render_template('core/search.html', title='Search', form=form, results=results)


# Legacy API endpoint for testing
@core.route("/create-user", methods=["POST"])
def create_user():
    if not current_app.config.get('TRAINING_MODE', False):
        return jsonify({"error": "Endpoint disabled"}), 403

    data = request.get_json()
    if not data or "username" not in data:
        return jsonify({"error": "Username required"}), 400

    username = sanitize_input(data["username"])
    if User.query.filter_by(username=username).first():
        return jsonify({"error": "User already exists"}), 409

    user = User(username=username, email=f"{username}@example.com")
    user.set_password("defaultpass")
    db.session.add(user)
    db.session.commit()

    return jsonify({"message": f"{username} created"}), 201