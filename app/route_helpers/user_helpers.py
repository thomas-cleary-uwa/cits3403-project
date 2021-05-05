""" helper functions for the user route """

from flask import flash, redirect, url_for
from flask_login import current_user

from app.route_helpers.route_helpers import get_user

from app.models import SubmittedAttempt, UserStats

def check_profile_access(username):
    """ check if the current user has access to username's profile
        return redirect obj if they do not, else None
    """

    if current_user.is_admin:
        flash('Administrators do not have a profile')
        return redirect(url_for('index'))

    if username != current_user.username:
        flash('You can not access other user\'s profiles')
        return redirect(url_for('user', username=current_user.username))

    return None # no redirect object


def get_template_data(user_id):
    """ return the data needed for the html template """


    attempts = SubmittedAttempt.query.filter_by(user_id=user_id)
    user_stats = UserStats.query.filter_by(user_id=user_id).first()

    return (attempts, user_stats)


def attempt_load_user_profile(username):
    """ return data to render the user profile, 
        if current user does not have access, return redirect object
    """
    redirect_obj = check_profile_access(username)
    if redirect_obj is not None:
        return (False, redirect_obj)

    user = get_user(username, four_zero_four=True)

    return (True, (user, get_template_data(user.id)))