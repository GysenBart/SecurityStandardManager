from app import db
from flask import url_for
from flask_admin import expose, AdminIndexView, expose
from sqlalchemy import Table, Column, Integer, String, Metadata
from sqlalchemy.dialects.postgresql import UUID
import uuid


# Define a simple model - can be removed later
class User(db.Model):
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = db.Column(db.String(50))
    email = db.Column(db.String(120))

    def __repr__(self):
        return f"<User {self.name}>"
    
class domains(db.Model):
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    SCFdomain = db.Column(db.string(100))
    SCFcontrol = db.Column(db.string(100))
    
class standards(db.Model):
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = db.Column(db.String(50))
    email = db.Column(db.String(120))
    
class clausules(db.Model):
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = db.Column(db.String(50))

# Custom Admin Index View
class CustomAdminIndexView(AdminIndexView):
    @expose('/')
    def index(self):
        # Add the button directly on the admin index page
        return self.render('admin/index.html', button_url=url_for('execute_function'))
    
# Dynamic models
