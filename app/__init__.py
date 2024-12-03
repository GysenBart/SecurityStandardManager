from flask import Flask
from flask_admin import Admin
from flask_sqlalchemy import SQLAlchemy
from flask_admin.contrib.sqla import ModelView
from flask_migrate import Migrate

from config import Config, prod_name, debug_enabled

# Initialize Flask app
app = Flask(__name__)

# Configure the database (SQLite for simplicity)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Initialize Flask-Admin
admin = Admin(app, name=prod_name, template_mode='bootstrap4')

from app.models import User
# Add views
admin.add_view(ModelView(User, db.session))