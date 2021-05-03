from app import db, login
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from hashlib import md5
from datetime import datetime


@login.user_loader
def load_user(id):
    return User.query.get(int(id))       


class User(UserMixin, db.Model):

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    registered_on = db.Column(db.DateTime, default=datetime.utcnow)
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)
    is_admin = db.Column(db.Boolean, default=False)
    has_saved_attempt = db.Column(db.Boolean, default=False)
    saved_attempt = db.relationship('SavedAttempt', backref='taker', lazy='dynamic')
    submitted_attempt = db.relationship('SubmittedAttempt', backref='taker', lazy='dynamic')



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


class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.String(128), index=True, unique=True)
    response_a = db.Column(db.String(64), index=True)   
    response_b = db.Column(db.String(64), index=True)
    response_c = db.Column(db.String(64), index=True)
    answer = db.Column(db.Integer, index=True)

    def __repr__(self):
        return '<Quiz {}>'.format(self.question)


class SubmittedAttempt(db.Model):
    
    attempt_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey(User.id), nullable=True)
    
    question_a_id = db.Column(db.Integer, db.ForeignKey(User.id))
    response_a = db.Column(db.Integer, index=True)
    mark_a = db.Column(db.Integer, index=True)
    
    question_b_id = db.Column(db.Integer, db.ForeignKey(User.id))
    response_b = db.Column(db.Integer, index=True)
    mark_b = db.Column(db.Integer, index=True)
    
    question_c_id = db.Column(db.Integer, db.ForeignKey(User.id))
    response_c = db.Column(db.Integer, index=True)
    mark_c = db.Column(db.Integer, index=True)

    score = db.Column(db.Integer, index=True)

    attempt_datetime = db.Column(db.DateTime, index=True)

    # currently returns score only
    def __repr__(self):
        return '<Attempt: {}>'.format(self.score)


class SavedAttempt(db.Model):

    attempt_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey(User.id), nullable=True)

    question_a_id = db.Column(db.Integer, db.ForeignKey(User.id))
    response_a = db.Column(db.Integer, index=True, nullable=True)
    
    question_b_id = db.Column(db.Integer, db.ForeignKey(User.id))
    response_b = db.Column(db.Integer, index=True, nullable=True)
    
    question_c_id = db.Column(db.Integer, db.ForeignKey(User.id))
    response_c = db.Column(db.Integer, index=True, nullable=True)

    # currently returns score only
    def __repr__(self):
        return '<Attempt: {}>'.format(self.score)
