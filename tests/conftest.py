import pytest
import os
from app import create_app
from app.config import TestingConfig
from app.extensions import db
from app.models import User


@pytest.fixture
def app():
    # Set up test environment
    os.environ['SECRET_KEY'] = 'test-secret-key'
    app = create_app(TestingConfig)
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def runner(app):
    return app.test_cli_runner()


@pytest.fixture
def test_user(app):
    with app.app_context():
        user = User(username='testuser', email='test@example.com')
        user.set_password('password')
        db.session.add(user)
        db.session.commit()
        return user


@pytest.fixture
def admin_user(app):
    with app.app_context():
        user = User(username='admin', email='admin@example.com', role='admin')
        user.set_password('password')
        db.session.add(user)
        db.session.commit()
        return user


@pytest.fixture
def authenticated_client(client, test_user):
    """Client that is logged in as test_user"""
    with client.application.app_context():
        # Simulate login by setting session
        with client.session_transaction() as sess:
            sess['_user_id'] = str(test_user.id)
            sess['_fresh'] = True
    return client


@pytest.fixture
def admin_client(client, admin_user):
    """Client that is logged in as admin_user"""
    with client.application.app_context():
        with client.session_transaction() as sess:
            sess['_user_id'] = str(admin_user.id)
            sess['_fresh'] = True
    return client