""" helper functions for before_request route """

from datetime import datetime
from flask_login import current_user

from app import db
from app.models import UserStats


def before_request():
    """ do these things before each request """
    # update the time this user was last seen on the website
    if current_user.is_authenticated and not current_user.is_admin:
        UserStats.query.filter_by(user_id=current_user.id).first().last_seen = datetime.utcnow()
        db.session.commit()