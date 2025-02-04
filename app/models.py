import datetime
from app import db
from flask import url_for
from flask_admin import expose, AdminIndexView, expose
from sqlalchemy import Table, Column, Integer, String, Metadata, Text
from sqlalchemy.dialects.postgresql import UUID
import uuid


# Define a simple model - can be removed later
class User(db.Model):
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = db.Column(db.String(50))
    email = db.Column(db.String(120))

    def __repr__(self):
        return f"<User {self.name}>"
    
class SecurityDomains(db.Model):
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = db.Column(db.String(100))
    
    def __str__(self):
        return self.name
    
class SecurityControls(db.model):
    id = db.Column(db.String(15), primary_key=True)
    name = db.Column(db.String(50))
    discription = db.Column(db.Text)
    
    def __str__(self):
        return self.name
    
class SecurityStandards(db.Model):
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = db.Column(db.String(50))
    discription = db.Column(db.Text)
    
    def __str__(self):
        return self.name
    
class Clausule(db.Model):
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = db.Column(db.String(50))
    discription = db.Column(db.Text)
    created_at = db.Column(db.DataTime, default=datetime.utcnow)
    
    def __str__(self):
        return f"{self.number} - {self.description[:50]}..."
    
class ClausuleComment(db.Model):
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    clausule_id = db.Column(db.Integer, db.ForeignKey('clausule.id'))
    comment = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    clausule = db.relationship('Clausule')
    
class DomainStandardClausule(db.model):
    # create all the relationships here
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    domain_id = db.Column(db.Integer, db.ForeignKey('security_domain.id'))
    standard_id = db.Column(db.Integer, db.ForeignKey('security_standard.id'))
    clausule_id = db.Column(db.Integer, db.ForeignKey('clausule.id'))
    version = db.Column(db.String(10))
    start_date = db.Column(db.DateTime, default=datetime.utcnow)
    end_date = db.Column(db.DateTime)
    
    domain = db.relationship('SecurityDomain')
    standard = db.relationship('SecurityStandard')
    clausule = db.relationship('Clausule')
    
    
# Custom Admin Index View
class CustomAdminIndexView(AdminIndexView):
    @expose('/')
    def index(self):
        # Add the button directly on the admin index page
        return self.render('admin/index.html', button_url=url_for('execute_function'))