""" defines models for the ORM with SQLalchemy and SQLite """

from hashlib import md5
from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from app import db, login



@login.user_loader
def load_user(id):
    """ helps flask-login to know who the current user is """
    return User.query.get(int(id))



class User(UserMixin, db.Model):
    """ the user model """

    id                = db.Column(db.Integer, primary_key=True)
    username          = db.Column(db.String(64), index=True, unique=True)
    email             = db.Column(db.String(120), index=True, unique=True)
    password_hash     = db.Column(db.String(128))

    registered_on     = db.Column(db.DateTime, default=datetime.utcnow)
    last_seen         = db.Column(db.DateTime, default=datetime.utcnow)

    is_admin          = db.Column(db.Boolean, default=False)
    has_saved_attempt = db.Column(db.Boolean, default=False)

    saved_attempt     = db.relationship('SavedAttempt', backref='taker', lazy='dynamic')
    submitted_attempt = db.relationship('SubmittedAttempt', backref='taker', lazy='dynamic')


    def __repr__(self):
        return '<User {}>'.format(self.username)


    def set_password(self, password):
        """ sets the users password as a hash """
        password = password.strip()
        self.password_hash = generate_password_hash(password)


    def check_password(self, password):
        """ checks to see whether password is correct for this user """
        password = password.strip()
        return check_password_hash(self.password_hash, password)


    def get_avatar(self, size):
        """ returns the gravatar for this user """
        email_lower = self.email.lower()
        digest = md5(email_lower.encode('utf-8')).hexdigest()

        return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(
            digest, size
        )



class Question(db.Model):
    """ the question model """

    id          = db.Column(db.Integer, primary_key=True)
    question    = db.Column(db.String(128), index=True, unique=True)

    response_a  = db.Column(db.String(64), index=True)
    response_b  = db.Column(db.String(64), index=True)
    response_c  = db.Column(db.String(64), index=True)

    # refers to the number radio button that the response will be
    # a=1, b=2, c=3
    answer      = db.Column(db.Integer, index=True)

    def __repr__(self):
        return '<Quiz {}>'.format(self.question)




class SubmittedAttempt(db.Model):
    """ the submitted attempt model """

    id               = db.Column(db.Integer, primary_key=True)
    user_id          = db.Column(db.Integer, db.ForeignKey(User.id))

    question_a_id    = db.Column(db.Integer, db.ForeignKey(Question.id))
    response_a       = db.Column(db.Integer, index=True)
    mark_a           = db.Column(db.Integer, index=True)

    question_b_id    = db.Column(db.Integer, db.ForeignKey(Question.id))
    response_b       = db.Column(db.Integer, index=True)
    mark_b           = db.Column(db.Integer, index=True)

    question_c_id    = db.Column(db.Integer, db.ForeignKey(Question.id))
    response_c       = db.Column(db.Integer, index=True)
    mark_c           = db.Column(db.Integer, index=True)

    score            = db.Column(db.Integer, index=True)

    attempt_datetime = db.Column(db.DateTime, index=True)


    def __repr__(self):
        return '<Attempt: {}>'.format(self.score)



class SavedAttempt(db.Model):
    """ the saved attempt model """

    id             = db.Column(db.Integer, primary_key=True)
    user_id        = db.Column(db.Integer, db.ForeignKey(User.id))

    question_a_id  = db.Column(db.Integer, db.ForeignKey(Question.id))
    response_a     = db.Column(db.Integer, index=True, nullable=True)

    question_b_id  = db.Column(db.Integer, db.ForeignKey(Question.id))
    response_b     = db.Column(db.Integer, index=True, nullable=True)

    question_c_id  = db.Column(db.Integer, db.ForeignKey(Question.id))
    response_c     = db.Column(db.Integer, index=True, nullable=True)

    saved_datetime = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    # currently returns score only
    def __repr__(self):
        return '<Attempt: {}>\nResponse A: {}\nResponse B: {}\nResponse C: {}\n'.format(
            self.user_id,
            self.response_a,
            self.response_b,
            self.response_c
        )
