from flask import Flask
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from flask_migrate import Migrate
from grocery_app.config import Config
from .extensions import db
from .models import User
from grocery_app.extensions import app
from .login_manager import login_manager
from flask_sqlalchemy import SQLAlchemy

def create_app():
  app = Flask(__name__)
  app.config.from_object(Config)
  db.init_app(app)
  login_manager.init_app(app)

# Initialize Flask app
app = Flask(__name__)
app.config.from_object(Config)

# Initialize extensions
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.init_app(app)
login_manager.login_view = 'auth.login'
migrate = Migrate(app, db)

# User loader for Flask-Login
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Import and register blueprints
from grocery_app.routes import main, auth
app.register_blueprint(main)
app.register_blueprint(auth)
