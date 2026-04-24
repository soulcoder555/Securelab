import os
import re
from werkzeug.utils import secure_filename
from flask import current_app

ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
MAX_FILENAME_LENGTH = 255

def allowed_file(filename):
    """Check if file extension is allowed."""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def secure_filename_custom(filename):
    """Secure filename with additional checks."""
    filename = secure_filename(filename)
    if len(filename) > MAX_FILENAME_LENGTH:
        raise ValueError("Filename too long")
    if not filename:
        raise ValueError("Invalid filename")
    return filename

def sanitize_input(text):
    """Basic input sanitization - remove dangerous characters."""
    if not isinstance(text, str):
        return ""
    # Remove null bytes and other dangerous chars
    text = text.replace('\x00', '')
    # Basic XSS prevention - remove script tags
    text = re.sub(r'<script[^>]*>.*?</script>', '', text, flags=re.IGNORECASE | re.DOTALL)
    return text.strip()

def validate_username(username):
    """Validate username format."""
    if not username or len(username) < 3 or len(username) > 80:
        return False
    # Only alphanumeric, underscore, dash
    return bool(re.match(r'^[a-zA-Z0-9_-]+$', username))

def validate_email(email):
    """Basic email validation."""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email)) and len(email) <= 120

def validate_user_claims(user):
    """Validate all user claims/permissions are valid."""
    if not user:
        return False, "User not found"

    # Check if user is active
    if not user.is_active:
        return False, "User account is inactive"

    # Validate role is valid
    valid_roles = ['user', 'admin']
    if user.role not in valid_roles:
        return False, f"Invalid role: {user.role}"

    # Check username format
    if not validate_username(user.username):
        return False, "Invalid username format"

    # Check email format
    if not validate_email(user.email):
        return False, "Invalid email format"

    # Check password hash exists and is valid format
    if not user.password_hash or len(user.password_hash) < 10:
        return False, "Invalid password hash"

    return True, "All claims valid"

def check_all_users_claims():
    """Check claims validity for all users in the system."""
    from app.models import User
    from app.extensions import db
    from flask import current_app

    invalid_users = []
    valid_count = 0

    try:
        users = User.query.all()
        for user in users:
            is_valid, message = validate_user_claims(user)
            if not is_valid:
                invalid_users.append({
                    'user_id': user.id,
                    'username': user.username,
                    'issue': message
                })
            else:
                valid_count += 1

        return {
            'total_users': len(users),
            'valid_users': valid_count,
            'invalid_users': invalid_users,
            'all_valid': len(invalid_users) == 0
        }
    except Exception as e:
        return {
            'error': f"Failed to check user claims: {str(e)}",
            'total_users': 0,
            'valid_users': 0,
            'invalid_users': [],
            'all_valid': False
        }

def log_security_event(action, details=None):
    """Log security-related events."""
    from app.utils.audit import log_activity
    from flask_login import current_user
    from flask import request

    user_id = current_user.id if current_user.is_authenticated else None
    log_activity(user_id, action, details, request.remote_addr, request.user_agent.string)