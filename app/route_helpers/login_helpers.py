""" helper functions for the login route """

from flask import flash, redirect, url_for
from flask_login import current_user, login_user

from app.route_helpers.route_helpers import get_user, redirect_next
from app import db
from app.models import UserStats


def is_user_valid(username, flash_message="Invalid username", redirect_route="index"):
    """ if username in db return (user, None)
        else return (False, redirect_obj)
    """
    user = get_user(username)
    
    if user is None:
        flash(flash_message)
        return (None, redirect(url_for(redirect_route)))

    return (user, None)


def is_password_valid(user, password, flash_message="Incorrect password", redirect_route="index"):
    """ if password is valid return (True, None)
        else return (False, redirect object) and flash a message
    """
    if user is None or not user.check_password(password):
        flash(flash_message)
        return (False, redirect(url_for(redirect_route)))

    return (True, None)


def update_login_stat():
    """ increment the user login count by 1 if they are not an admin """
    if not current_user.is_admin:
        UserStats.query.filter_by(user_id=current_user.id).first().num_logins += 1
        db.session.commit()


def attempt_login(login_form):
    """ returns a redirect object depending on if the login submission was valid or not """
    # check user name exists
    user, redirect_obj = is_user_valid(login_form.username.data)
    if not user:
        return redirect_obj

    # check password correct
    password_valid, redirect_obj = is_password_valid(user, login_form.password.data)
    if not password_valid:
        return redirect_obj

    # if username and password are correct log in the user
    login_user(user, remember=login_form.remember_me.data)

    # update login stat
    update_login_stat()

    next_redirect_obj = redirect_next()
    return next_redirect_obj
