import pytest
from flask import url_for
from app.models import User


def test_register_page(client):
    response = client.get(url_for('auth.register'))
    assert response.status_code == 200
    assert b'Register' in response.data


def test_register_user(client, app):
    with app.app_context():
        response = client.post(url_for('auth.register'), data={
            'username': 'newuser',
            'email': 'new@example.com',
            'password': 'password123',
            'confirm_password': 'password123'
        }, follow_redirects=True)
        assert response.status_code == 200
        user = User.query.filter_by(username='newuser').first()
        assert user is not None
        assert user.check_password('password123')


def test_login_page(client):
    response = client.get(url_for('auth.login'))
    assert response.status_code == 200
    assert b'Login' in response.data


def test_login_user(client, test_user):
    response = client.post(url_for('auth.login'), data={
        'username': 'testuser',
        'password': 'password'
    }, follow_redirects=True)
    assert response.status_code == 200
    assert b'Welcome' in response.data


def test_login_invalid_credentials(client):
    response = client.post(url_for('auth.login'), data={
        'username': 'invalid',
        'password': 'wrong'
    }, follow_redirects=True)
    assert response.status_code == 200
    assert b'Invalid username or password' in response.data


def test_logout(client, test_user):
    # Login first
    client.post(url_for('auth.login'), data={
        'username': 'testuser',
        'password': 'password'
    })

    # Then logout
    response = client.get(url_for('auth.logout'), follow_redirects=True)
    assert response.status_code == 200
    assert b'Login' in response.data  # Should redirect to login page