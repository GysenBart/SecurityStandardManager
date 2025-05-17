from datetime import datetime
from app import db
from flask import url_for
from flask_admin import expose, AdminIndexView, expose
import sqlalchemy as sa #import Table, Column, Integer, String, Metadata, Text
from sqlalchemy.dialects.postgresql import UUID
import uuid
from app.util import update_manager


class User(db.Model):
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = db.Column(db.String(50))
    email = db.Column(db.String(120))

    def __repr__(self):
        return f"<User {self.name}>"
    
class SecurityDomains(db.Model):
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = db.Column(db.String(100))
    description = db.Column(db.Text)
    
    def __str__(self):
        return self.name
    
class SecurityControls(db.Model):
    id = db.Column(db.String(15), primary_key=True)
    name = db.Column(db.String(50))
    description = db.Column(db.Text)
    
    def __str__(self):
        return self.name
    
class SecurityStandards(db.Model):
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = db.Column(db.String(50))
    description = db.Column(db.Text)
    def __str__(self):
        return self.name
    
class Clausule(db.Model):
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = db.Column(db.String(50))
    title = db.Column(db.Text) # filled by user
    description = db.Column(db.Text) # filled by user
    created_at = db.Column(db.DateTime, default=datetime.now)
    standard_id = db.Column(UUID(as_uuid=True), sa.ForeignKey(SecurityStandards.id, name='fk_DomainStandardClausule_securityStandards_id'))
    
    def __str__(self):
        return f"{self.number} - {self.description[:50]}..."
    

# This model is used to make relationships
class DomainStandardClausule(db.Model):
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    ############# ask for nullable #############
    domain_id = db.Column(UUID(as_uuid=True), sa.ForeignKey(SecurityDomains.id, name='fk_DomainStandardClausule_securityDomains_id'))
    control_id = db.Column(UUID(as_uuid=True), sa.ForeignKey(SecurityControls.id, name='fk_DomainStandardClausule_securityControls_id'))
    standard_id = db.Column(UUID(as_uuid=True), sa.ForeignKey(SecurityStandards.id, name='fk_DomainStandardClausule_securityStandards_id'))
    clausule_id = db.Column(UUID(as_uuid=True), sa.ForeignKey(Clausule.id, name='fk_DomainStandardClausule_clausule_id'))
    version = db.Column(db.String(10))
    start_date = db.Column(db.DateTime, default=datetime.now)
    end_date = db.Column(db.DateTime)
    
    # Only needed for back population when we need a many to many relationship, i think this is not necesary in this case
    #domain = db.relationship('SecurityDomain')
    #control = db.relationship('SecurityControl')
    #standard = db.relationship('SecurityStandard')
    #clausule = db.relationship('Clausule')
    
    
# Custom Admin Index View
class CustomAdminIndexView(AdminIndexView):
    @expose('/')
    def index(self):
        # Add the button directly on the admin index page
        return self.render('admin/index.html', button_url=url_for('execute_function'), update_available=update_manager.check_for_updates())