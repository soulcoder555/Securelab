from app.extensions import db
from app.models import ActivityLog

def log_activity(user_id, action, details=None, ip_address=None, user_agent=None):
    """Log user activity for audit trail."""
    try:
        log_entry = ActivityLog(
            user_id=user_id,
            action=action,
            details=details,
            ip_address=ip_address,
            user_agent=user_agent
        )
        db.session.add(log_entry)
        db.session.commit()
    except Exception as e:
        # Log to stderr if database logging fails
        import sys
        print(f"Failed to log activity: {e}", file=sys.stderr)
        db.session.rollback()

def get_user_activity(user_id, limit=50):
    """Get recent activity for a user."""
    return ActivityLog.query.filter_by(user_id=user_id)\
                           .order_by(ActivityLog.timestamp.desc())\
                           .limit(limit).all()

def get_all_activity(limit=100):
    """Get recent activity for all users (admin only)."""
    return ActivityLog.query.order_by(ActivityLog.timestamp.desc())\
                           .limit(limit).all()