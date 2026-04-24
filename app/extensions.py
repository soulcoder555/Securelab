from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect
from flask_talisman import Talisman

db = SQLAlchemy()
login_manager = LoginManager()
csrf = CSRFProtect()
talisman = Talisman()