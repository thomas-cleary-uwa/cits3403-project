""" helper functions for the register route """

from flask import flash, redirect, url_for

from app import db
from app.models import User, UserStats


def add_user(username, email, password):
    """ add user to database """
    user = User(username=username, email=email)
    user.set_password(password)

    db.session.add(user)
    db.session.commit()

    add_user_stats(user.id)


def add_user_stats(user_id):
    """ add stats to db for user with user_id """
    user_stats = UserStats(user_id=user_id)

    db.session.add(user_stats)
    db.session.commit()


def attempt_registration(
    register_form, 
    redirect_route="login",
    flash_message="Congratulations, you are now a registered user!"
):
    """ return redirect object depending on the success of the registration """

    add_user(register_form.username.data, register_form.email.data, register_form.password.data)

    # flash a message to the screen for the user
    flash(flash_message)

    return redirect(url_for(redirect_route))