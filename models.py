# Import SQLAlchemy
from flask_sqlalchemy import SQLAlchemy

# SQLAlchemy database
db = SQLAlchemy()

# Users model and functions
class Users(db.Model):
    # Fields for user model
    __tablename__ = "users"
    user_id = db.Column('user_id', db.Integer, primary_key = True)
    username = db.Column('username', db.String(50))
    password = db.Column('password', db.String(150))

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def get_id(self):
        return self.user_id

    def __repr__(self):
        return '<User %r>' % (self.username)

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

class AnonymousUserMixin(object):
    @property
    def is_authenticated(self):
        return False

    @property
    def is_active(self):
        return False

    @property
    def is_anonymous(self):
        return True

    def get_id(self):
        return

# Students models
class Students(db.Model):
    # Fields for student model
    id = db.Column(db.Integer, primary_key = True)
    firstname = db.Column(db.String(50))
    lastname = db.Column(db.String(50))
    email = db.Column(db.String(50))
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))

    def __repr__(self):
        return self.Students