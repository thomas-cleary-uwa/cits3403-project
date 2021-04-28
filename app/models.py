from app import db, login
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin, current_user
from hashlib import md5
from datetime import datetime
from flask_admin.contrib.sqla import ModelView
from flask import redirect, url_for


@login.user_loader
def load_user(id):
    return User.query.get(int(id))       


class User(UserMixin, db.Model):

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    lastSeen = db.Column(db.DateTime, default=datetime.utcnow)
    isAdmin = db.Column(db.Boolean, default=False)


    def __repr__(self):
        return '<User {}>'.format(self.username)


    def set_password(self, password):
        self.password_hash = generate_password_hash(password)


    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


    def avatar(self, size):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(
            digest, size
        )


class Quiz(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.String(128), index=True, unique=True)
    response_a = db.Column(db.String(64), index=True, unique=True)   
    response_b = db.Column(db.String(64), index=True, unique=True)
    response_c = db.Column(db.String(64), index=True, unique=True)
    answer = db.Column(db.String(12), index=True, unique=True) 

    def __repr__(self):
        return '<Quiz {}>'.format(self.question)


class AdminModelView(ModelView):

    def is_accessible(self):
        return current_user.is_authenticated and current_user.isAdmin

    def inaccessible_callback(self, name, **kwargs):
        # redirect to login page if user doesn't have access
        return redirect(url_for('index'))