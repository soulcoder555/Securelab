from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from app.extensions import db


class User(db.Model, UserMixin):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    role = db.Column(db.String(20), default='user', nullable=False)  # 'user' or 'admin'
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    is_active = db.Column(db.Boolean, default=True, nullable=False)

    notes = db.relationship('Note', backref='author', lazy='dynamic')
    activities = db.relationship('ActivityLog', backref='user', lazy='dynamic')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def is_admin(self):
        return self.role == 'admin'

    def __repr__(self):
        return f"<User {self.username}>"


class Note(db.Model):
    __tablename__ = "notes"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    is_completed = db.Column(db.Boolean, default=False, nullable=False)

    def __repr__(self):
        return f"<Note {self.title}>"


class ActivityLog(db.Model):
    __tablename__ = "activity_logs"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    action = db.Column(db.String(100), nullable=False)
    details = db.Column(db.Text)
    ip_address = db.Column(db.String(45))  # IPv6 ready
    user_agent = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    def __repr__(self):
        return f"<ActivityLog {self.action} by {self.user_id}>"


class Challenge(db.Model):
    __tablename__ = "challenges"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    vulnerability_type = db.Column(db.String(100), nullable=False)  # XSS, SQL Injection, etc.
    difficulty = db.Column(db.String(20), nullable=False)  # Beginner, Intermediate, Advanced
    objective = db.Column(db.Text, nullable=False)
    hints = db.Column(db.Text)  # JSON format with multiple hints
    writeup = db.Column(db.Text)
    points = db.Column(db.Integer, default=100)
    learning_path = db.Column(db.String(50))  # Like 'web-security', 'api-security', etc.
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    user_progress = db.relationship('UserProgress', backref='challenge', lazy='dynamic', cascade='all, delete-orphan')

    def __repr__(self):
        return f"<Challenge {self.title}>"


class UserProgress(db.Model):
    __tablename__ = "user_progress"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    challenge_id = db.Column(db.Integer, db.ForeignKey('challenges.id'), nullable=False)
    completed = db.Column(db.Boolean, default=False)
    attempts = db.Column(db.Integer, default=0)
    hints_viewed = db.Column(db.Integer, default=0)
    completed_at = db.Column(db.DateTime)
    started_at = db.Column(db.DateTime, default=datetime.utcnow)
    points_earned = db.Column(db.Integer, default=0)

    user = db.relationship('User', backref='progress')

    def __repr__(self):
        return f"<UserProgress User:{self.user_id} Challenge:{self.challenge_id}>"


class Vulnerability(db.Model):
    __tablename__ = "vulnerabilities"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    description = db.Column(db.Text, nullable=False)
    severity = db.Column(db.String(20))  # Critical, High, Medium, Low
    category = db.Column(db.String(100))
    cve_id = db.Column(db.String(20))
    affected_code = db.Column(db.Text)
    fixed_code = db.Column(db.Text)
    resources = db.Column(db.Text)  # JSON links to external resources
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Vulnerability {self.name}>"
