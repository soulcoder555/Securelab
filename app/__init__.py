from flask import Flask
from app.config import DevelopmentConfig
from app.extensions import db, login_manager, csrf, talisman


def create_app(config_class=DevelopmentConfig):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize extensions
    db.init_app(app)
    login_manager.init_app(app)
    csrf.init_app(app)

    # Security headers with Talisman
    csp = {
        'default-src': "'self'",
        'script-src': "'self' 'unsafe-inline'",
        'style-src': "'self' 'unsafe-inline' https://cdn.jsdelivr.net",
    }
    talisman.init_app(app, content_security_policy=csp, force_https=False)

    # Register blueprints
    from app.blueprints.auth.routes import auth
    from app.blueprints.core.routes import core
    from app.blueprints.admin.routes import admin
    from app.blueprints.learning.routes import learning

    app.register_blueprint(core)
    app.register_blueprint(auth, url_prefix='/auth')
    app.register_blueprint(admin, url_prefix='/admin')
    app.register_blueprint(learning)

    # Login manager settings
    login_manager.login_view = 'auth.login'
    login_manager.login_message_category = 'info'

    # User loader for Flask-Login
    @login_manager.user_loader
    def load_user(user_id):
        from app.models import User
        return User.query.get(int(user_id))

    @app.shell_context_processor
    def make_shell_context():
        from app.models import User
        return {
            "app": app,
            "db": db,
            "User": User,
        }

    return app
