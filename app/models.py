from app import db
from flask import url_for
from flask_admin import expose, AdminIndexView, expose


# Define a simple model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    email = db.Column(db.String(120))

    def __repr__(self):
        return f"<User {self.name}>"
    
class standards(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    email = db.Column(db.String(120))
    
class clausules(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))

# Custom Admin Index View
class CustomAdminIndexView(AdminIndexView):
    @expose('/')
    def index(self):
        # Add the button directly on the admin index page
        return self.render('admin/index.html', button_url=url_for('execute_function'))