from app import db


# Define a simple model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    email = db.Column(db.String(120))

    def __repr__(self):
        return f"<User {self.name}>"