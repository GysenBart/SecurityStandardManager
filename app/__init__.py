from flask import Flask
from flask_admin import Admin
from flask_sqlalchemy import SQLAlchemy
from flask_admin.contrib.sqla import ModelView
from flask_migrate import Migrate
from flask_apscheduler import APScheduler

from config import Config, prod_name, debug_enabled, folder_static

# Initialize Flask app
app = Flask(__name__, static_folder=folder_static)

# Configure the database (SQLite for simplicity)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
scheduler = APScheduler(app)

# Initialize Flask-Admin

admin = Admin(app, name=prod_name, template_mode='bootstrap3')

from app import routes
from app.models import User, standards

# Add views
admin.add_view(ModelView(User, db.session, category="Test"))
admin.add_view(ModelView(standards, db.session, category="Test"))
#admin.add_view(ModelView(clausules, db.session, category="Test"))
#admin.add_view(CustomActionView(name="Custom Action", endpoint="custom_action"))