from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from app import db
from app.models import User
from app.blueprints.auth.forms import RegistrationForm, LoginForm
from app.utils.security import log_security_event

auth = Blueprint("auth", __name__, url_prefix="/auth")


@auth.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('core.home'))

    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(
            username=form.username.data,
            email=form.email.data
        )
        user.set_password(form.password.data)

        db.session.add(user)
        db.session.commit()

        log_security_event("user_registered", f"User {user.username} registered")
        flash("Registration successful! Please log in.", "success")
        return redirect(url_for('auth.login'))

    return render_template('auth/register.html', title='Register', form=form)


@auth.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('core.home'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data) and user.is_active:
            login_user(user, remember=form.remember.data)
            log_security_event("user_login", f"User {user.username} logged in")
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('core.home'))
        else:
            log_security_event("login_failed", f"Failed login attempt for {form.username.data}")
            flash("Invalid username or password", "danger")

    return render_template('auth/login.html', title='Login', form=form)


@auth.route("/logout")
@login_required
def logout():
    log_security_event("user_logout", f"User {current_user.username} logged out")
    logout_user()
    return redirect(url_for('core.home'))
