from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_required, current_user
from app import db
from app.models import User, ActivityLog
from app.blueprints.admin.forms import UserManagementForm
from app.utils.audit import get_all_activity
from app.utils.security import check_all_users_claims

admin = Blueprint("admin", __name__, url_prefix="/admin")


def admin_required(f):
    """Decorator to require admin role."""
    @login_required
    def decorated_function(*args, **kwargs):
        if not current_user.is_admin():
            flash("Admin access required.", "danger")
            return redirect(url_for('core.home'))
        return f(*args, **kwargs)
    decorated_function.__name__ = f.__name__
    return decorated_function


@admin.route("/dashboard")
@admin_required
def dashboard():
    users = User.query.all()
    recent_activity = get_all_activity(limit=20)
    return render_template('admin/dashboard.html', title='Admin Dashboard',
                         users=users, activities=recent_activity)


@admin.route("/users/<int:user_id>", methods=["GET", "POST"])
@admin_required
def manage_user(user_id):
    user = User.query.get_or_404(user_id)
    form = UserManagementForm(obj=user)

    if form.validate_on_submit():
        user.username = form.username.data
        user.email = form.email.data
        user.role = form.role.data
        user.is_active = form.is_active.data
        db.session.commit()
        flash(f"User {user.username} updated successfully!", "success")
        return redirect(url_for('admin.dashboard'))

    return render_template('admin/dashboard.html', title='Manage User',
                         form=form, user=user)


@admin.route("/check-claims")
@admin_required
def check_claims():
    """Check validity of all user claims/permissions."""
    result = check_all_users_claims()

    if request.is_json or request.args.get('json'):
        return jsonify(result)

    return render_template('admin/claims_check.html', title='Claims Validation',
                         result=result)


@admin.route("/users/<int:user_id>/toggle", methods=["POST"])
@admin_required
def toggle_user(user_id):
    user = User.query.get_or_404(user_id)
    user.is_active = not user.is_active
    db.session.commit()
    status = "activated" if user.is_active else "deactivated"
    flash(f"User {user.username} {status}.", "success")
    return redirect(url_for('admin.dashboard'))