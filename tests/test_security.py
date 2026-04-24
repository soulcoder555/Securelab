import pytest
from flask import url_for
from app.utils.security import sanitize_input, validate_username, validate_email, allowed_file


def test_sanitize_input():
    # Test basic sanitization
    assert sanitize_input("Hello World") == "Hello World"
    assert sanitize_input("   spaced   ") == "spaced"
    assert sanitize_input("") == ""
    assert sanitize_input(None) == ""

    # Test XSS prevention
    malicious = "<script>alert('xss')</script>Hello"
    sanitized = sanitize_input(malicious)
    assert "<script>" not in sanitized
    assert "Hello" in sanitized


def test_validate_username():
    assert validate_username("validuser") == True
    assert validate_username("user_123") == True
    assert validate_username("user-name") == True
    assert validate_username("") == False
    assert validate_username("u") == False  # Too short
    assert validate_username("user@domain") == False  # Invalid char
    assert validate_username("a" * 81) == False  # Too long


def test_validate_email():
    assert validate_email("user@example.com") == True
    assert validate_email("test.email+tag@domain.co.uk") == True
    assert validate_email("invalid-email") == False
    assert validate_email("") == False
    assert validate_email("a" * 121 + "@example.com") == False  # Too long


def test_allowed_file():
    assert allowed_file("test.txt") == True
    assert allowed_file("image.png") == True
    assert allowed_file("document.pdf") == True
    assert allowed_file("script.exe") == False
    assert allowed_file("file") == False  # No extension
    assert allowed_file("file.txt.exe") == False  # Multiple extensions, last not allowed


def test_create_user_api_security(client, app):
    # Test that the API endpoint is disabled by default
    response = client.post(url_for('core.create_user'), json={'username': 'test'})
    assert response.status_code == 403
    assert b'disabled' in response.data

    # Enable training mode
    app.config['TRAINING_MODE'] = True

    # Now it should work
    response = client.post(url_for('core.create_user'), json={'username': 'testuser'})
    assert response.status_code == 201
    assert b'created' in response.data


def test_input_validation_on_registration(client):
    # Test XSS prevention in registration
    response = client.post(url_for('auth.register'), data={
        'username': '<script>alert("xss")</script>user',
        'email': 'test@example.com',
        'password': 'password123',
        'confirm_password': 'password123'
    }, follow_redirects=True)

    # Should fail validation due to username
    assert b'Username can only contain' in response.data


def test_validate_user_claims():
    """Test user claims validation."""
    from app.utils.security import validate_user_claims
    from app.models import User

    # Test valid user
    valid_user = User(
        username='testuser',
        email='test@example.com',
        password_hash='hashed_password',
        role='user',
        is_active=True
    )
    is_valid, message = validate_user_claims(valid_user)
    assert is_valid == True
    assert message == "All claims valid"

    # Test invalid username
    invalid_user = User(
        username='us',  # Too short
        email='test@example.com',
        password_hash='hashed_password',
        role='user',
        is_active=True
    )
    is_valid, message = validate_user_claims(invalid_user)
    assert is_valid == False
    assert "Invalid username format" in message

    # Test invalid role
    invalid_role_user = User(
        username='testuser',
        email='test@example.com',
        password_hash='hashed_password',
        role='invalid_role',
        is_active=True
    )
    is_valid, message = validate_user_claims(invalid_role_user)
    assert is_valid == False
    assert "Invalid role" in message

    # Test inactive user
    inactive_user = User(
        username='testuser',
        email='test@example.com',
        password_hash='hashed_password',
        role='user',
        is_active=False
    )
    is_valid, message = validate_user_claims(inactive_user)
    assert is_valid == False
    assert "inactive" in message

    # Test None user
    is_valid, message = validate_user_claims(None)
    assert is_valid == False
    assert "User not found" in message


def test_check_all_users_claims(client, app):
    """Test checking all users claims."""
    from app.utils.security import check_all_users_claims

    with app.app_context():
        result = check_all_users_claims()

        assert 'total_users' in result
        assert 'valid_users' in result
        assert 'invalid_users' in result
        assert 'all_valid' in result
        assert isinstance(result['invalid_users'], list)