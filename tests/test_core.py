import pytest
import os
from flask import url_for
from app.models import Note, User
from app.extensions import db


def test_home_page_requires_login(client):
    response = client.get(url_for('core.home'))
    assert response.status_code == 302  # Redirect to login


def test_home_page_authenticated(client, test_user):
    client.post(url_for('auth.login'), data={
        'username': 'testuser',
        'password': 'password'
    })

    response = client.get(url_for('core.home'))
    assert response.status_code == 200
    assert b'Welcome' in response.data


def test_create_note(client, test_user, app):
    client.post(url_for('auth.login'), data={
        'username': 'testuser',
        'password': 'password'
    })

    with app.app_context():
        response = client.post(url_for('core.notes'), data={
            'title': 'Test Note',
            'content': 'This is a test note',
            'is_completed': False
        }, follow_redirects=True)

        assert response.status_code == 200
        note = Note.query.filter_by(title='Test Note').first()
        assert note is not None
        # Get user from database in current context
        user = User.query.filter_by(username='testuser').first()
        assert note.user_id == user.id


def test_upload_file(client, test_user, app):
    client.post(url_for('auth.login'), data={
        'username': 'testuser',
        'password': 'password'
    })

    # Create a test file
    test_file_path = os.path.join(app.config['UPLOAD_FOLDER'], 'test.txt')
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    with open(test_file_path, 'w') as f:
        f.write('test content')

    with open(test_file_path, 'rb') as f:
        response = client.post(url_for('core.upload'),
                             data={'file': (f, 'test.txt')},
                             content_type='multipart/form-data',
                             follow_redirects=True)

    assert response.status_code == 200
    assert b'uploaded successfully' in response.data

    # Cleanup
    os.remove(test_file_path)


def test_search_notes(client, test_user, app):
    client.post(url_for('auth.login'), data={
        'username': 'testuser',
        'password': 'password'
    })

    # Create a note first
    with app.app_context():
        user = User.query.filter_by(username='testuser').first()
        note = Note(title='Search Test', content='This is searchable content', user_id=user.id)
        db.session.add(note)
        db.session.commit()

    response = client.post(url_for('core.search'), data={'query': 'searchable'})
    assert response.status_code == 200
    assert b'Search Test' in response.data